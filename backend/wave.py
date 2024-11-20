import librosa
import numpy as np

class Wave:
    def __init__(self, filepath):
        self.audio_data, self.sr = librosa.load(filepath, mono=False)
        
        