# midi_preview.py
import pygame
import tempfile
from pathlib import Path
import time
from midiutil import MIDIFile
import logging
from typing import List, Dict, Union, Optional

# Configure logging for debugging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MIDIPreview:
    """
    MIDI preview system for bassline generator with robust error handling and resource management.
    Manages temporary file creation and pygame-based MIDI playback.
    Supports multiple bass instruments and full-length preview playback.
    """
    
    # Define available MIDI bass instruments with their program numbers
    BASS_INSTRUMENTS = {
        'Acoustic Bass': 32,
        'Electric Bass (finger)': 33,
        'Electric Bass (pick)': 34,
        'Fretless Bass': 35,
        'Slap Bass 1': 36,
        'Slap Bass 2': 37,
        'Synth Bass 1': 38,
        'Synth Bass 2': 39
    }
    
    def __init__(self) -> None:
        """
        Initialize the MIDI preview system.
        Sets up pygame mixer and creates a temporary directory for MIDI files.
        Initializes default bass instrument.
        """
        try:
            # Initialize pygame mixer with optimal audio settings
            pygame.mixer.init(
                frequency=44100,
                size=-16,
                channels=2,
                buffer=2048
            )
            
            # Create temporary directory for MIDI files
            self._temp_dir = Path(tempfile.mkdtemp(prefix='midi_preview_'))
            self._current_preview: Optional[Path] = None
            self._current_instrument = 'Synth Bass 1'  # Default instrument
            
            logger.debug(f"Initialized MIDIPreview system. Temp dir: {self._temp_dir}")
            
        except pygame.error as e:
            raise RuntimeError(f"Failed to initialize audio system: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize preview system: {e}")

    def set_instrument(self, instrument_name: str) -> None:
        """
        Set the active bass instrument for playback.
        
        Args:
            instrument_name: Name of the instrument from BASS_INSTRUMENTS
            
        Raises:
            ValueError: If instrument name is not in the available instruments list
        """
        if instrument_name not in self.BASS_INSTRUMENTS:
            raise ValueError(f"Invalid instrument. Choose from: {', '.join(self.BASS_INSTRUMENTS.keys())}")
        self._current_instrument = instrument_name
        logger.debug(f"Set instrument to: {instrument_name}")

    def get_available_instruments(self) -> List[str]:
        """
        Get list of available bass instruments.
        
        Returns:
            List of instrument names sorted alphabetically
        """
        return sorted(self.BASS_INSTRUMENTS.keys())

    def create_preview(self, bassline: List[Dict[str, Union[int, float]]], tempo: int = 120) -> Path:
        """
        Create a temporary MIDI file for preview playback.
        
        Args:
            bassline: List of note dictionaries with keys:
                     'note' (int): MIDI note number
                     'position' (int/float): Beat position
                     'duration' (float): Note duration in beats
                     'velocity' (int): Note velocity (0-127)
            tempo: Playback tempo in BPM
            
        Returns:
            Path object pointing to the created MIDI file
            
        Raises:
            ValueError: If bassline is empty or invalid
            RuntimeError: If MIDI file creation fails
        """
        if not bassline:
            raise ValueError("Cannot create preview: empty bassline")
            
        try:
            # Create unique filename using timestamp
            current_time = int(time.time())
            preview_path = self._temp_dir / f"preview_{current_time}.mid"
            
            # Initialize MIDI file with explicit parameters
            midi = MIDIFile(
                numTracks=1,
                removeDuplicates=True,
                deinterleave=False
            )
            
            # Define track parameters
            track_number = 0
            channel = 0
            initial_time = 0
            
            # Initialize track
            midi.addTrackName(track_number, initial_time, "Bassline Preview")
            midi.addTempo(track_number, initial_time, tempo)
            
            # Add program change for bass instrument
            program_number = self.BASS_INSTRUMENTS[self._current_instrument]
            midi.addProgramChange(track_number, channel, initial_time, program_number)
            
            # Add all notes with explicit timing
            for note in bassline:
                beat_position = float(note['position']) / 4.0
                midi.addNote(
                    track=track_number,
                    channel=channel,
                    pitch=note['note'],
                    time=beat_position,
                    duration=note['duration'],
                    volume=note['velocity']
                )
            
            # Write MIDI file with error handling
            with open(preview_path, "wb") as output_file:
                midi.writeFile(output_file)
            
            logger.debug(f"Created preview MIDI file: {preview_path}")
            return preview_path
            
        except Exception as e:
            logger.error(f"Failed to create MIDI preview: {e}")
            raise RuntimeError(f"Failed to create MIDI preview: {e}")

    def play_preview(self, midi_path: Path) -> None:
        """
        Play a MIDI preview file with error handling.
        
        Args:
            midi_path: Path to the MIDI file to play
            
        Raises:
            FileNotFoundError: If MIDI file doesn't exist
            RuntimeError: If playback fails
        """
        if not midi_path.exists():
            raise FileNotFoundError(f"MIDI file not found: {midi_path}")
            
        try:
            self.stop_preview()  # Stop any current playback
            pygame.mixer.music.load(str(midi_path))
            pygame.mixer.music.play()
            self._current_preview = midi_path
            logger.debug(f"Started playback: {midi_path}")
            
        except pygame.error as e:
            logger.error(f"Playback failed: {e}")
            raise RuntimeError(f"Failed to play MIDI preview: {e}")

    def stop_preview(self) -> None:
        """
        Stop current preview playback safely.
        Handles edge cases where mixer might not be initialized.
        """
        try:
            if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                logger.debug("Stopped playback")
        except pygame.error as e:
            logger.warning(f"Error stopping playback: {e}")

    def is_playing(self) -> bool:
        """
        Check if preview is currently playing.
        
        Returns:
            bool: True if preview is playing, False otherwise
        """
        try:
            return bool(pygame.mixer.music.get_busy())
        except pygame.error:
            return False

    def cleanup(self) -> None:
        """
        Clean up resources and temporary files.
        Should be called when the preview system is no longer needed.
        """
        logger.debug("Starting cleanup")
        
        # Stop playback
        self.stop_preview()
        
        # Remove temporary files
        try:
            for file in self._temp_dir.glob("*.mid"):
                try:
                    file.unlink()
                    logger.debug(f"Removed temp file: {file}")
                except Exception as e:
                    logger.warning(f"Failed to remove file {file}: {e}")
            
            self._temp_dir.rmdir()
            logger.debug("Removed temp directory")
            
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
        
        # Quit pygame mixer
        try:
            pygame.mixer.quit()
            logger.debug("Pygame mixer shutdown complete")
        except pygame.error as e:
            logger.warning(f"Error during pygame shutdown: {e}")
