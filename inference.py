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
from waveglow.denoiser import Denoiser


class Inference:

    def __init__(self):
        self.hparams = create_hparams()
        self.checkpoint_path = "models/tacotron2_statedict.pt"
        self.waveglow_path = 'models/waveglow_256channels.pt'
        self.model = None
        self.waveglow = None
        self.denoiser = None

    #model = None
    #waveglow = None
    #denoiser = None


    def load_model(self):
        self.hparams.sampling_rate = 22050
        self.model = load_model(self.hparams)
        self.model.load_state_dict(torch.load(self.checkpoint_path)['state_dict'])
        _ = self.model.cuda().eval().half()

        self.waveglow = torch.load(self.waveglow_path)['model']
        for m in self.waveglow.modules():
            if 'Conv' in str(type(m)):
                setattr(m, 'padding_mode', 'zeros')
        self.waveglow.cuda().eval().half()
        for k in self.waveglow.convinv:
            k.float()

        self.denoiser = Denoiser(self.waveglow)


    def infer(self, input):
        audio = None

        sequence = np.array(text_to_sequence(input, ['english_cleaners']))[None, :]
        sequence = torch.autograd.Variable(
            torch.from_numpy(sequence)).cuda()

        mel_outputs, mel_outputs_postnet, _, alignments = self.model.inference(sequence)


        with torch.no_grad():
            audio = self.waveglow.infer(mel_outputs_postnet, sigma=0.666)

        print(type(audio))

        filename = "static/generatedAudio/"+str(random.randint(100, 1000)) + 'audio.wav'

        audio_denoised = self.denoiser(audio, strength=0.01)[:, 0]
        audio_denoised = audio_denoised.data.cpu().float()

        torchaudio.save(filename, audio_denoised, self.hparams.sampling_rate)
        return filename
