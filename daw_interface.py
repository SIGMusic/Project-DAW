# Description: This file contains the DAWInterface class, which is responsible for managing the DAW's state and handling user input.

from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
from config import WIDTH, TRACK_LABEL_WIDTH

class DAWInterface:
    def __init__(self):
        self.scroll_x = 0
        self.max_scroll_x = 3000
        self.scroll_speed = 20
        self.visible_width = WIDTH - TRACK_LABEL_WIDTH
        self.tracks = []
        self.dragging = False
        self.drag_start_x = 0
        self.drag_start_scroll = 0

    def add_track(self, audio_data):
        self.tracks.append(audio_data)

    def handle_input(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if event.pos[0] > TRACK_LABEL_WIDTH:  # Only allow dragging in the waveform area
                    self.dragging = True
                    self.drag_start_x = event.pos[0]
                    self.drag_start_scroll = self.scroll_x
        
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