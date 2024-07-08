# from modules.stream_data import *
from modules.preprocessing import *
from modules.classification import *
from modules.maintenence import *
from modules.stream_data import *

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets
from pynput import keyboard

## Adjust As Necessary
serial_port = 'COM4' #Looks different on MAC/Linux -> "/dev/tty*"
# Other Boards: https://brainflow.readthedocs.io/en/stable/UserAPI.html#brainflow-board-shim
board_id = BoardIds.SYNTHETIC_BOARD #BoardIds.CYTON_BOARD
segment_duration = 4 # seconds

def main():        
    
    ## Listening for `esc` key to exit
    key_listener = KeyListener()
    key_listener.run_listener()

    ## Initializing Board  
    board = BrainFlowBoardSetup(board_id, serial_port)
    # board.show_params()
    board.setup()
            
    ## Get Stream Information
    sampling_rate = BoardShim.get_sampling_rate(board_id)
    eeg_channels = BoardShim.get_eeg_channels(board_id)
    print(f"Sampling Rate: {sampling_rate}")
    print(f"Channels: {eeg_channels}")
    
    # Letting 5 seconds of data accumulate
    print(f"Letting Samples Accumulate....")
    time.sleep(5)
    
    # Reading Data
    # data = board.get_board_data()
    data = board.get_current_board_data(num_samples=1250)
    print(f"Collected data shape: {data.shape}")
    print(f"(Channels, Samples)")
    
    ## Initializing Segmenter Class
    segmenter = PreProcess(board, segment_duration=segment_duration)
    
    # # Initialize CCAModel
    # cca_model = CCAModel(n_components=2)

    # # Example training data (replace with actual preprocessed training data)
    # X_train = np.random.randn(100, 64)  # 100 samples, 64 features
    # Y_train = np.random.randint(0, 2, 100)  # Binary labels for the training data

    # # Fit the CCA model and classifier
    # cca_model.fit(X_train, Y_train)

    try:
        while not key_listener.stop_flag:
            # Step 1: Get a segment of data
            segment = segmenter.get_segment()
            if segment is not None:
                print(f"Segment shape: {segment.shape}")

                # Step 2: Filter the data
                filtered_data = segmenter.filter_data(segment)
                print("Filtered data shape:", filtered_data.shape)

                # Step 3: Extract features
                # features = segmenter.extract_features(filtered_data)
                # print("Extracted features shape:", features.shape)

                # Step 4: Classify the features
                # prediction = cca_model.predict(features)
                # print("Prediction:", prediction)

                # Optionally save or process the data further
                # segmenter.save_data(filtered_data, "filtered_data.csv")
                # segmenter.save_data(features, "features.csv")

            # Sleep for a while to collect new data
            time.sleep(segmenter.segment_duration)

    except KeyboardInterrupt:
        pass

    finally:
        board.stop()
        print("\nSession Exited Successfully\n")
     
    
    # try:
    #     while True:
    #         # Step 1: Get a segment of data
    #         segment = segmenter.get_segment()
    #         if segment is not None:
    #             print(f"Segment shape: {segment.shape}")

    #             # Step 2: Filter the data
    #             filtered_data = segmenter.filter_data(segment)
    #             print("Filtered data shape:", filtered_data.shape)

    #             # Step 3: Extract features
    #             features = segmenter.extract_features(filtered_data)
    #             print("Extracted features shape:", features.shape)

    #         # Sleep for a while to collect new data
    #         time.sleep(segmenter.segment_duration)

    # except KeyboardInterrupt:
    #     # Handle any cleanup here
    #     board_controller.stop_streaming()
    #     print("Streaming stopped.")
    
    

if __name__ == "__main__":
    main()