# Pyzlides: Python Presentation Creator

## Overview

Pyzlides is a Python library that allows users to generate presentation slides in PDF format using Python code. The slides will be generated in a standard PPT resolution, and elements like headers, body text, images, and layouts can be defined declaratively through Python classes. Pyzlides will support customizable themes, layouts, and ordering of slides via a configuration file.

## Features

1. **Declarative Slide Creation**: Define slides using Python classes such as `Head1`, `BodyText`, `Img`, etc.
2. **Custom Layouts**: Define custom layouts like `Center`, `Bottom`, etc., for positioning slide elements.
3. **Configurable Themes**: Use a configuration file to specify theme colors, fonts, and backgrounds.
4. **Slide Ordering**: Order slides using the configuration file, defining the sequence of Python slide files.
5. **PDF Output**: Generate a PDF presentation using the specified elements, themes, and layouts.
6. **Extendable**: Easy to add new slide elements or layouts by extending the base classes.

---

## Dependencies

* **ReportLab**: For generating the PDF slides.
* **Pillow**: For handling images in slides.
* **PyYAML**: For parsing the configuration file.


## Core Classes

1. **Base Slide Element Classes**

   These are the base classes that represent different slide elements.

   * `Head1(text: str)`: Represents a header element. Will be rendered with a large font size.
   * `BodyText(text: str)`: Represents body text. Used for normal paragraph-style text.
   * `Img(path: str, caption: str)`: Represents an image with an optional caption.
   * `Bold(text: str)`: Used to make the text bold.
   * `Center(element)`: Centers an element on the slide.
   * `Bottom(element)`: Positions an element at the bottom of the slide.

2. **Slide Class**
   This class represents a single slide. It will have an ordered list of elements and methods to render them.

   ```python
   class Slide:
       def __init__(self, elements: List[BaseElement]):
           self.elements = elements
   ```

3. **Configuration Class**
   This class handles the reading of the configuration file, which contains theme settings, slide ordering, etc.

   ```python
   class Config:
       def __init__(self, config_file: str):
           self.config = self.load_config(config_file)

       def load_config(self, config_file):
           # Parse the YAML or JSON config file
           pass
   ```

---

## Configuration File

The configuration file will be in **YAML** format for simplicity. Here is an example of the config file format:

### `config.yaml`

```yaml
theme:
  background_color: "#FFFFFF"
  font_color: "#000000"
  font_size: 12
  header_color: "#FF5733"
  font: "Helvetica"

slide_order:
  - "slide1.py"
  - "slide2.py"
  - "slide3.py"
  
layouts:
  Center: "centered"
  Bottom: "bottom-aligned"
  Left: "left-aligned"
```

---

## Slide Example Files

Each slide will be defined as a separate Python file.

### `slide1.py`

```python
from pyzlides import Head1, BodyText, Center

slide = Center(
    Head1("Introduction to Pyzlides")
)
```

### `slide2.py`

```python
from pyzlides import BodyText, Img

slide = BodyText("Pyzlides allows you to create presentations in Python.") + Img("image_path.jpg", "Example Image")
```

### `slide3.py`

```python
from pyzlides import BodyText, Bold, Bottom

slide = Bottom(BodyText("This is a " + Bold("bold") + " statement."))
```

---

## Commands

### `generate_pdf` Command

This command will process all slide Python files, generate a PDF using the specified configurations, and output the presentation.

```bash
python pyzlides.py generate_pdf
```

### Workflow

1. **Reading the Config**: The `generate_pdf` command reads the `config.yaml` file to determine the theme settings and slide order.
2. **Importing Slide Files**: The command imports the slide Python files specified in the `slide_order` section of the config.
3. **Generating the PDF**: For each slide, it renders the elements defined in the Python file and assembles them into the final PDF.

---

## Sample Code

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pyzlides import Slide, Head1, BodyText, Img

class PyzlidesPDF:
    def __init__(self, output_file="presentation.pdf"):
        self.output_file = output_file
        self.c = canvas.Canvas(self.output_file, pagesize=letter)

    def render_slide(self, slide: Slide):
        for element in slide.elements:
            element.render(self.c)
        self.c.showPage()

    def generate(self, slides: List[Slide]):
        for slide in slides:
            self.render_slide(slide)
        self.c.save()
```

---

## Tech Plan

### Step 1: Define the Base Classes

Start by defining the base classes for slide elements (e.g., `Head1`, `BodyText`, `Img`, `Bold`). Each class will have a method `render` that will handle the actual drawing on the canvas.

### Step 2: Build the Slide Class

The `Slide` class should accept a list of elements, arrange them according to their specified layouts (e.g., center, bottom), and provide a method to render them on the PDF.

### Step 3: Implement the Configuration Parsing

Create a configuration file format (YAML or JSON) to specify theme colors, fonts, and slide order. Parse this file using `PyYAML`.

### Step 4: Implement the PDF Generation Logic

Integrate ReportLab for PDF generation, where each slide's elements will be drawn on the PDF, and the final PDF is saved.

### Step 5: Command Line Tool

Create a command-line tool that can be executed with `python pyzlides.py generate_pdf`, which will parse the config file, process the slides, and generate the final PDF.

### Step 6: Test & Documentation

Ensure that the library is well-tested with example slide configurations and that the documentation is clear and complete.

---
