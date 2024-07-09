import pygame
import sys
import math
import time

class SSVEPStimulus:
    """
    Class to handle the stimulus presentation paradigm for an SSVEP BCI system using flickering boxes.
    
    Attributes:
        boxes (list): A list of dictionaries containing box properties (position, flickering frequency, and text/symbol).
        screen (pygame.Surface): The Pygame screen surface.
        screen_width (int): The width of the screen.
        screen_height (int): The height of the screen.
        background_color (pygame.Color): The background color of the screen.
        box_color (pygame.Color): The color of the boxes.
        start_button (pygame.Rect): The start button rectangle.
        start_button_color (pygame.Color): The color of the start button.
        start_text (pygame.Surface): The text surface for the start button.
        start (bool): Flag to start the flickering boxes.
    """

    def __init__(self, box_frequencies, box_texts=None, box_text_indices=None, show_both=False, screen_resolution=None):
        """
        Initializes the SSVEPStimulus class.
        
        Args:
            box_frequencies (list): List of flickering frequencies for the boxes.
            box_texts (list, optional): List of texts or symbols to display on the boxes. Defaults to None.
            box_text_indices (list, optional): List of indices specifying which boxes display the texts. Defaults to None.
            show_both (bool, optional): Flag to show both box_text and frequency. Defaults to False.
            screen_resolution (tuple, optional): Screen resolution (width, height). Defaults to None (fullscreen).
        """
        if box_texts and len(box_texts) != len(box_text_indices):
            raise ValueError("The length of box_texts and box_text_indices must be the same if box_texts is provided.")
        
        pygame.init()
        
        if screen_resolution:
            self.screen = pygame.display.set_mode(screen_resolution)
        else:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        
        self.screen_width, self.screen_height = self.screen.get_size()
        pygame.display.set_caption("Flickering Boxes")
        
        sorted_indices = sorted(range(len(box_frequencies)), key=lambda i: box_frequencies[i])
        interleaved_indices = []

        # Interleave frequencies to maximize distance between similar frequencies
        left = 0
        right = len(sorted_indices) - 1
        while left <= right:
            if left == right:
                interleaved_indices.append(sorted_indices[left])
            else:
                interleaved_indices.append(sorted_indices[left])
                interleaved_indices.append(sorted_indices[right])
            left += 1
            right -= 1

        self.boxes = [{"rect": pygame.Rect(0, 0, 150, 150), "frequency": box_frequencies[i], "text": None} for i in interleaved_indices]
        
        if box_texts and box_text_indices:
            for text, idx in zip(box_texts, box_text_indices):
                self.boxes[idx]["text"] = text
        
        self.background_color = pygame.Color('black')
        self.box_color = pygame.Color('white')
        
        self.start_button = pygame.Rect(self.screen_width // 2 - 50, self.screen_height // 2 - 25, 100, 50)
        self.start_button_color = pygame.Color('green')
        self.start_text = pygame.font.Font(None, 36).render('Start', True, pygame.Color('white'))
        self.start = False
        
        self.font = pygame.font.Font(None, 36)  # Font for displaying frequencies and texts/symbols
        self.show_both = show_both  # Flag to show both text and frequency

    def run(self):
        """
        Runs the main loop to handle the stimulus presentation.
        """
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
                
                centerX, centerY = self.screen_width // 2, self.screen_height // 2
                radius = min(self.screen_width, self.screen_height) // 3
                num_boxes = len(self.boxes)
                
                for i, box in enumerate(self.boxes):
                    angle = 2 * math.pi * i / num_boxes
                    box["rect"].center = (centerX + int(radius * math.cos(angle)), centerY + int(radius * math.sin(angle)))
                    
                    if math.sin(current_time * box["frequency"] * math.pi) > 0:
                        pygame.draw.rect(self.screen, self.box_color, box["rect"])
                        if self.show_both and box["text"]:
                            # Display both text and frequency
                            text_surface = self.font.render(box["text"], True, pygame.Color('black'))
                            text_rect = text_surface.get_rect(center=(box["rect"].centerx, box["rect"].centery - 10))
                            self.screen.blit(text_surface, text_rect)
                            
                            frequency_text = self.font.render(f"{box['frequency']} Hz", True, pygame.Color('black'))
                            frequency_rect = frequency_text.get_rect(center=(box["rect"].centerx, box["rect"].centery + 20))
                            self.screen.blit(frequency_text, frequency_rect)
                        else:
                            display_text = box["text"] if box["text"] else f"{box['frequency']} Hz"
                            text_surface = self.font.render(display_text, True, pygame.Color('black'))
                            text_rect = text_surface.get_rect(center=box["rect"].center)
                            self.screen.blit(text_surface, text_rect)

            pygame.display.flip()
            pygame.time.wait(10)

        pygame.quit()
        sys.exit()

## Example usage
# if __name__ == "__main__":
#     box_frequencies = [8, 10, 12, 14]  # List of frequencies
#     box_texts = ["A", "B", "C", "D"]  # List of texts or symbols
#     box_text_indices = [0, 1, 2, 3]  # Indices where the texts should be displayed
#     stimulus = SSVEPStimulus(box_frequencies, box_texts, box_text_indices, show_both=True)
#     stimulus.run()
