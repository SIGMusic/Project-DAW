import scipy.signal
import librosa

track_zoom = 100
sample_rate = 22050
samples_per_pixel = sample_rate // track_zoom
print(samples_per_pixel)
sixty_bpm, sr = librosa.load(sr=None, path="60.mp3", mono=False)
sixty_bpm = librosa.resample(y=sixty_bpm, orig_sr=sr, target_sr=sample_rate)
print(len(sixty_bpm.T) / sample_rate)

sixty_decimate = scipy.signal.decimate(sixty_bpm, samples_per_pixel)
print(len(sixty_decimate.T) / track_zoom)