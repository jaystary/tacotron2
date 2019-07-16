# Tacotron 2 Including Inference - currently work in progress

PyTorch implementation of [Natural TTS Synthesis By Conditioning
Wavenet On Mel Spectrogram Predictions](https://arxiv.org/pdf/1712.05884.pdf). 

Original implementation from https://github.com/NVIDIA/tacotron2

This implementation contains an API (with Flask as Framework) that can consume POST requests that transforms
Text into WAV-files which then are stored and can be downloaded/played back. 
It is an adaption of the included IPython Notebook
with a few adjustments in the inference code.


The inference code had some issues that originated from newer versions of 
Pytorch / Numpy, which have been adjusted (as commented in code).

[Waveglow](https://github.com/NVIDIA/waveglow) is used to generated audio from mel-spectograms.


For inference you will need:
For generating Mel-Spectograms from Text:

[Tacotron2 Model](https://drive.google.com/file/d/1c5ZTuT7J08wLUoVZ2KkUs_VdZuJ86ZqA/view?usp=sharing)

[Selftrained](https://jaystarymlmodels.s3.amazonaws.com/tacotron_trained.pt) (Quality is a bit lower):

For generating Speech Synthesis from Mel-Spectograms:
[WaveGlow Model](https://drive.google.com/file/d/1WsibBTsuRg_SF2Z6L6NFRTT-NjEy1oTx/view?usp=sharing)

Training and running this model requires a GPU / TPU.


Currently working on implementing a streaming solution that can take longer texts as input and get processed in chunks as output and displayed in a frontend. After that i want to implement batch processing where one can run big TTS jobs in the background.

