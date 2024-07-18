import pygame
import random
import numpy as np
import sys
import os
from math import sin, cos, pi

# Initialize Pygame
pygame.init()

# Get the screen resolution
infoObject = pygame.display.Info()
screen_width = infoObject.current_w
screen_height = infoObject.current_h

# Set the screen dimensions and make it fullscreen
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Whack-a-Pirate")

# Load images
pirate_images = [pygame.image.load(f"images/pirate{i}.png") for i in range(1, 7)]
skull_image = pygame.image.load("images/skull.jpg")
skull_image = pygame.transform.scale(skull_image, (pirate_images[0].get_width(), pirate_images[0].get_height()))

# Define the number of locations and the distance from the center
num_locations = 6
dist_from_ctr = 300

# Calculate flicker frequencies
refresh_rate = 60
frames_per_cycle = range(10, 41, 2)
viable_freqs = np.array([refresh_rate / f for f in frames_per_cycle])
print(f"Potential Frequencies at {refresh_rate}Hz are: {viable_freqs}")
num_freqs = num_locations
median_alpha = 12
flicker_freqs = []

while len(flicker_freqs) < num_freqs:
    diff = np.abs(viable_freqs - median_alpha)
    min_diff_idx = np.argmin(diff)
    flicker_freqs.append(viable_freqs[min_diff_idx])
    viable_freqs = np.delete(viable_freqs, min_diff_idx)

# Compute frames per cycle for each flicker frequency
frames_per_cycle = [round(refresh_rate / freq) for freq in flicker_freqs]
np.random.shuffle(frames_per_cycle)
actual_freqs = [refresh_rate / frames for frames in frames_per_cycle]
print(f"Flicker Freqs: {sorted(flicker_freqs)}")
print(f"Actual Freqs: {sorted(actual_freqs)}")

# Define Pirate class
class Pirate(pygame.sprite.Sprite):
    def __init__(self, image, location, duration):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.duration = duration
        self.location = location
        self.visible = False
        self.frame_count = 0

    def update(self):
        self.frame_count += 1
        flicker_period = self.duration
        self.visible = (self.frame_count % flicker_period) < (flicker_period / 2)

        if self.location is not None:
            self.rect.x = self.location[0] - self.rect.width / 2
            self.rect.y = self.location[1] - self.rect.height / 2

    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect)

# Create pirates with locations and durations
durations = [round(refresh_rate / freq) for freq in actual_freqs]
random.shuffle(durations)
pirates = [Pirate(image, None, duration) for image, duration in zip(pirate_images, durations)]

# Position pirates around a circle
pirate_sprites = pygame.sprite.Group()
for i, pirate in enumerate(pirates):
    angle = 2 * pi * i / num_locations
    x = dist_from_ctr * cos(angle) + screen_width / 2
    y = screen_height / 2 - dist_from_ctr * sin(angle)
    pirate.location = (x, y)
    pirate.update()
    pirate_sprites.add(pirate)

# Main function to handle pirate flickering
def flicker_pirates():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))  # Clear the screen

        pirate_sprites.update()
        for pirate in pirates:
            pirate.draw(screen)
        pygame.display.flip()
        clock.tick(refresh_rate)

if __name__ == "__main__":
    flicker_pirates()
