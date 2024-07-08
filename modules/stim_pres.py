import pygame
import sys
import math
import time

class SSVEPStimulus:
    def __init__(self, box_frequencies, screen_resolution=None):
        pygame.init()
        
        if screen_resolution:
            self.screen = pygame.display.set_mode(screen_resolution)
        else:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        
        self.screen_width, self.screen_height = self.screen.get_size()
        pygame.display.set_caption("Flickering Boxes")
        
        self.boxes = [
            {"rect": pygame.Rect(300, 100, 200, 150), "frequency": box_frequencies[0]},
            {"rect": pygame.Rect(300, 100, 200, 150), "frequency": box_frequencies[1]},
            {"rect": pygame.Rect(300, 100, 200, 150), "frequency": box_frequencies[2]},
            {"rect": pygame.Rect(300, 100, 200, 150), "frequency": box_frequencies[3]},
        ]
        
        self.background_color = pygame.Color('black')
        self.box_color = pygame.Color('white')
        
        self.start_button = pygame.Rect(self.screen_width // 2 - 50, self.screen_height // 2 - 25, 100, 50)
        self.start_button_color = pygame.Color('green')
        self.start_text = pygame.font.Font(None, 36).render('Start', True, pygame.Color('white'))
        self.start = False
        
        self.font = pygame.font.Font(None, 36)  # Font for displaying frequencies

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.collidepoint(event.pos):
                        self.start = True

            self.screen.fill(self.background_color)

            if not self.start:
                pygame.draw.rect(self.screen, self.start_button_color, self.start_button)
                self.screen.blit(self.start_text, (self.start_button.x + 10, self.start_button.y + 10))
            else:
                current_time = time.time()
                edge_offset = 100
                box_size = 150
                offset = 300
                centerX, centerY = self.screen_width // 2, self.screen_height // 2

                self.boxes[0]["rect"].center = (centerX, centerY - offset)
                self.boxes[2]["rect"].center = (centerX, centerY + offset)
                self.boxes[3]["rect"].center = (edge_offset + box_size // 2, centerY)
                self.boxes[1]["rect"].center = (self.screen_width - edge_offset - box_size // 2, centerY)

                for box in self.boxes:
                    if math.sin(current_time * box["frequency"] * math.pi) > 0:
                        pygame.draw.rect(self.screen, self.box_color, box["rect"])
                        frequency_text = self.font.render(f"{box['frequency']} Hz", True, pygame.Color('black'))
                        text_rect = frequency_text.get_rect(center=box["rect"].center)
                        self.screen.blit(frequency_text, text_rect)

            pygame.display.flip()
            pygame.time.wait(10)

        pygame.quit()
        sys.exit()




# import pygame
# import sys
# import math
# import time

# class SSVEPStimulus:
#     """
#     Class to handle the stimulus presentation paradigm for an SSVEP BCI system using flickering boxes.
    
#     Attributes:
#         boxes (list): A list of dictionaries containing box properties (position and flickering frequency).
#         screen (pygame.Surface): The Pygame screen surface.
#         screen_width (int): The width of the screen.
#         screen_height (int): The height of the screen.
#         background_color (pygame.Color): The background color of the screen.
#         box_color (pygame.Color): The color of the boxes.
#         start_button (pygame.Rect): The start button rectangle.
#         start_button_color (pygame.Color): The color of the start button.
#         start_text (pygame.Surface): The text surface for the start button.
#         start (bool): Flag to start the flickering boxes.
#     """

#     def __init__(self, box_frequencies, screen_resolution=None):
#         """
#         Initializes the SSVEPStimulus class.
        
#         Args:
#             box_frequencies (list): List of flickering frequencies for the boxes.
#             screen_resolution (tuple, optional): Screen resolution (width, height). Defaults to None (fullscreen).
#         """
#         # Initialize Pygame
#         pygame.init()
        
#         # Full screen or set resolution
#         if screen_resolution:
#             self.screen = pygame.display.set_mode(screen_resolution)
#         else:
#             self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        
#         self.screen_width, self.screen_height = self.screen.get_size()
#         pygame.display.set_caption("Flickering Boxes")
        
#         # Box properties
#         self.boxes = [
#             {"rect": pygame.Rect(300, 100, 200, 150), "frequency": box_frequencies[0]}, # Top
#             {"rect": pygame.Rect(300, 100, 200, 150), "frequency": box_frequencies[1]}, # Bottom
#             {"rect": pygame.Rect(300, 100, 200, 150), "frequency": box_frequencies[2]}, # Left
#             {"rect": pygame.Rect(300, 100, 200, 150), "frequency": box_frequencies[3]}, # Right
#         ]
        
#         self.background_color = pygame.Color('black')
#         self.box_color = pygame.Color('white')
        
#         # Start button properties
#         self.start_button = pygame.Rect(self.screen_width // 2 - 50, self.screen_height // 2 - 25, 100, 50)
#         self.start_button_color = pygame.Color('green')
#         self.start_text = pygame.font.Font(None, 36).render('Start', True, pygame.Color('white'))
#         self.start = False  # Flickering doesn't start until the button is pressed

#     def run(self):
#         """
#         Runs the main loop to handle the stimulus presentation.
#         """
#         # Main game loop
#         running = True
#         while running:
#             # Event handling
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False
#                 elif event.type == pygame.KEYDOWN:  # Check for key presses
#                     if event.key == pygame.K_ESCAPE:  # Exit on Esc
#                         running = False
#                 elif event.type == pygame.MOUSEBUTTONDOWN:
#                     if self.start_button.collidepoint(event.pos):
#                         self.start = True  # Start flickering when the start button is clicked

#             # Clear screen
#             self.screen.fill(self.background_color)

#             if not self.start:
#                 # Draw start button
#                 pygame.draw.rect(self.screen, self.start_button_color, self.start_button)
#                 self.screen.blit(self.start_text, (self.start_button.x + 10, self.start_button.y + 10))
#             else:
#                 # Current time
#                 current_time = time.time()

#                 # Calculate positions for diamond pattern near the edges of the screen
#                 edge_offset = 100  # Distance from the edge of the screen to the box
#                 # Assuming each box is 150x150 pixels
#                 box_size = 150
                
#                 offset = 300  # Distance from the center to the box's center in the diamond pattern

#                 # Calculate the center of the screen
#                 centerX, centerY = self.screen_width // 2, self.screen_height // 2

#                 # Adjust positions for the top and bottom boxes to be in the diamond pattern
#                 # Top box
#                 self.boxes[0]["rect"].center = (centerX, centerY - offset)  
#                 # Bottom box
#                 self.boxes[2]["rect"].center = (centerX, centerY + offset)  
#                 # Left box
#                 self.boxes[3]["rect"].center = (edge_offset + box_size // 2, centerY)
#                 # Right box
#                 self.boxes[1]["rect"].center = (self.screen_width - edge_offset - box_size // 2, centerY)

#                 # Draw boxes based on their flickering state
#                 for box in self.boxes:
#                     if math.sin(current_time * box["frequency"] * math.pi) > 0:
#                         pygame.draw.rect(self.screen, self.box_color, box["rect"])

#             # Update display
#             pygame.display.flip()

#             # Control frame rate
#             pygame.time.wait(10)

#         # Clean up and exit
#         pygame.quit()
#         sys.exit()

# # Example usage
# # if __name__ == "__main__":
# #     box_frequencies = [8, 10, 12, 14]
# #     stimulus = SSVEPStimulus(box_frequencies)
# #     stimulus.run()
