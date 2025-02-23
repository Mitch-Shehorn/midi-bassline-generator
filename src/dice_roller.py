"""
Dice Roll Module for Bassline Generator

This module provides randomization utilities for generating musical parameters.
"""

import random

class DiceRoller:
    """
    A utility class for generating randomized musical parameters.
    
    Design Principles:
    - Provides controlled randomization
    - Maintains musical coherence
    - Flexible parameter generation
    """
    
    @staticmethod
    def roll_parameters(generator):
        """
        Randomly generate bassline generation parameters.
        
        Args:
            generator (BasslineGenerator): Bassline generation utility 
                providing access to available musical parameters
        
        Returns:
            dict: Randomly selected parameters for bassline generation
        
        Key Randomization Constraints:
        - Fixed 8-bar length for consistent musical phrasing
        - Tempo range: 60-180 BPM (musically practical)
        - Note density: 0.3-1.0 (ensures meaningful musical content)
        """
        return {
            'root_note': random.choice(list(generator.musical_scales.root_notes.keys())),
            'scale_type': random.choice(generator.musical_scales.get_available_scales()),
            'genre': random.choice(generator.get_available_genres()),
            'tempo': random.randint(60, 180),
            'bars': 8,  # Consistent 8-bar phrase
            'note_density': round(random.uniform(0.3, 1.0), 2)
        }
    
    @staticmethod
    def print_parameters(params):
        """
        Formats and prints generated parameters in a readable layout.
        
        Args:
            params (dict): Generated musical parameters
        
        Output Design:
        - Clear, structured visual representation
        - Highlights key musical characteristics
        """
        print("\n🎲 Dice Roll Parameters 🎲")
        print("-" * 30)
        print(f"Root Note:     {params['root_note']}")
        print(f"Scale Type:    {params['scale_type'].replace('_', ' ').title()}")
        print(f"Genre:         {params['genre']}")
        print(f"Tempo:         {params['tempo']} BPM")
        print(f"Bars:          {params['bars']} (Fixed)")
        print(f"Note Density:  {params['note_density']}")
        print("-" * 30)
    
    @staticmethod
    def interactive_roll(generator):
        """
        Interactive dice roll with user confirmation.
        
        Args:
            generator (BasslineGenerator): Bassline generation utility
        
        Returns:
            dict or None: Confirmed parameters or None if cancelled
        
        Interaction Flow:
        - Generate parameters
        - Display parameters
        - Allow user to accept, reject, or re-roll
        """
        while True:
            # Generate initial parameters
            params = DiceRoller.roll_parameters(generator)
            DiceRoller.print_parameters(params)
            
            # User confirmation prompt
            confirm = input("\nAccept these parameters? (Y/N/R) [Yes/No/Re-roll]: ").strip().lower()
            
            if confirm == 'y':
                return params
            elif confirm == 'n':
                return None
            elif confirm == 'r':
                # Continue loop to regenerate
                continue
            else:
                print("Invalid input. Please enter Y, N, or R.")
