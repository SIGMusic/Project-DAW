# Description: This file contains the DAWInterface class, which is responsible for managing the DAW's state and handling user input.
import math
import pygame.mixer as mixer
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
        self.is_playing = False
        self.base_y = HEIGHT - (CONTROL_PANEL_HEIGHT // 2)
        mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    
    def file_select(self):
        root = Tk()
        root.withdraw()
        file_path = askopenfilename(title="Select a File", filetypes=[("All Files", "*.*")])
        return file_path
    
    def load_audio(self, filepath):
        try:
            audio_data = Wave(filepath).audio_data
            if (len(audio_data.shape) == 1):
                audio_data = np.stack((audio_data, audio_data), axis=1)
            print (audio_data.shape)
            return audio_data
        except:
            return np.zeros(3000)
    
    def add_track(self, audio_data):
        self.tracks.append(audio_data)
        self.sounds.append(mixer.Sound(audio_data))

    def play_audio(self):
        self.is_playing = True
        if self.sounds is not None:
            for sound in self.sounds:
                sound.play()

    def stop_audio(self):
        self.is_playing = False
        mixer.stop()

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
                    and not self.is_playing):
                    self.play_audio()
                if (self.is_inside_circle(event.pos, (120, self.base_y), 20)
                    and self.is_playing):
                    self.is_playing = False
                    self.stop_audio()
                if (WIDTH - 120 < event.pos[0] < WIDTH 
                    and HEIGHT - FILE_UPLOAD_HEIGHT < event.pos[1] < HEIGHT
                    and self.tracks.__len__() < 6):
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