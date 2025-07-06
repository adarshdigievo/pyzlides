import sys
import os
from .core import Config, PyzlidesPDF, load_slide_from_file, Slide, BodyText


def generate_pdf():
    """Main function to generate PDF presentation"""
    # Load configuration
    config = Config()
    theme = config.get_theme()
    slide_files = config.get_slide_order()

    if not slide_files:
        print("No slide files specified in configuration. Nothing to generate.")
        return

    # Load slides
    slides = []
    for slide_file in slide_files:
        if os.path.exists(slide_file):
            slide = load_slide_from_file(slide_file)
            slides.append(slide)
        else:
            print(f"Warning: Slide file {slide_file} not found.")
            slides.append(Slide(BodyText(f"Slide not found: {slide_file}")))

    if not slides:
        print("No slides to generate.")
        return

    # Generate PDF
    pdf_generator = PyzlidesPDF()
    pdf_generator.generate(slides, theme)


def main():
    """Main entry point for command line interface"""
    if len(sys.argv) < 2:
        print("Usage: python -m pyzlides generate_pdf")
        print("   or: python pyzlides.py generate_pdf")
        sys.exit(1)

    command = sys.argv[1]

    if command == "generate_pdf":
        generate_pdf()
    else:
        print(f"Unknown command: {command}")
        print("Available commands: generate_pdf")
        sys.exit(1)


if __name__ == "__main__":
    main()