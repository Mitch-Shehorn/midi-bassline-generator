"""
Bassline Generation Core Module

Generates MIDI basslines with configurable musical parameters.
"""

import random
from midiutil import MIDIFile
import os
from datetime import datetime
from musical_scales import MusicalScales
from pathlib import Path

class BasslineGenerator:
    def __init__(self):
        """Initialize bassline generator with rhythm patterns and note configurations."""
        self.musical_scales = MusicalScales()
        
        # Define rhythm patterns for different genres
        self.rhythm_patterns = {
            'Funk': [
                [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0],
                [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0] 
            ],
            'Darksynth': [
                [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0],
                [1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0]
            ],
            'Pop': [
                [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
                [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]
            ],
            'Trap': [
                [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
                [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0]
            ]
        }
        
        # Available note durations in beats
        self.note_durations = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0]

    def generate_bassline(self, root_note, scale_type, genre, num_bars=4, note_density=1.0):
        """
        Generate a bassline with specified musical parameters.
        
        Args:
            root_note (str): Root note for scale generation (e.g., 'C', 'F#')
            scale_type (str): Type of musical scale (e.g., 'major', 'minor')
            genre (str): Rhythmic style influencing note placement
            num_bars (int, optional): Number of bars to generate. Defaults to 4.
            note_density (float, optional): Probability of note generation. Defaults to 1.0.
        
        Returns:
            list: Generated bassline with note details
        """
        # Generate scale notes
        scale_notes = self.musical_scales.generate_scale(root_note, scale_type)
        bassline = []
        
        for bar in range(num_bars):
            # Select a random rhythm pattern for the genre
            pattern = random.choice(self.rhythm_patterns[genre])
            
            for step, hit in enumerate(pattern):
                if hit and random.random() <= note_density:
                    # Select notes from lower half of the scale
                    lower_half_notes = scale_notes[:len(scale_notes)//2]
                    if not lower_half_notes:
                        lower_half_notes = scale_notes
                    
                    note = random.choice(lower_half_notes)
                    duration = random.choice(self.note_durations)
                    
                    note_data = {
                        'note': note,
                        'position': (bar * 16) + step,
                        'duration': duration,
                        'velocity': 100
                    }
                    
                    bassline.append(note_data)
        
        # Ensure at least one note is generated
        if not bassline:
            note = random.choice(scale_notes[:len(scale_notes)//2])
            bassline.append({
                'note': note,
                'position': 0,
                'duration': 1.0,
                'velocity': 100
            })
        
        return bassline

    def get_available_genres(self):
        """
        Retrieve all available rhythm genres.
        
        Returns:
            list: Available genre names sorted alphabetically
        """
        return sorted(list(self.rhythm_patterns.keys()))

    def create_midi_file(self, bassline, filename=None, tempo=120):
        """
        Create a MIDI file from the generated bassline and save to Desktop.
        
        Args:
            bassline (list): Generated bassline notes
            filename (str, optional): Output filename. Defaults to timestamp-based name.
            tempo (int, optional): Tempo in beats per minute. Defaults to 120.
        
        Returns:
            str: Full path to the created MIDI file
        
        Raises:
            ValueError: If bassline is empty
            OSError: If unable to access or write to Desktop directory
        """
        if not bassline:
            raise ValueError("Cannot create MIDI file with empty bassline")
        
        # MIDI file creation setup
        midi = MIDIFile(1)  # One track
        track = 0
        time = 0
        channel = 0
        
        midi.addTrackName(track, time, "Bassline")
        midi.addTempo(track, time, tempo)
        
        # Add notes to MIDI file
        for note in bassline:
            beat_position = note['position'] / 4.0
            midi.addNote(
                track, channel, 
                note['note'], beat_position,
                note['duration'], note['velocity']
            )
        
        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bassline_{timestamp}.mid"
        
        try:
            # Get Desktop path with OneDrive compatibility
            # Try standard Desktop path first
            desktop_path = Path.home() / "Desktop"
            
            # If standard path doesn't exist, try OneDrive path
            if not desktop_path.exists():
                onedrive_path = Path.home() / "OneDrive" / "Desktop"
                if onedrive_path.exists():
                    desktop_path = onedrive_path
                else:
                    # Create Desktop directory if it doesn't exist
                    desktop_path.mkdir(parents=True, exist_ok=True)
            
            # Ensure filename is safe
            safe_filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.'))
            filepath = desktop_path / safe_filename
            
            # Create MIDI file
            with open(filepath, "wb") as output_file:
                midi.writeFile(output_file)
            
            return str(filepath)
            
        except OSError as e:
            raise OSError(f"Failed to save MIDI file to Desktop: {str(e)}")
