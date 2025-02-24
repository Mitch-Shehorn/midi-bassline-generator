import sys
import pkg_resources
import os

def verify_setup():
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    print("\nInstalled Packages:")
    for pkg in pkg_resources.working_set:
        print(f"  - {pkg.key} {pkg.version}")
    
    print("\nPYTHONPATH:")
    for path in sys.path:
        print(f"  - {path}")
    
    print("\nCurrent Working Directory:", os.getcwd())
    
    try:
        import midiutil
        print("\nmidiutil successfully imported!")
    except ImportError as e:
        print("\nError importing midiutil:", str(e))

if __name__ == "__main__":
    verify_setup()
