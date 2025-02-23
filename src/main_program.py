"""
Main program for generating MIDI basslines using the BasslineGenerator class.
Supports both manual and dice roll parameter entry.
"""
import random
import os
from bassline_generator_core import BasslineGenerator
from dice_roller import DiceRoller

def main():
    """
    Primary execution function for Bassline Generator.
    """
    generator = BasslineGenerator()
    
    print("\nEnhanced Bassline Generator")
    print("----------------------------")
    
    print("\nAvailable Options:")
    print("1. Manual Parameter Entry")
    print("2. Dice Roll (Random Generation)")
    
    while True:
        try:
            mode = input("\nChoose mode (1/2): ").strip()
            
            if mode == '1':
                # Manual parameter entry
                # Access root notes through the musical_scales instance
                root_note = input("\nEnter root note: ").strip()
                if root_note not in generator.musical_scales.root_notes:
                    print(f"Invalid root note. Please choose from: {', '.join(sorted(generator.musical_scales.root_notes.keys()))}")
                    continue
                    
                # Access scales through the musical_scales instance
                scale_list = sorted(generator.musical_scales.scales.keys())
                while True:
                    try:
                        print("\nAvailable scales:")
                        for i, scale in enumerate(scale_list, 1):
                            print(f"{i}. {scale.replace('_', ' ').title()}")
                        scale_index = int(input("\nEnter scale number: ")) - 1
                        if 0 <= scale_index < len(scale_list):
                            scale_type = scale_list[scale_index]
                            break 
                        else:
                            print("Invalid scale number. Please try again.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                    
                genre = input("Enter genre: ").strip().capitalize()
                if genre not in generator.rhythm_patterns:
                    print("Invalid genre. Please choose from: Funk, Darksynth, Pop, Trap")
                    continue
                    
                tempo = int(input("Enter tempo (BPM): ").strip())
                if not 40 <= tempo <= 240:
                    print("Tempo must be between 40 and 240 BPM")
                    continue
                    
                bars = int(input("Enter number of bars (1-16): ").strip())
                if not 1 <= bars <= 16:
                    print("Number of bars must be between 1 and 16")  
                    continue
                    
                note_density = float(input("Enter note density (0.0 - 1.0): ").strip())
                if not 0.0 <= note_density <= 1.0:
                    print("Note density must be between 0.0 and 1.0")
                    continue
            
            elif mode == '2':
                # Dice roll mode
                params = DiceRoller.interactive_roll(generator)
                
                # Check if user cancelled dice roll
                if params is None:
                    continue
                
                # Unpack dice roll parameters
                root_note = params['root_note']
                scale_type = params['scale_type']
                genre = params['genre']
                tempo = params['tempo']
                bars = params['bars']
                note_density = params['note_density']
            
            else:
                print("Invalid mode. Please choose 1 or 2.")
                continue
            
            break
        
        except ValueError:
            print("Invalid input. Please try again.")
            
    print("\nGenerating bassline...")
    bassline = generator.generate_bassline(root_note, scale_type, genre, bars, note_density)
    
    # Generate descriptive filename
    filename = f"{genre.lower()}_bassline_{root_note}_{scale_type}_{tempo}bpm.mid"
    filepath = generator.create_midi_file(bassline, filename, tempo)
        
    print(f"\nSuccess! MIDI file saved to: {os.path.abspath(filepath)}") 
        
if __name__ == "__main__":
    main()
