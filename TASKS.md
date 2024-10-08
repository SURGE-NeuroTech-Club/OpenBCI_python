## Tasks/To-Do's:

_General Updates_
- [ ] Make stim_pres better --> Implement Whack-a-pirate
  - Further apart on screen
- [ ] Test other filtering methods (brainflow?)
- [ ] Try FBCCA/other types of classifier
  - FBCCA ref: https://github.com/NTX-McGill/NeuroTechX-McGill-2021/blob/main/signal/CCA_analysis/predict.py
  - 
- [ ] 



_EEG Data Processing/Classification_
- [X] Get Board data streaming
- [X] Process Data
  - [X] Segment Data
  - [X] Filter [Brainflow/External?] --> **Need to Test!**
- [X] Signal Generation (harmonics) --> Vishal's code
  - [X] Test stacked/unstacked harmonics performance (speed & accuracy)
    - After offline (sim data testing) it seems there is little/no difference in either
- [X] Feature Extraction/Classification [CCA]
  - [ ] Feedback/Output Signal --> do something with the output (also handle exceptions?)


_Signal Elicitation/Presentation Paradigm_
- [X] Make SSVEP paradigm [pygame]
  - [X] Integrate into program
  - [x] Test that we can elicit the inteded SSVEP frequencie(s)
    - Kind of works, maybe!

Notes:
**Cyton Board**: streams data in 24 channels
- 1-8 = EEG
- 9-11 = Accelerometer Channels
- 13+ Aux Channels(?)

**SSVEP Projects w/ Cyton:**
- https://github.com/WATOLINK/mind-speech-interface-ssvep
- https://github.com/NTX-McGill/NeuroTechX-McGill-2021/tree/main

For SSVEP: Oz, O1, O2, pOz, PO3, PO4, Pz (+ reference?)
    --> https://www.researchgate.net/publication/349257316/figure/fig2/AS:990562102571009@1613179817695/a-The-10-10-electrode-placement-system-Bold-10-20-system-b-The-cerebral-lobes-and.ppm

Brainflow has it's own filtering/ML?
- https://brainflow.readthedocs.io/en/stable/UserAPI.html#brainflow-ml-model
- https://brainflow.readthedocs.io/en/stable/UserAPI.html#brainflow-data-filter


## CCA/SSVEP Python Libraries: (other than scikit-learn)
- https://github.com/jameschapman19/cca_zoo
- https://github.com/nbara/python-meegkit
- https://wiki.mentalab.com/applications/ssvep/
- MNE-LSL: https://mne.tools/mne-lsl/stable/api/index.html

- https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0140703&type=printable