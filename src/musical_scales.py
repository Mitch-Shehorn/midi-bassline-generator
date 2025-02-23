"""
Musical Scales and Note Utilities Module

Provides comprehensive musical scale and note-related functionality.
"""

class MusicalScales:
    """
    Comprehensive musical scale and note management utility.
    
    Supports multiple scale types, root notes, and musical transformations.
    """
    
    def __init__(self):
        """
        Initialize musical scale and note configurations.
        Provides an extensive collection of musical scales and root notes.
        """
        self.scales = {
            # Standard Scales
            'major': [0, 2, 4, 5, 7, 9, 11],
            'minor': [0, 2, 3, 5, 7, 8, 10],
            'pentatonic_major': [0, 2, 4, 7, 9],
            'pentatonic_minor': [0, 3, 5, 7, 10],
            'blues': [0, 3, 5, 6, 7, 10],
            
            # Church Modes 
            'dorian': [0, 2, 3, 5, 7, 9, 10],
            'phrygian': [0, 1, 3, 5, 7, 8, 10],
            'lydian': [0, 2, 4, 6, 7, 9, 11],
            'mixolydian': [0, 2, 4, 5, 7, 9, 10],
            'locrian': [0, 1, 3, 5, 6, 8, 10],
            
            # Modified Minor Scales
            'harmonic_minor': [0, 2, 3, 5, 7, 8, 11],
            'melodic_minor': [0, 2, 3, 5, 7, 9, 11],
            'hungarian_minor': [0, 2, 3, 6, 7, 8, 11],
            
            # World Music Scales
            'hirajoshi': [0, 2, 3, 7, 8],
            'persian': [0, 1, 4, 5, 6, 8, 11],
            'byzantine': [0, 1, 4, 5, 7, 8, 11],
            'egyptian': [0, 2, 5, 7, 10],
            
            # Synthetic Scales
            'whole_tone': [0, 2, 4, 6, 8, 10],
            'diminished': [0, 2, 3, 5, 6, 8, 9, 11],
            'prometheus': [0, 2, 4, 6, 9, 10],
            'enigmatic': [0, 1, 4, 6, 8, 10, 11]
        }

        self.root_notes = {
            'C': 36, 'C#': 37, 'Db': 37, 
            'D': 38, 'D#': 39, 'Eb': 39,
            'E': 40, 'F': 41, 'F#': 42, 
            'Gb': 42, 'G': 43, 'G#': 44,
            'Ab': 44, 'A': 45, 'A#': 46, 
            'Bb': 46, 'B': 47
        }

    def generate_scale(self, root_note, scale_type, octaves=2):
        """
        Generate a musical scale based on root note and scale type.
        
        Args:
            root_note (str): Musical root note (e.g., 'C', 'G#')
            scale_type (str): Type of musical scale 
            octaves (int, optional): Number of octaves to generate. Defaults to 2.
        
        Returns:
            list: MIDI note numbers representing the generated scale
        
        Raises:
            ValueError: If root note or scale type is invalid
        """
        if root_note not in self.root_notes:
            raise ValueError(f"Invalid root note. Choose from: {', '.join(sorted(self.root_notes.keys()))}")
        if scale_type not in self.scales:
            raise ValueError(f"Invalid scale type. Choose from: {', '.join(sorted(self.scales.keys()))}")
            
        root_midi = self.root_notes[root_note]
        scale_intervals = self.scales[scale_type]
        scale_notes = []
        
        for octave in range(octaves):
            for interval in scale_intervals:
                note = root_midi + interval + (octave * 12) 
                scale_notes.append(note)
        
        return scale_notes

    def get_available_scales(self):
        """
        Retrieve all available musical scales.
        
        Returns:
            list: Names of available musical scales
        """
        return sorted(list(self.scales.keys()))

    def get_available_root_notes(self):
        """
        Retrieve all available root notes.
        
        Returns:
            list: Available root note names
        """
        return sorted(list(self.root_notes.keys()))
