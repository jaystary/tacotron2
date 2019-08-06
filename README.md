# Tacotron 2 Adaption
This is an adaption of NVIDIA´s Tacotron2 implemention based on PyTorch with WaveGlow used as speech generation.

It includes code for for Inference (inference.py)

It has an API through flask socketIO

Tacotron2 has issues handling long input, thus one has to split up the incoming text. For that case i create batches of files and then merge then later on in the process. This entire process is logged and written to a DB Backend, thus it allows to do longrunning processing of batches without loosing the data if something breaks inbetween.
