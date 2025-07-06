"""
Entry point for running pyzlides as a module.
Usage: python -m pyzlides generate_pdf
"""

from .cli import main

if __name__ == "__main__":
    main()