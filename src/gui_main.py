# gui_main.py
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from bassline_generator_core import BasslineGenerator
from dice_roller import DiceRoller
from midi_preview import MIDIPreview
import pygame
import logging

# Configure logging system with standard formatting
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BasslineGeneratorGUI:
    """Main GUI application for Bassline Generator with integrated MIDI preview"""
    
    def __init__(self, root):
        """Initialize the GUI application and its components"""
        logger.debug("Initializing Bassline Generator GUI")
        self.root = root
        self.root.title("Bassline Generator")
        self.root.geometry("800x600")
        
        # Initialize core components
        try:
            self.generator = BasslineGenerator()
            self.preview_system = MIDIPreview()
            logger.debug("Core components initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize core components: {e}")
            raise
        
        # Create main container
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Build UI components
        self._create_parameter_controls()
        self._create_generation_controls()
        self._create_status_area()
        self._apply_styling()
        
        logger.debug("GUI initialization complete")

    def _create_parameter_controls(self):
        """Create and configure musical parameter input controls"""
        params_frame = ttk.LabelFrame(self.main_frame, text="Musical Parameters", padding="5")
        params_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Root Note Selection
        ttk.Label(params_frame, text="Root Note:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.root_note_var = tk.StringVar(value='C')
        root_note_combo = ttk.Combobox(params_frame, 
                                     textvariable=self.root_note_var,
                                     values=sorted(self.generator.musical_scales.root_notes.keys()),
                                     state='readonly')
        root_note_combo.grid(row=0, column=1, sticky="ew", pady=2)
        
        # Scale Type Selection
        ttk.Label(params_frame, text="Scale Type:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.scale_type_var = tk.StringVar(value='major')
        scale_type_combo = ttk.Combobox(params_frame,
                                      textvariable=self.scale_type_var,
                                      values=sorted(self.generator.musical_scales.scales.keys()),
                                      state='readonly')
        scale_type_combo.grid(row=1, column=1, sticky="ew", pady=2)
        
        # Genre Selection
        ttk.Label(params_frame, text="Genre:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.genre_var = tk.StringVar(value='Funk')
        genre_combo = ttk.Combobox(params_frame,
                                 textvariable=self.genre_var,
                                 values=self.generator.get_available_genres(),
                                 state='readonly')
        genre_combo.grid(row=2, column=1, sticky="ew", pady=2)
        
        # Tempo Control
        ttk.Label(params_frame, text="Tempo (BPM):").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.tempo_var = tk.StringVar(value='120')
        tempo_spinbox = ttk.Spinbox(params_frame,
                                  from_=40,
                                  to=240,
                                  textvariable=self.tempo_var,
                                  width=10)
        tempo_spinbox.grid(row=3, column=1, sticky="ew", pady=2)
        
        # Bars Control
        ttk.Label(params_frame, text="Number of Bars:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.bars_var = tk.StringVar(value='4')
        bars_spinbox = ttk.Spinbox(params_frame,
                                 from_=1,
                                 to=16,
                                 textvariable=self.bars_var,
                                 width=10)
        bars_spinbox.grid(row=4, column=1, sticky="ew", pady=2)
        
        # Note Density Control
        ttk.Label(params_frame, text="Note Density:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.density_var = tk.DoubleVar(value=1.0)
        density_scale = ttk.Scale(params_frame,
                                from_=0.0,
                                to=1.0,
                                variable=self.density_var,
                                orient=tk.HORIZONTAL)
        density_scale.grid(row=5, column=1, sticky="ew", pady=2)
        
        # Bass Instrument Selection
        ttk.Label(params_frame, text="Bass Instrument:").grid(row=6, column=0, sticky=tk.W, pady=2)
        self.instrument_var = tk.StringVar(value='Synth Bass 1')
        instrument_combo = ttk.Combobox(params_frame,
                                      textvariable=self.instrument_var,
                                      values=self.preview_system.get_available_instruments(),
                                      state='readonly')
        instrument_combo.grid(row=6, column=1, sticky="ew", pady=2)
        
        # Bind instrument change event
        instrument_combo.bind('<<ComboboxSelected>>', self._on_instrument_change)

    def _on_instrument_change(self, event):
        """Handle instrument selection changes"""
        try:
            self.preview_system.set_instrument(self.instrument_var.get())
            self.status_text.insert(tk.END, f"Changed instrument to: {self.instrument_var.get()}\n")
            self.status_text.see(tk.END)
        except Exception as e:
            logger.error(f"Failed to change instrument: {e}")
            messagebox.showerror("Error", f"Failed to change instrument: {e}")

    def _create_generation_controls(self):
        """Create preview and generation control buttons"""
        controls_frame = ttk.Frame(self.main_frame)
        controls_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)
        
        # Preview Controls
        preview_frame = ttk.LabelFrame(controls_frame, text="Preview", padding="5")
        preview_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.preview_btn = ttk.Button(preview_frame,
                                    text="▶ Preview",
                                    command=self._preview_bassline)
        self.preview_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_preview_btn = ttk.Button(preview_frame,
                                         text="■ Stop",
                                         command=self._stop_preview)
        self.stop_preview_btn.pack(side=tk.LEFT, padx=5)
        self.stop_preview_btn.state(['disabled'])
        
        # Generation Controls
        generate_frame = ttk.LabelFrame(controls_frame, text="Generation", padding="5")
        generate_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.generate_btn = ttk.Button(generate_frame,
                                     text="Generate Bassline",
                                     command=self._generate_bassline)
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        
        self.dice_roll_btn = ttk.Button(generate_frame,
                                      text="Random Parameters",
                                      command=self._roll_parameters)
        self.dice_roll_btn.pack(side=tk.LEFT, padx=5)

    def _create_status_area(self):
        """Create status display area with scrolling text widget"""
        status_frame = ttk.LabelFrame(self.main_frame, text="Status", padding="5")
        status_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        self.status_text = tk.Text(status_frame, height=10, width=60, wrap=tk.WORD)
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_text.configure(yscrollcommand=scrollbar.set)

    def _preview_bassline(self):
        """Generate and play a preview of the current bassline settings"""
        logger.debug("Starting bassline preview generation")
        try:
            # Update UI state
            self.preview_btn.state(['disabled'])
            self.stop_preview_btn.state(['!disabled'])
            
            # Get current parameters
            params = {
                'root_note': self.root_note_var.get(),
                'scale_type': self.scale_type_var.get(),
                'genre': self.genre_var.get(),
                'tempo': int(self.tempo_var.get()),
                'bars': int(self.bars_var.get()),  # Use full bar count for preview
                'note_density': float(self.density_var.get())
            }
            logger.debug(f"Preview parameters: {params}")
            
            # Generate bassline
            bassline = self.generator.generate_bassline(
                params['root_note'],
                params['scale_type'],
                params['genre'],
                params['bars'],
                params['note_density']
            )
            
            if not bassline:
                raise ValueError("No notes generated for preview")
            
            # Create and play preview
            preview_path = self.preview_system.create_preview(bassline, params['tempo'])
            self.preview_system.play_preview(preview_path)
            
            # Update status
            self.status_text.insert(tk.END, f"Playing preview ({params['bars']} bars)...\n")
            self.status_text.see(tk.END)
            
            # Start monitoring
            self._monitor_preview()
            
        except Exception as e:
            logger.error(f"Preview failed: {e}")
            messagebox.showerror("Preview Error", str(e))
            self._stop_preview()

    def _stop_preview(self):
        """Stop the current preview playback"""
        logger.debug("Stopping preview playback")
        try:
            self.preview_system.stop_preview()
            self.preview_btn.state(['!disabled'])
            self.stop_preview_btn.state(['disabled'])
            
            self.status_text.insert(tk.END, "Preview stopped\n")
            self.status_text.see(tk.END)
            
        except Exception as e:
            logger.error(f"Error stopping preview: {e}")
            messagebox.showerror("Preview Error", f"Failed to stop preview: {e}")

    def _monitor_preview(self):
        """Monitor preview playback status"""
        try:
            if self.preview_system.is_playing():
                self.root.after(100, self._monitor_preview)
            else:
                self._stop_preview()
        except Exception as e:
            logger.error(f"Error monitoring preview: {e}")
            self._stop_preview()

    def _generate_bassline(self):
        """Handle full bassline generation in a separate thread"""
        try:
            self.generate_btn.state(['disabled'])
            self.dice_roll_btn.state(['disabled'])
            
            self.status_text.insert(tk.END, "Generating bassline...\n")
            self.status_text.see(tk.END)
            
            params = {
                'root_note': self.root_note_var.get(),
                'scale_type': self.scale_type_var.get(),
                'genre': self.genre_var.get(),
                'tempo': int(self.tempo_var.get()),
                'bars': int(self.bars_var.get()),
                'note_density': self.density_var.get()
            }
            
            thread = threading.Thread(target=self._generate_bassline_thread, args=(params,))
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            logger.error(f"Failed to start generation: {e}")
            messagebox.showerror("Error", f"Failed to generate bassline: {e}")
            self._enable_controls()

    def _generate_bassline_thread(self, params):
        """Generate bassline in background thread"""
        try:
            bassline = self.generator.generate_bassline(
                params['root_note'],
                params['scale_type'],
                params['genre'],
                params['bars'],
                params['note_density']
            )
            
            filename = f"{params['genre'].lower()}_bassline_{params['root_note']}_{params['scale_type']}_{params['tempo']}bpm.mid"
            filepath = self.generator.create_midi_file(bassline, filename, params['tempo'])
            
            self.root.after(0, self._update_status, f"Successfully generated: {filepath}\n")
            
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            self.root.after(0, messagebox.showerror, "Error", f"Generation failed: {e}")
        finally:
            self.root.after(0, self._enable_controls)

    def _roll_parameters(self):
        """Generate random musical parameters"""
        params = DiceRoller.roll_parameters(self.generator)
        
        self.root_note_var.set(params['root_note'])
        self.scale_type_var.set(params['scale_type'])
        self.genre_var.set(params['genre'])
        self.tempo_var.set(str(params['tempo']))
        self.bars_var.set(str(params['bars']))
        self.density_var.set(params['note_density'])
        
        # Randomly select an instrument
        instruments = self.preview_system.get_available_instruments()
        self.instrument_var.set(random.choice(instruments))
        self.preview_system.set_instrument(self.instrument_var.get())
        
        self.status_text.insert(tk.END, "Generated random parameters\n")
        self.status_text.see(tk.END)

    def _update_status(self, message):
        """Update status text display"""
        self.status_text.insert(tk.END, message)
        self.status_text.see(tk.END)

    def _enable_controls(self):
        """Re-enable control buttons"""
        self.generate_btn.state(['!disabled'])
        self.dice_roll_btn.state(['!disabled'])

    def _apply_styling(self):
        """Apply visual styling to GUI elements"""
        style = ttk.Style()
        style.configure("TButton", padding=6)
        style.configure("TFrame", padding=5)
        style.configure("TLabelframe", padding=10)
        
        # Enable proper grid weight distribution
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        
        # Apply specific styling for instrument controls
        style.configure("Instrument.TCombobox", padding=4)

    def cleanup(self):
        """Clean up resources before shutdown"""
        logger.debug("Performing application cleanup")
        if hasattr(self, 'preview_system'):
            self.preview_system.cleanup()

def main():
    """Application entry point"""
    logger.info("Starting Bassline Generator application")
    
    # Initialize random seed for consistent behavior
    import random
    random.seed()
    
    root = tk.Tk()
    app = BasslineGeneratorGUI(root)
    
    try:
        root.mainloop()
    except Exception as e:
        logger.error(f"Application error: {e}")
        messagebox.showerror("Error", f"Application error: {e}")
    finally:
        logger.info("Shutting down application")
        app.cleanup()

if __name__ == "__main__":
    main()