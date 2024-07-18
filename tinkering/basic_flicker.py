import pygame
import sys
import math
import time

# Initialize Pygame
pygame.init()

# Full screen setup
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
pygame.display.set_caption("Flickering Boxes")

# Box properties
boxes = [
    {"rect": pygame.Rect(300, 100, 200, 150), "frequency": 8}, # Top
    {"rect": pygame.Rect(300, 100, 200, 150), "frequency": 10}, # Bottm
    {"rect": pygame.Rect(300, 100, 200, 150), "frequency": 12}, # Left
    {"rect": pygame.Rect(300, 100, 200, 150), "frequency": 14}, # Right
]
background_color = pygame.Color('black')
box_color = pygame.Color('white')

# Start button properties
start_button = pygame.Rect(screen_width // 2 - 50, screen_height // 2 - 25, 100, 50)
start_button_color = pygame.Color('green')
start_text = pygame.font.Font(None, 36).render('Start', True, pygame.Color('white'))
start = False  # Flickering doesn't start until the button is pressed

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:  # Check for key presses
            if event.key == pygame.K_ESCAPE:  # Exit on Esc
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                start = True  # Start flickering when the start button is clicked

    # Clear screen
    screen.fill(background_color)

    if not start:
        # Draw start button
        pygame.draw.rect(screen, start_button_color, start_button)
        screen.blit(start_text, (start_button.x + 10, start_button.y + 10))
    else:
        # Current time
        current_time = time.time()

        # Calculate positions for diamond pattern near the edges of the screen
        edge_offset = 100  # Distance from the edge of the screen to the box
        # Assuming each box is 150x150 pixels
        box_size = 150
        
        offset = 300  # Distance from the center to the box's center in the diamond pattern

        # Calculate the center of the screen
        centerX, centerY = screen_width // 2, screen_height // 2

        # Adjust positions for the top and bottom boxes to be in the diamond pattern
        # Top box
        boxes[0]["rect"].center = (centerX, centerY - offset)  
        # Bottom box
        boxes[2]["rect"].center = (centerX, centerY + offset)  
        # Left box
        boxes[3]["rect"].center = (edge_offset + box_size // 2, centerY)
        # Right box
        boxes[1]["rect"].center = (screen_width - edge_offset - box_size // 2, centerY)

        # Draw boxes based on their flickering state
        for box in boxes:
            if math.sin(current_time * box["frequency"] * math.pi) > 0:
                pygame.draw.rect(screen, box_color, box["rect"])

    # Update display
    pygame.display.flip()

    # Control frame rate
    pygame.time.wait(10)

# Clean up and exit
pygame.quit()
sys.exit()