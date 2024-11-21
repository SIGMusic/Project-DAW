# Description: This file contains the DAWInterface class, which is responsible 
# for managing the DAW's state, playback, and handling user input.
import os
import platform
import math
import pygame.mixer as mixer
import pygame.sndarray as sndarray
import numpy as np
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
from .config import *
from backend.wave import Wave
from tkinter import Tk
from tkinter.filedialog import askopenfilename

class DAWInterface:
    def __init__(self):
        self.scroll_x = 0
        self.max_scroll_x = 3000
        self.scroll_speed = 20
        self.visible_width = WIDTH - TRACK_LABEL_WIDTH
        self.tracks = []
        self.sounds = []
        self.dragging = False
        self.drag_start_x = 0
        self.drag_start_scroll = 0
        self.track_zoom = INITIAL_TRACK_ZOOM
        self.is_playing = False # If playback is occurring
        self.base_y = HEIGHT - (CONTROL_PANEL_HEIGHT // 2)
        self.max_len_track = 0
        mixer.quit() # Ensure reset to default configuration
        mixer.init(frequency=SAMPLE_RATE, size=-16, channels=2, buffer=2048)
    
    def file_select(self):
        system = platform.system()
        file_path = ""
        root = Tk()
        root.withdraw()
        if system == 'Windows' or system == 'Linux': # Windows Linux
            file_path = askopenfilename(title="Select a File", 
                filetypes=[
                    ('Waveform Audio File', '*.wav'), 
                    ('Free Lossless Audio Codec', '*.flac'), 
                    ('Ogg', '*.ogg'), 
                    ('MPEG-1 Audio Layer III', '*.mp3'), 
                    ('MPEG-4 Audio', '*.m4a')
                ]
            )
        elif system == 'Darwin': # MacOS
            file_path = askopenfilename(title="Select a File")
        else:
            raise OSError('Unsupported operating system: ' + system) 
        return file_path
        
    def load_audio(self, file_path):
        try:
            audio_data = Wave(file_path).audio_data
            
            # If mono, duplicate to make stereo
            if len(audio_data.shape) == 1:
                audio_data = np.stack((audio_data, audio_data), axis=1)
                
            # Check that the format matches rows -> samples, columns -> channels, swap if otherwise
            if audio_data.shape[0] < audio_data.shape[1]:
                audio_data = np.ascontiguousarray(audio_data.T)
                
            if audio_data.shape[0] > self.max_len_track:
                self.max_len_track = audio_data.shape[0]
            return audio_data
        except:
            return np.zeros(3000)
    
    def add_track(self, audio_data):
        self.tracks.append(audio_data)

    def combine_audio(self, s1, s2): # Helper method to layer audio tracks for playback
        size1 = s1.shape[0]
        size2 = s2.shape[0]
        if size1 > size2:
            s2 = np.pad(s2, [(0, size1 - size2), (0, 0)], mode='constant')
        if size1 < size2:
            s1 = np.pad(s1, [(0, size2 - size1), (0, 0)], mode='constant')
        return s1 + s2
    
    def play_audio(self):
        self.is_playing = True
        if self.tracks is not None:
            play = self.tracks[0]
            for i in range(1, len(self.tracks)):
                play = self.combine_audio(play, self.tracks[i]) # Layer audio tracks for simultaneous playback
            play = play.tobytes() # mixer.Sound() requires raw byte data
            mixer.Sound(buffer=play).play()

    def stop_audio(self):
        self.is_playing = False
        mixer.stop()

    # Helper to determine if a click occured within a circular button
    def is_inside_circle(self, point, center, radius):
        distance = math.sqrt((point[0] - center[0]) ** 2 + (point[1] - center[1]) ** 2)
        return distance <= radius

    def handle_input(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if event.pos[0] > TRACK_LABEL_WIDTH:  # Only allow dragging in the waveform area
                    self.dragging = True
                    self.drag_start_x = event.pos[0]
                    self.drag_start_scroll = self.scroll_x
                if (self.is_inside_circle(event.pos, (60, self.base_y), 20)
                    and not self.is_playing): # Play audio if play button clicked and it's not already playing
                    self.play_audio()
                if (self.is_inside_circle(event.pos, (120, self.base_y), 20)
                    and self.is_playing): # Stop audio if stop button clicked and it's playing
                    self.stop_audio()
                if (WIDTH - 120 < event.pos[0] < WIDTH 
                    and HEIGHT - FILE_UPLOAD_HEIGHT < event.pos[1] < HEIGHT
                    and self.tracks.__len__() < 6): # Launch file explorer if audio upload clicked and there is 6 or fewer tracks currently
                    self.add_track(self.load_audio(self.file_select()))
                

        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
            elif event.button == 4:  # Mouse wheel up
                self.scroll_x = max(0, self.scroll_x - self.scroll_speed)
            elif event.button == 5:  # Mouse wheel down
                self.scroll_x = min(self.max_scroll_x, self.scroll_x + self.scroll_speed)
        
        elif event.type == MOUSEMOTION:
            if self.dragging:
                dx = event.pos[0] - self.drag_start_x
                new_scroll = self.drag_start_scroll + dx  # Reverse the direction of scrolling
                self.scroll_x = max(0, min(self.max_scroll_x, new_scroll))