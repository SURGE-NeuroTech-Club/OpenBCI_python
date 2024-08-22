from psychopy import visual, event, core, monitors
import numpy as np

class SSVEPStimulus:
    """
    Class to handle the stimulus presentation paradigm for an SSVEP BCI system using flickering boxes.
    """

    def __init__(self, box_frequencies, refresh_rate=None, box_texts=None, box_text_indices=None, show_both=False, display_index=0):
        """
        Initializes the SSVEPStimulus class.
        """
        if box_texts and len(box_texts) != len(box_text_indices):
            raise ValueError("The length of box_texts and box_text_indices must be the same if box_texts is provided.")
        
        # Setup monitor and window
        monitor = monitors.Monitor(name='testMonitor')  # Change as appropriate
        
        win = visual.Window(
            monitor=monitor, 
            screen=display_index, 
            fullscr=True, 
            color='black', 
            units='pix', 
            allowGUI=False, 
            winType='pyglet',
            autoLog=False
        )

        self.win = win

        # Measure screen refresh rate
        self.refresh_rate = self.measure_refresh_rate() if refresh_rate is None else refresh_rate
        print(f"Measured Refresh Rate: {self.refresh_rate:.2f} Hz")
        
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

        # Create boxes and assign frequencies
        self.boxes = []
        self.box_texts = box_texts
        self.show_both = show_both
        self.frame_count = 0
        
        centerX, centerY = 0, 0  # Center of the screen
        radius = min(win.size) // 3  # Radius for circular placement
        num_boxes = len(box_frequencies)

        for i in interleaved_indices:
            angle = 2 * np.pi * i / num_boxes
            pos = (centerX + int(radius * np.cos(angle)), centerY + int(radius * np.sin(angle)))

            box = visual.Rect(win=win, width=150, height=150, fillColor='white', lineColor='white', pos=pos)
            text_stim = visual.TextStim(win=win, text=str(box_frequencies[i]), color='black', pos=pos)
            
            self.boxes.append({
                "box": box,
                "frequency": box_frequencies[i],
                "text": text_stim,
                "frame_count": 0,
                "on": True  # Track whether the box is on or off
            })
        
        self.start = False
        self.start_button = visual.Rect(win=win, width=100, height=50, fillColor='green', pos=(0, 0))
        self.start_text = visual.TextStim(win=win, text='Press Space/Enter to Start', color='white', pos=(0, 0))

    def measure_refresh_rate(self, n_frames=60):
        """
        Measure the screen refresh rate by timing the rendering of a number of frames.
        """
        clock = core.Clock()
        for _ in range(n_frames):
            self.win.flip()
        duration = clock.getTime()
        return n_frames / duration

    def run(self):
        """
        Runs the main loop to handle the stimulus presentation.
        """
        while True:
            keys = event.getKeys()
            if 'escape' in keys:
                break
            elif 'space' in keys or 'return' in keys:
                self.start = True
            
            mouse = event.Mouse(visible=False, win=self.win)
            if not self.start:
                self.start_button.draw()
                self.start_text.draw()
            else:
                self.frame_count += 1
                for box in self.boxes:
                    flicker_period = self.refresh_rate / box["frequency"]
                    # Flip the state at the right time using frame counting
                    if (self.frame_count % flicker_period) < (flicker_period / 2):
                        if not box["on"]:
                            box["on"] = True
                            box["box"].setAutoDraw(True)
                    else:
                        if box["on"]:
                            box["on"] = False
                            box["box"].setAutoDraw(False)

                    if self.show_both and self.box_texts:
                        box["text"].draw()

            self.win.flip()
        
        self.win.close()
        core.quit()

# Example usage
if __name__ == "__main__":
    box_frequencies = [8, 10, 12, 14, 16, 18]  # List of frequencies
    box_texts = ["A", "B", "C"]  # List of texts or symbols
    box_text_indices = [0, 2, 4]  # Indices where the texts should be displayed
    refresh_rate = None  # Let the script measure the refresh rate

    stimulus = SSVEPStimulus(box_frequencies, refresh_rate=refresh_rate, box_texts=box_texts, box_text_indices=box_text_indices, show_both=True, display_index=0)
    stimulus.run()
