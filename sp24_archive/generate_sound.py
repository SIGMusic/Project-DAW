import numpy as np
from scipy.io.wavfile import write

# Storing all 4th Octave note frequency values in Hz 
A4_freq = 440
B4_freq = 493.88
C4_freq = 261.63
D4_freq = 293.66
E4_freq = 329.63
F4_freq = 349.23
G4_freq = 392

# Storing all 5th Octave note frequency values in Hz 
# A5_freq # = 440
# B5_freq # = 493.88
C5_freq = 523.25
D5_freq = 587.33
E5_freq = 659.25
# F5_freq # = 349.23
G5_freq = 783.99

# This function takes the time, frequency, amplitude, and sample_rate and returns a sound wave with those properties
def generate_sound(time, frequency, amp, sample_rate):
    # Discrete time samples for our sound wave
    t = np.linspace(0, time, int(sample_rate * time))
    sound = amp * np.sin(2 * np.pi * frequency * t)
    write('sound.wav', sample_rate, sound.astype(np.float32))
    
# This function generates the chord progression and melody of 505 by Arctic Monkeys 
def generate_505(sample_rate, sound):
    # Duration value and time array for the chord progression
    duration_chord = 4 
    t_chord = np.linspace(0, duration_chord, int(sample_rate * duration_chord))
    # Create 505 chord progression: Dm Em Dm Em
    D_minor = np.vstack([sound(t_chord, D4_freq, 0.1), sound(t_chord, F4_freq, 0.1), sound(t_chord, A4_freq, 0.1)])
    E_minor = np.vstack([sound(t_chord, E4_freq, 0.1), sound(t_chord, G4_freq, 0.1), sound(t_chord, B4_freq, 0.1)])
    chord_progression = np.vstack([D_minor, E_minor, D_minor, E_minor, D_minor, E_minor, D_minor, E_minor])
    
    # # Create melody notes for 505 
    # duration_melody = 1
    # E5 = sound(np.linspace(0, duration_melody, int(sample_rate * 1)), E5_freq, 0.5)
    # D5 = sound(np.linspace(0, duration_melody, int(sample_rate * 1)), D5_freq, 0.5)
    # C5 = sound(np.linspace(0, duration_melody, int(sample_rate * 1)), C5_freq, 0.5)
    # B4 = sound(np.linspace(0, duration_melody, int(sample_rate * 1)), B4_freq, 0.5)
    # A4 = sound(np.linspace(0, duration_melody, int(sample_rate * 1)), A4_freq, 0.5)
    
    # # Stack the melody notes horizontally and then vertically with the chord progression
    # generate_505 = np.vstack((np.hstack([E5, D5, C5, B4]).T, chord_progression)).T
    # For rhythm:
    generate_505 = chord_progression
    
    # Write down to file
    write('505.wav', sample_rate, generate_505.astype(np.float32))

def generate_basic_sound(sample_rate, sound):
    duration = 3  # Duration in seconds
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Create A minor chord
    A_minor = np.vstack([sound(t, A_freq, 0.1), sound(t, C_freq, 0.1), sound(t, E_freq, 0.1)])
    
    # Create melody notes each lasting for one second
    melody_C = sound(np.linspace(0, 1, int(sample_rate * 1)), C5_freq, 0.25)
    melody_E = sound(np.linspace(0, 1, int(sample_rate * 1)), E5_freq, 0.25)
    melody_G = sound(np.linspace(0, 1, int(sample_rate * 1)), G4_freq, 0.25)
    
    # Stack the melody notes vertically with the A minor chord 
    melody_with_chord = np.vstack([np.hstack([melody_E, melody_G, melody_C]).T, 
                                   np.hstack([melody_C, melody_E, melody_G]).T, A_minor])
    
    # Write down to file
    write('Achord_with_melody.wav', sample_rate, melody_with_chord.T.astype(np.float32))
    
if __name__ == '__main__':
    sample_rate = 8000
    sound = lambda time, freq, amp=1: amp * np.sin(2 * np.pi * freq * time)
    # generate_505(sample_rate, sound)
    generate_basic_sound(sample_rate, sound)
    # generate_sound(5, 440, 0.5, 8000)