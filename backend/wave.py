import librosa
import numpy as np

class Wave:
    def __init__(self, file_path):
        self.audio_data, self.sr = librosa.load(file_path, mono=False)
        
        