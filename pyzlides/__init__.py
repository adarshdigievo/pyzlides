"""
Pyzlides: Python Presentation Creator

A Python library for generating presentation slides in PDF format using declarative Python code.
"""

from .core import (
    BaseElement,
    Head1,
    Head2,
    Head3,
    BodyText,
    Bold,
    Code,
    Img,
    Center,
    Bottom,
    TitleSlide,
    GridLayout,
    BackgroundImage,
    Slide,
    Config,
    PyzlidesPDF
)

__version__ = "1.0.0"
__author__ = "Pyzlides Team"

__all__ = [
    "BaseElement",
    "Head1",
    "Head2", 
    "Head3",
    "BodyText",
    "Bold",
    "Code",
    "Img",
    "Center",
    "Bottom",
    "TitleSlide",
    "GridLayout",
    "BackgroundImage",
    "Slide",
    "Config",
    "PyzlidesPDF"
]
