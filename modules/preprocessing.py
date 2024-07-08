import time
import numpy as np
from brainflow.board_shim import BoardShim
from scipy.signal import butter, lfilter

class PreProcess:
    def __init__(self, board, segment_duration):
        self.board = board
        self.segment_duration = segment_duration
        self.sampling_rate = BoardShim.get_sampling_rate(self.board.board_id)
        self.buffer_size = self.sampling_rate * self.segment_duration

    def segment(self):
        while True:
            data = self.board.get_current_board_data(self.buffer_size)
            
            # Check if we have enough data for a full segment
            if data.shape[1] >= self.buffer_size:
                # Extract the latest segment
                segment = data[:, -self.buffer_size:]
                
                # Process the segment (e.g., print or save it)
                print(f"Segment shape: {segment.shape}")
                print(segment)
            
            # Sleep for a while to collect new data
            time.sleep(self.segment_duration)
    
    def get_segment(self):
        data = self.board.get_current_board_data(self.buffer_size)
        if data.shape[1] >= self.buffer_size:
            segment = data[:, -self.buffer_size:]
            return segment
        return None

    def filter_data(self, data):
        lowcut = 0.5  # Example low cut frequency in Hz
        highcut = 30.0  # Example high cut frequency in Hz
        filtered_data = np.apply_along_axis(self.bandpass_filter, 1, data, lowcut, highcut, self.sampling_rate)
        return filtered_data

    def bandpass_filter(self, data, lowcut, highcut, fs, order=5):
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype='band')
        y = lfilter(b, a, data)
        return y

    def extract_features(self, data):
        # Example feature extraction: Mean and standard deviation
        features = np.vstack((data.mean(axis=1), data.std(axis=1))).T
        return features

    def save_data(self, data, filename):
        np.savetxt(filename, data, delimiter=',')
        
        
        
               
           
           
            
    # def process_segment(self, segment):
    #     print(f"Segment shape: {segment.shape}")
    #     filtered_data = self.filter_data(segment)
    #     features = self.extract_features(filtered_data)
    #     print("Filtered data:", filtered_data)
    #     print("Extracted features:", features)

    # def filter_data(self, data):
    #     lowcut = 0.5  # Example low cut frequency in Hz
    #     highcut = 30.0  # Example high cut frequency in Hz
    #     filtered_data = np.apply_along_axis(bandpass_filter, 1, data, lowcut, highcut, self.sampling_rate)
    #     return filtered_data

    # def butter_bandpass(lowcut, highcut, fs, order=5):
    #     nyquist = 0.5 * fs
    #     low = lowcut / nyquist
    #     high = highcut / nyquist
    #     b, a = butter(order, [low, high], btype='band')
    #     return b, a

    # def bandpass_filter(data, lowcut, highcut, fs, order=5):
    #     b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    #     y = lfilter(b, a, data)
    #     return y

    # def extract_features(self, data):
    #     features = data.mean(axis=1)
    #     return features

    # def save_data(self, data, filename):
    #     np.savetxt(filename, data, delimiter=',')



