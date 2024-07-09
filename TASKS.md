## Tasks/To-Do's:

_EEG Data Processing/Classification_
- [X] Get Board data streaming
- [ ] Process Data
  - [X] Segment Data
  - [ ] Filter [Brainflow/External?] --> **Need to Test!**
- [X] Signal Generation (harmonics) --> Vishal's code
  - [ ] Test stacked/unstacked harmonics performance (speed & accuracy)
- [ ] Feature Extraction/Classification [CCA]
  - [ ] Feedback/Output Signal [loops into function]
- [ ] Adjust to use Tensors for processing steps?

_Signal Elicitation/Presentation Paradigm_
- [X] Make SSVEP paradigm [pygame]
  - [X] Integrate into program
  - [ ] Test that we can elicit the inteded SSVEP frequencie(s)




For SSVEP: Oz, O1, O2, pOz, PO3, PO4, Pz (+ reference?)
    --> https://www.researchgate.net/publication/349257316/figure/fig2/AS:990562102571009@1613179817695/a-The-10-10-electrode-placement-system-Bold-10-20-system-b-The-cerebral-lobes-and.ppm

Brainflow has it's own filtering/ML?
- https://brainflow.readthedocs.io/en/stable/UserAPI.html#brainflow-ml-model
- https://brainflow.readthedocs.io/en/stable/UserAPI.html#brainflow-data-filter


Flow:
Cyton Board > LSL > Neuropype > LSL > Python
Cyton Board > Brainflow > Python

- Get data streaming to script (via LSL/Brainflow)
- Preprocessing steps:
  - Filter
  - Segmentation
  - FFT(?)
- Classification:
  - CCA(?)




## CCA/SSVEP Python Libraries: (other than scikit-learn)
- https://github.com/jameschapman19/cca_zoo
- https://github.com/nbara/python-meegkit
- https://wiki.mentalab.com/applications/ssvep/

- https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0140703&type=printable