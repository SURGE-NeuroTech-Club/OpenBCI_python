# Online SSVEP 

This repository holds code for using the brainflow library with an OpenBCI Cyton board to make a real-time (online) steady-state visually evoked potential (SSVEP) brain-computer interface (BCI) demo.

`main.py`: the online BCI system

*Modules/*: Each file should contain documentation on classes & functions
- `stream_data.py`: A custom class that uses the brainflow library to connect and stream from the Cyton Board
- `preprocessing.py`: Class that contains functions to segment, filter, and save data
- `ssvep_handler.py`: Classes that generate harmonics and uses canonical correlation analysis (CCA) to classify SSVEP data, and functions that perform and return signal-to-noise ratio (SNR)
- `stim_pres.py`: Code related to stimulus presentation (i.e., flickering stimuli to elicit SSVEP)
- `maintenence.py`: Code related to listening for the 'esc' key and raising stop flags

*Other:*
- `sim_ssvep_data.npy`: simulated SSVEP data in shape (8, 15000) 
  - 8 channels, 15000 samples (60 seconds at 250 Hz Sample Rate)
  - Simulated SSVEP signal changes between [9.25, 11.25, 13.25, 15.25] Hz every 10 seconds

## Links/Reference

LSL:
- https://docs.openbci.com/Software/CompatibleThirdPartySoftware/LSL/
- https://github.com/openbci-archive/OpenBCI_LSL

Brainflow
- https://brainflow.readthedocs.io/en/stable/Examples.html#python
- https://brainflow.readthedocs.io/en/stable/UserAPI.html#python-api-reference