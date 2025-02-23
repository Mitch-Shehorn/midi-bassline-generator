# gui_main.py
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from bassline_generator_core import BasslineGenerator
from dice_roller import DiceRoller

class BasslineGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bassline Generator")
        self.root.geometry("800x600")
        
        # Initialize backend components
        self.generator = BasslineGenerator()
        
        # Create main container with padding
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self._create_parameter_controls()
        self._create_generation_controls()
        self._create_status_area()
        
        # Apply modern styling
        self._apply_styling()

    def _create_parameter_controls(self):
        """Create controls for musical parameters"""
        # Parameters Frame
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

    def _create_generation_controls(self):
        """Create controls for bassline generation"""
        controls_frame = ttk.Frame(self.main_frame)
        controls_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)
        
        # Generate Button
        self.generate_btn = ttk.Button(controls_frame,
                                     text="Generate Bassline",
                                     command=self._generate_bassline)
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        
        # Dice Roll Button
        self.dice_roll_btn = ttk.Button(controls_frame,
                                      text="Random Parameters",
                                      command=self._roll_parameters)
        self.dice_roll_btn.pack(side=tk.LEFT, padx=5)

    def _create_status_area(self):
        """Create status display area"""
        status_frame = ttk.LabelFrame(self.main_frame, text="Status", padding="5")
        status_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        self.status_text = tk.Text(status_frame, height=10, width=60, wrap=tk.WORD)
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_text.configure(yscrollcommand=scrollbar.set)

    def _apply_styling(self):
        """Apply modern styling to the GUI"""
        style = ttk.Style()
        style.configure("TButton", padding=6)
        style.configure("TFrame", padding=5)
        style.configure("TLabelframe", padding=10)
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

    def _generate_bassline(self):
        """Handle bassline generation in a separate thread"""
        try:
            # Disable controls during generation
            self.generate_btn.state(['disabled'])
            self.dice_roll_btn.state(['disabled'])
            
            # Update status
            self.status_text.insert(tk.END, "Generating bassline...\n")
            self.status_text.see(tk.END)
            
            # Get parameters
            params = {
                'root_note': self.root_note_var.get(),
                'scale_type': self.scale_type_var.get(),
                'genre': self.genre_var.get(),
                'tempo': int(self.tempo_var.get()),
                'bars': int(self.bars_var.get()),
                'note_density': self.density_var.get()
            }
            
            # Start generation in separate thread
            thread = threading.Thread(target=self._generate_bassline_thread, args=(params,))
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate bassline: {str(e)}")
            self.generate_btn.state(['!disabled'])
            self.dice_roll_btn.state(['!disabled'])

    def _generate_bassline_thread(self, params):
        """Generate bassline in separate thread"""
        try:
            # Generate bassline
            bassline = self.generator.generate_bassline(
                params['root_note'],
                params['scale_type'],
                params['genre'],
                params['bars'],
                params['note_density']
            )
            
            # Create MIDI file
            filename = f"{params['genre'].lower()}_bassline_{params['root_note']}_{params['scale_type']}_{params['tempo']}bpm.mid"
            filepath = self.generator.create_midi_file(bassline, filename, params['tempo'])
            
            # Update status
            self.root.after(0, self._update_status, f"Successfully generated: {filepath}\n")
            
        except Exception as e:
            self.root.after(0, messagebox.showerror, "Error", f"Generation failed: {str(e)}")
        finally:
            # Re-enable controls
            self.root.after(0, self._enable_controls)

    def _roll_parameters(self):
        """Generate random parameters"""
        params = DiceRoller.roll_parameters(self.generator)
        
        # Update GUI controls
        self.root_note_var.set(params['root_note'])
        self.scale_type_var.set(params['scale_type'])
        self.genre_var.set(params['genre'])
        self.tempo_var.set(str(params['tempo']))
        self.bars_var.set(str(params['bars']))
        self.density_var.set(params['note_density'])
        
        # Update status
        self.status_text.insert(tk.END, "Generated random parameters\n")
        self.status_text.see(tk.END)

    def _update_status(self, message):
        """Update status text"""
        self.status_text.insert(tk.END, message)
        self.status_text.see(tk.END)

    def _enable_controls(self):
        """Re-enable control buttons"""
        self.generate_btn.state(['!disabled'])
        self.dice_roll_btn.state(['!disabled'])

def main():
    root = tk.Tk()
    app = BasslineGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
