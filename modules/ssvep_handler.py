import numpy as np
from mvlearn.embed import CCA
from scipy.signal import welch

class SSVEP_SNR:
    def __init__(self, signal, fs, target_freq, noise_bandwidth=1):
        self.signal = signal
        self.fs = fs
        self.target_freq = target_freq
        self.noise_bandwidth = noise_bandwidth

    def calculate_psd(self):
        freqs, psd = welch(self.signal, self.fs, nperseg=1024)
        return freqs, psd

    def calculate_snr(self):
        freqs, psd = self.calculate_psd()
        target_idx = np.argmin(np.abs(freqs - self.target_freq))
        noise_range = np.logical_and(freqs >= self.target_freq - self.noise_bandwidth, freqs <= self.target_freq + self.noise_bandwidth)
        noise_range[target_idx] = False
        signal_power = psd[target_idx]
        noise_power = np.mean(psd[noise_range])
        snr = 10 * np.log10(signal_power / noise_power)
        return snr

class ClassifySSVEP:
    def __init__(self, frequencies, harmonics, sampling_rate, n_samples, stack_harmonics=True):
        self.frequencies = frequencies
        self.harmonics = harmonics
        self.sampling_rate = sampling_rate
        self.n_samples = n_samples
        self.stack_harmonics = stack_harmonics
        self.reference_signals = self._generate_reference_signals()

    def _generate_reference_signals(self):
        reference_signals = {}
        time = np.linspace(0, self.n_samples / self.sampling_rate, self.n_samples, endpoint=False)
        for freq in self.frequencies:
            signals = []
            for harmon in self.harmonics:
                sine_wave = np.sin(2 * np.pi * harmon * freq * time)
                cosine_wave = np.cos(2 * np.pi * harmon * freq * time)
                signals.append(sine_wave)
                signals.append(cosine_wave)
            if self.stack_harmonics:
                reference_signals[freq] = np.vstack(signals).T
            else:
                reference_signals[freq] = np.array(signals)
        return reference_signals

    def get_reference_signals(self, frequency):
        return self.reference_signals.get(frequency, None)

    def cca_analysis(self, eeg_data):
        cca = CCA(n_components=1)
        max_corr = 0
        target_freq = None

        for freq, ref in self.reference_signals.items():
            if self.stack_harmonics:
                if eeg_data.shape[1] != ref.shape[0]:
                    raise ValueError("EEG data and reference signals must have the same number of samples")
                cca.fit([eeg_data.T, ref])
                U, V = cca.transform([eeg_data.T, ref])
            else:
                U, V = None, None
                if eeg_data.shape[1] != ref.shape[1]:
                    raise ValueError("EEG data and reference signals must have the same number of samples")
                for i in range(ref.shape[0] // 2):
                    cca.fit([eeg_data.T, ref[2*i:2*i+2, :].T])
                    U_tmp, V_tmp = cca.transform([eeg_data.T, ref[2*i:2*i+2, :].T])
                    if U is None:
                        U, V = U_tmp, V_tmp
                    else:
                        U = np.hstack((U, U_tmp))
                        V = np.hstack((V, V_tmp))
            corr = np.corrcoef(U[:, 0], V[:, 0])[0, 1]
            if corr > max_corr:
                max_corr = corr
                target_freq = freq
        return target_freq, max_corr

    def check_snr(self, eeg_data):
        snr_results = {}
        for freq in self.frequencies:
            signal = eeg_data.flatten()  # Assuming eeg_data is 2D: (n_channels, n_samples)
            snr_calculator = SSVEP_SNR(signal, self.sampling_rate, freq)
            snr = snr_calculator.calculate_snr()
            snr_results[freq] = snr
        return snr_results

## Example usage
# if __name__ == "__main__":
#     frequencies = [9.25, 11.25, 13.25]
#     harmonics = np.arange(1, 4)
#     sampling_rate = 256
#     n_samples = 1025

#     # Initialize with stacking harmonics
#     ssvep_harmonics_stacked = ClassifySSVEP(frequencies, harmonics, sampling_rate, n_samples, stack_harmonics=True)

#     # Initialize without stacking harmonics
#     ssvep_harmonics_not_stacked = ClassifySSVEP(frequencies, harmonics, sampling_rate, n_samples, stack_harmonics=False)

#     # Example EEG data (randomly generated for illustration purposes, shape: n_channels, n_samples)
#     eeg_data = np.random.randn(6, n_samples)  # Assuming 6 channels and 1025 samples

#     # Perform CCA analysis with stacked harmonics
#     detected_freq_stacked, correlation_stacked = ssvep_harmonics_stacked.cca_analysis(eeg_data)
#     print(f"Detected frequency with stacked harmonics: {detected_freq_stacked} Hz with correlation: {correlation_stacked}")

#     # Perform CCA analysis without stacking harmonics
#     detected_freq_not_stacked, correlation_not_stacked = ssvep_harmonics_not_stacked.cca_analysis(eeg_data)
#     print(f"Detected frequency without stacked harmonics: {detected_freq_not_stacked} Hz with correlation: {correlation_not_stacked}")
    
    # snr_results = ssvep_harmonics_stacked.check_snr(eeg_data)
    # for freq, snr in snr_results.items():
    #     print(f"Frequency: {freq} Hz, SNR: {snr:.2f} dB")


############
# Without Stacking option - worked tho(?)
############

# import numpy as np
# from mvlearn.embed import CCA

# class ClassifySSVEP:
#     """
#     A class to generate and handle harmonics for SSVEP (Steady-State Visual Evoked Potential) BCI systems.

#     Attributes:
#         frequencies (list): List of target frequencies.
#         harmonics (list): List of harmonics to generate for each frequency.
#         sampling_rate (int): The sampling rate of the EEG data.
#         n_samples (int): The number of samples in the time window for analysis.
#         reference_signals (dict): A dictionary containing the generated reference signals for each frequency.
#     """

#     def __init__(self, frequencies, harmonics, sampling_rate, n_samples):
#         """
#         Initializes the SSVEPHarmonics class with the given parameters.

#         Args:
#             frequencies (list): List of target frequencies.
#             harmonics (list): List of harmonics to generate for each frequency.
#             sampling_rate (int): The sampling rate of the EEG data.
#             n_samples (int): The number of samples in the time window for analysis.
#         """
#         self.frequencies = frequencies
#         self.harmonics = harmonics
#         self.sampling_rate = sampling_rate
#         self.n_samples = n_samples
#         self.reference_signals = self._generate_reference_signals()

#     def _generate_reference_signals(self):
#         """
#         Generates reference signals (sine and cosine waves) for each target frequency and its harmonics.

#         Returns:
#             dict: A dictionary containing the generated reference signals for each frequency.
#         """
#         reference_signals = {}
#         time = np.linspace(0, self.n_samples / self.sampling_rate, self.n_samples, endpoint=False)
#         for freq in self.frequencies:
#             signals = []
#             for harmon in self.harmonics:
#                 sine_wave = np.sin(2 * np.pi * harmon * freq * time)
#                 cosine_wave = np.cos(2 * np.pi * harmon * freq * time)
#                 signals.append(sine_wave)
#                 signals.append(cosine_wave)
#             reference_signals[freq] = np.array(signals).T
#         return reference_signals

#     def get_reference_signals(self, frequency):
#         """
#         Retrieves the reference signals for a given frequency.

#         Args:
#             frequency (float): The target frequency.

#         Returns:
#             np.ndarray: The reference signals for the given frequency.
#         """
#         return self.reference_signals.get(frequency, None)


#     def cca_analysis(self, eeg_data):
#         """
#         Performs Canonical Correlation Analysis (CCA) to identify the target frequency the user is focusing on.

#         Args:
#             eeg_data (np.ndarray): The EEG data to be analyzed.
        
#         Returns:
#             predicted target frequency and maximum correlation
#         """
#         cca = CCA(n_components=1) #, regs=0.1)
#         max_corr = 0
#         target_freq = None

#         for freq, ref in self.reference_signals.items():
#             cca.fit([eeg_data.T, ref])
#             U, V = cca.transform([eeg_data.T, ref])
#             corr = np.corrcoef(U[:, 0], V[:, 0])[0, 1]
#             if corr > max_corr:
#                 max_corr = corr
#                 target_freq = freq
#         return target_freq, max_corr


#     # def cca_analysis(self, eeg_data):
#     #     """
#     #     Performs Canonical Correlation Analysis (CCA) to identify the target frequency the user is focusing on.

#     #     Args:
#     #         eeg_data (np.ndarray): The EEG data to be analyzed.

#     #     Returns:
#     #         tuple: The detected frequency and the corresponding correlation value.
#     #     """
#     #     cca = CCA(n_components=1)
#     #     max_corr = 0
#     #     target_freq = None
#     #     for freq, ref in self.reference_signals.items():
#     #         cca.fit([eeg_data, ref])
#     #         U, V = cca.transform([eeg_data, ref])
#     #         corr = np.corrcoef(U[:, 0], V[:, 0])[0, 1]
#     #         if corr > max_corr:
#     #             max_corr = corr
#     #             target_freq = freq
#     #     return target_freq, max_corr


# ## Example usage
# # if __name__ == "__main__":
# #     frequencies = [9.25, 11.25, 13.25]
# #     harmonics = np.arange(1, 4)
# #     sampling_rate = 256
# #     n_samples = 1025

# #     ssvep_harmonics = SSVEPHarmonics(frequencies, harmonics, sampling_rate, n_samples)

# #     # Example EEG data (randomly generated for illustration purposes)
# #     eeg_data = np.random.randn(n_samples, len(frequencies))

# #     # Perform CCA analysis
# #     detected_freq, correlation = ssvep_harmonics.cca_analysis(eeg_data)
# #     print(f"Detected frequency: {detected_freq} Hz with correlation: {correlation}")
