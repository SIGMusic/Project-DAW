#   very beginnery code for daw im not sure what im doing
#   created 11/10/24
#   emmett quan 👍

import pygame, sys
from pygame.locals import *
import numpy as np
from scipy.io import wavfile
from daw_interface import DAWInterface
from config import *

def main():
    pygame.init()
    pygame.display.set_caption("pungi")

    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
    daw = DAWInterface()
    daw.add_track(load_audio("exported_sound.wav")) # TODO: make configurable via UI
    daw.add_track(load_audio("exported_sound.wav"))

    while True:
        DISPLAYSURF.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            daw.handle_input(event)

        draw_timeline(DISPLAYSURF, daw.scroll_x)
        draw_tracks(DISPLAYSURF, daw)
        draw_filter_box(DISPLAYSURF)  
        draw_control_panel(DISPLAYSURF)
        draw_scroll_indicator(DISPLAYSURF, daw)
        
        pygame.display.update()

def draw_timeline(surface, scroll_x):
    # Draw timeline background
    pygame.draw.rect(surface, (40, 40, 40), (TRACK_LABEL_WIDTH, 0, WIDTH - TRACK_LABEL_WIDTH, TIMELINE_HEIGHT))
    
    # Draw time markers
    marker_spacing = 100
    start_marker = scroll_x // marker_spacing
    for i in range(15):  # Draw visible markers
        x_pos = TRACK_LABEL_WIDTH + (i * marker_spacing) - (scroll_x % marker_spacing)
        if x_pos >= TRACK_LABEL_WIDTH and x_pos < WIDTH:
            pygame.draw.line(surface, WHITE, (x_pos, 0), (x_pos, TIMELINE_HEIGHT - 5))
            time_text = f"{(start_marker + i):.1f}s"
            font = pygame.font.Font(None, 20)
            text = font.render(time_text, True, WHITE)
            surface.blit(text, (x_pos - 15, 5))

def draw_tracks(surface, daw):
    content_height = HEIGHT - CONTROL_PANEL_HEIGHT - TIMELINE_HEIGHT
    
    # Create a surface for the scrollable content
    content_surface = pygame.Surface((WIDTH - TRACK_LABEL_WIDTH, content_height))
    content_surface.fill(BLACK)
    
    # Draw each track
    for i in range(6): # Draw 6 tracks for now
        top = i * TRACK_HEIGHT + TIMELINE_HEIGHT
        
        pygame.draw.rect(surface, (60, 60, 60), (0, top, TRACK_LABEL_WIDTH, TRACK_HEIGHT))
        
        font = pygame.font.Font(None, 24)
        text = font.render(f"Track {i+1}", True, WHITE)
        surface.blit(text, (10, top + TRACK_HEIGHT//3))
        
        # Draw track content area
        pygame.draw.rect(surface, (40, 40, 40), 
                        (TRACK_LABEL_WIDTH, top, WIDTH - TRACK_LABEL_WIDTH, TRACK_HEIGHT))
        
        pygame.draw.line(surface, WHITE, (0, top), (WIDTH, top))
        
        # Draw waveform if audio data exists
        if daw.tracks is not None and i < len(daw.tracks):
            draw_waveform(surface, daw.tracks[i], top, daw.scroll_x)

def draw_waveform(surface, audio_data, top, scroll_x):
    # Create a subsurface for the waveform area
    waveform_rect = pygame.Rect(TRACK_LABEL_WIDTH, top, WIDTH - TRACK_LABEL_WIDTH, TRACK_HEIGHT)
    try:
        waveform_surface = surface.subsurface(waveform_rect)
    except ValueError:
        return

    normalized_data = (audio_data / np.max(np.abs(audio_data))) * (TRACK_HEIGHT // 2)
    center_line = TRACK_HEIGHT // 2
    
    # Only draw visible portion of waveform
    visible_start = max(0, int(scroll_x))
    visible_end = min(len(normalized_data), int(scroll_x + waveform_surface.get_width()))
    
    for x in range(visible_start, visible_end - 1):
        screen_x = x - scroll_x
        if 0 <= screen_x < waveform_surface.get_width() - 1:
            y1 = int(center_line - normalized_data[x])
            y2 = int(center_line - normalized_data[x + 1])
            pygame.draw.line(waveform_surface, WHITE, (screen_x, y1), (screen_x + 1, y2), 1)

def draw_filter_box(surface):
    y_position = HEIGHT - CONTROL_PANEL_HEIGHT - FILTER_BOX_HEIGHT # Filter box position above control panel
    
    pygame.draw.rect(surface, (40, 40, 40), 
                    (0, y_position, WIDTH, FILTER_BOX_HEIGHT))
    
    font = pygame.font.Font(None, 24)
    title = font.render("Filters", True, WHITE)
    surface.blit(title, (10, y_position + 10))
    
    # Placeholder for filters
    filter_options = ["Low Pass", "High Pass", "Band Pass"]
    for i, filter_name in enumerate(filter_options):
        x_pos = 100 + (i * 120)
        pygame.draw.rect(surface, (60, 60, 60),
                        (x_pos, y_position + 30, 100, 30))
        filter_text = font.render(filter_name, True, WHITE)
        surface.blit(filter_text, (x_pos + 10, y_position + 35))

def draw_control_panel(surface):
    pygame.draw.rect(surface, (50, 50, 50), 
                    (0, HEIGHT - CONTROL_PANEL_HEIGHT, WIDTH, CONTROL_PANEL_HEIGHT))
    base_y = HEIGHT - (CONTROL_PANEL_HEIGHT // 2)
    pygame.draw.circle(surface, WHITE, (60, base_y), 20)  # Play
    pygame.draw.polygon(surface, BLACK, [(50, base_y - 15), (50, base_y + 15), (80, base_y)])

    pygame.draw.circle(surface, WHITE, (120, base_y), 20)  # Stop
    pygame.draw.rect(surface, BLACK, (110, base_y - 15, 20, 30))

    pygame.draw.circle(surface, WHITE, (180, base_y), 20)  # Record
    pygame.draw.circle(surface, RED, (180, base_y), 15)

def draw_scroll_indicator(surface, daw):
    scroll_bar_width = WIDTH - TRACK_LABEL_WIDTH
    visible_ratio = daw.visible_width / daw.max_scroll_x
    handle_width = max(40, scroll_bar_width * visible_ratio)
    handle_pos = TRACK_LABEL_WIDTH + (scroll_bar_width - handle_width) * (daw.scroll_x / daw.max_scroll_x)
    
    y_pos = HEIGHT - CONTROL_PANEL_HEIGHT - FILTER_BOX_HEIGHT - 15
    
    pygame.draw.rect(surface, (40, 40, 40), 
                    (TRACK_LABEL_WIDTH, y_pos, WIDTH - TRACK_LABEL_WIDTH, 10))
    pygame.draw.rect(surface, WHITE, 
                    (handle_pos, y_pos, handle_width, 10))

def load_audio(filepath):
    try:
        sample_rate, audio_data = wavfile.read(filepath)
        if len(audio_data.shape) > 1:
            audio_data = audio_data[:, 0]
        downsampled_data = audio_data[::len(audio_data) // 3000]
        return downsampled_data
    except:
        return np.zeros(3000)

if __name__ == "__main__":
    main()
