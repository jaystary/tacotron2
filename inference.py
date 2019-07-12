import IPython.display as ipd

import sys
sys.path.append('waveglow/')
import numpy as np
import torch
import torchaudio
import random

from hparams import create_hparams
from model import Tacotron2
from layers import TacotronSTFT, STFT
from audio_processing import griffin_lim
from train import load_model
from text import text_to_sequence


class Inference:

    def __init__(self):
        self.hparams = create_hparams()
        self.checkpoint_path = "models/tacotron2_statedict.pt"
        self.waveglow_path = 'models/waveglow_256channels.pt'

    model = None
    waveglow = None


    def load_model(self):
        self.hparams.sampling_rate = 22050
        model = load_model(self.hparams)
        model.load_state_dict(torch.load(self.checkpoint_path)['state_dict'])
        _ = model.cuda().eval().half()

        waveglow = torch.load(self.waveglow_path)['model']
        for m in waveglow.modules():
            if 'Conv' in str(type(m)):
                setattr(m, 'padding_mode', 'zeros')
        waveglow.cuda().eval().half()
        for k in waveglow.convinv:
            k.float()

        return model, waveglow




    def infer(self, input):
        self.hparams.sampling_rate = 22050
        model = load_model(self.hparams)
        model.load_state_dict(torch.load(self.checkpoint_path)['state_dict'])
        _ = model.cuda().eval().half()

        waveglow = torch.load(self.waveglow_path)['model']
        for m in waveglow.modules():
            if 'Conv' in str(type(m)):
                setattr(m, 'padding_mode', 'zeros')
        waveglow.cuda().eval().half()
        for k in waveglow.convinv:
            k.float()
        sequence = np.array(text_to_sequence(input, ['english_cleaners']))[None, :]
        sequence = torch.autograd.Variable(
            torch.from_numpy(sequence)).cuda().long()

        mel_outputs, mel_outputs_postnet, _, alignments = model.inference(sequence)


        with torch.no_grad():
            audio = waveglow.infer(mel_outputs_postnet, sigma=0.666)

        filename = "static/generatedAudio/"+str(random.randint(1, 101)) + 'audio.wav'

        torchaudio.save(filename, audio[0].data.cpu().long(), self.hparams.sampling_rate)
        return filename


        #return ipd.Audio(audio[0].data.cpu().numpy(), rate=self.hparams.sampling_rate)