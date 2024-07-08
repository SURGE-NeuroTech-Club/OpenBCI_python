import threading
from pynput import keyboard

class KeyListener:
    def __init__(self):
        self.stop_flag = False

    def on_press(self, key):
        if key == keyboard.Key.esc:
            self.stop_flag = True
            return False  # Stop listener

    def start_listener(self):
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()
        listener.join()  # Ensure the listener thread waits for key press

    def run_listener(self):
        listener_thread = threading.Thread(target=self.start_listener)
        listener_thread.start()
