from psychopy import visual, event, core, monitors
import numpy as np

class SSVEPStimulus:
    """
    Class to handle the stimulus presentation paradigm for an SSVEP BCI system using flickering boxes.
    
    Attributes:
        win (visual.Window): The PsychoPy window where stimuli are presented.
        refresh_rate (float): The refresh rate of the display in Hz.
        actual_frequencies (list of float): The list of actual frequencies that can be displayed given the refresh rate.
        boxes (list of dict): A list of dictionaries, each containing the box stimulus and its related properties.
        start (bool): Flag indicating whether the stimulus presentation has started.
        frame_count (int): Counter for the number of frames elapsed.
    """

    def __init__(self, box_frequencies, refresh_rate=None, box_texts=None, box_text_indices=None, show_both=False, display_index=0):
        """
        Initializes the SSVEPStimulus class.

        Args:
            box_frequencies (list of float): Desired frequencies for the flickering boxes.
            refresh_rate (float, optional): The refresh rate of the screen. If None, the rate will be measured.
            box_texts (list of str, optional): Texts or symbols to display on the boxes.
            box_text_indices (list of int, optional): Indices indicating which boxes should display text.
            show_both (bool, optional): If True, both the frequency and text will be displayed on the boxes.
            display_index (int, optional): Index of the display screen to use.
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

        # Calculate actual frequencies that can be shown given the refresh rate
        self.actual_frequencies = self.calculate_actual_frequencies(box_frequencies)
        print(f"Actual Frequencies: {self.actual_frequencies}")

        # Sort and interleave the indices of the boxes to maximize the distance between similar frequencies
        sorted_indices = sorted(range(len(self.actual_frequencies)), key=lambda i: self.actual_frequencies[i])
        interleaved_indices = []

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
        num_boxes = len(self.actual_frequencies)

        for i, idx in enumerate(interleaved_indices):
            angle = 2 * np.pi * i / num_boxes
            pos = (centerX + int(radius * np.cos(angle)), centerY + int(radius * np.sin(angle)))

            box = visual.Rect(win=win, width=150, height=150, fillColor='white', lineColor='white', pos=pos)
            frequency_text = f"{self.actual_frequencies[idx]:.2f} Hz"
            text_stim = visual.TextStim(win=win, text=frequency_text, color='black', pos=pos)
            
            # Adjust text position if both box_text and frequency are shown
            if self.show_both and self.box_texts and idx in box_text_indices:
                box_text = box_texts[box_text_indices.index(idx)]
                box_text_stim = visual.TextStim(win=win, text=box_text, color='black', pos=(pos[0], pos[1] + 30))
                self.boxes.append({
                    "box": box,
                    "frequency": self.actual_frequencies[idx],
                    "text": text_stim,
                    "box_text": box_text_stim,
                    "frame_count": 0,
                    "on": True  # Track whether the box is on or off
                })
            else:
                self.boxes.append({
                    "box": box,
                    "frequency": self.actual_frequencies[idx],
                    "text": text_stim,
                    "box_text": None,
                    "frame_count": 0,
                    "on": True  # Track whether the box is on or off
                })
        
        self.start = False
        self.start_button = visual.Rect(win=win, width=100, height=50, fillColor='green', pos=(0, 0))
        self.start_text = visual.TextStim(win=win, text='Press Space/Enter to Start', color='white', pos=(0, 0))

    def measure_refresh_rate(self, n_frames=60):
        """
        Measure the screen refresh rate by timing the rendering of a number of frames.

        Args:
            n_frames (int): The number of frames to render for measuring the refresh rate.

        Returns:
            float: The measured refresh rate in Hz.
        """
        clock = core.Clock()
        for _ in range(n_frames):
            self.win.flip()
        duration = clock.getTime()
        return n_frames / duration

    def calculate_actual_frequencies(self, desired_frequencies):
        """
        Calculate the actual frequencies that can be shown given the measured refresh rate.

        Args:
            desired_frequencies (list of float): The desired frequencies for the flickering boxes.

        Returns:
            list of float: The actual frequencies that can be achieved given the screen's refresh rate.
        """
        actual_frequencies = []
        for freq in desired_frequencies:
            frames_per_cycle = round(self.refresh_rate / freq)
            actual_freq = self.refresh_rate / frames_per_cycle
            actual_frequencies.append(actual_freq)
        return actual_frequencies

    def run(self):
        """
        Runs the main loop to handle the stimulus presentation.
        
        The loop waits for a key press (space/enter) to start the stimulus presentation. Once started,
        the boxes will flicker at their assigned frequencies. The loop will continue until the escape key is pressed.
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
                            box["text"].setAutoDraw(True)
                            if box["box_text"]:
                                box["box_text"].setAutoDraw(True)
                    else:
                        if box["on"]:
                            box["on"] = False
                            box["box"].setAutoDraw(False)
                            box["text"].setAutoDraw(False)
                            if box["box_text"]:
                                box["box_text"].setAutoDraw(False)

            self.win.flip()
        
        self.win.close()
        core.quit()
 
# Example usage
if __name__ == "__main__":
    box_frequencies = [7.8, 8, 8.5, 10.5, 12.2, 16, 16.5]  # List of desired frequencies
    box_texts = ["A", "B", "C"]  # List of texts or symbols
    box_text_indices = [0, 2, 4]  # Indices where the texts should be displayed
    refresh_rate = None  # Let the script measure the refresh rate

    stimulus = SSVEPStimulus(box_frequencies, refresh_rate=refresh_rate, box_texts=box_texts, box_text_indices=box_text_indices, show_both=True, display_index=0)
    stimulus.run()
