# Tasks/To-Do's:

The goal of this repo/library is to make a toolkit for making SSVEP/ERP-based brain-computer interfaces accessible for those who don't have much/any experience.

## Goals:

The outline & functionality is split into categories related to different aspects of BCI's

**Signal Aquisition/Hardware Interfacing:**
- [ ] Support for OpenBCI Cyton Board
- [ ] Support for Unicorn
- [ ] Stream data

**Signal Processing:**
- [ ] Filters:
  - [ ] Bandpass
- [ ] Epoching/Segmenting
- [ ] 

**Classification:**
- SSVEP:
  - [ ] CCA
  - [ ] FBCCA
- ERP:
  - [ ] Training data handler
  - [ ] LDA
  - [ ] SVM

**Stimulus Presentation:**
- [X] SSVEP (working)
  - [ ] 
- [ ] Oddball(?)

**Output:**
- [ ] Output hooks
  - Easy way for the classifier output to be hooked into performing tasks/executing commands (i.e., the 'computer' part)

**Examples/Tutorials:**
1. [ ] Data aquisition 
2. [ ] Filtering
3. [ ] Stimulus Presentation 
4. [ ] Classifier

# Notes:

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