import librosa
import numpy as np
from frontend.config import SAMPLE_RATE
class Wave:
    def __init__(self, file_path):
        # load the file from the given path
        self.audio_data, self.sr = librosa.load(sr=None, path=file_path, mono=False)
        
        # if the file's sample rate doesn't match our fixed rate as defined in frontend/config.py, make it match
        if self.sr != SAMPLE_RATE:
            self.audio_data = librosa.resample(self.audio_data, orig_sr=self.sr, target_sr=SAMPLE_RATE)
            
        # convert to int16 format so pygame.mixer.Sound can read it properly
        self.audio_data = np.int16(self.audio_data * 32767)

        