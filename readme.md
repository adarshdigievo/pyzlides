# Pyzlides: Python Presentation Creator

> Note: This project was entirely vibe coded using [Jetbrains Junie](https://www.jetbrains.com/junie/) agent on Pycharm IDE.

Pyzlides is a powerful Python library that allows you to create beautiful presentation slides in PDF format using declarative Python code. Generate professional presentations with customizable themes, layouts, and rich content including text, images, code blocks with syntax highlighting, and more.

## Features

- **Declarative Slide Creation**: Define slides using intuitive Python classes
- **Rich Text Elements**: Headers (H1, H2, H3), body text, bold formatting
- **Code Syntax Highlighting**: Support for multiple programming languages using Pygments
- **Image Support**: Include images with captions
- **Flexible Layouts**: Center, bottom positioning, title slides, and grid layouts
- **Custom Backgrounds**: Use custom background images
- **Configurable Themes**: Customize colors, fonts, and styling via YAML configuration
- **Automatic Text Wrapping**: Handles long text gracefully
- **PDF Output**: Generates presentations in standard presentation resolution

## Installation

### Prerequisites

- Python 3.13 or higher

### Install Dependencies

```bash
pip install pillow pygments pyyaml reportlab
```

### Local Installation

1. Clone or download the project
2. Navigate to the project directory
3. Install dependencies as shown above

## Quick Start

1. **Create slide files** (e.g., `slide1.py`):
```python
from pyzlides import Head1, BodyText, Center

slide = [
    Center(Head1("Welcome to Pyzlides")),
    BodyText("Create beautiful presentations with Python!")
]
```

2. **Create a configuration file** (`config.yaml`):
```yaml
theme:
  background_color: "#FFFFFF"
  font_color: "#000000"
  font_size: 24
  header_color: "#2E86AB"
  header_font_size: 48
  font: "Helvetica"

slide_order:
  - "slide1.py"
```

3. **Generate your presentation**:
```bash
python -m pyzlides generate_pdf
```

This creates `presentation.pdf` in your current directory.

## Slide Elements

### Text Elements

#### Headers
```python
from pyzlides import Head1, Head2, Head3

# Large header (typically for titles)
Head1("Main Title")

# Medium header (for section titles)
Head2("Section Title")

# Small header (for subsections)
Head3("Subsection Title")
```

#### Body Text and Formatting
```python
from pyzlides import BodyText, Bold

# Regular paragraph text
BodyText("This is regular body text.")

# Bold text (can be combined with other elements)
BodyText("This text has " + Bold("bold formatting") + " in it.")

# Bullet points
BodyText("• First bullet point")
BodyText("• Second bullet point")
```

### Code Blocks

```python
from pyzlides import Code

# Python code with syntax highlighting
Code("""
def hello_world():
    print("Hello, World!")
    return "success"
""", "python")

# JavaScript code
Code("""
function greetUser(name) {
    console.log(`Hello, ${name}!`);
}
""", "javascript")

# Code without language specification (no highlighting)
Code("echo 'Hello World'")
```

### Images

```python
from pyzlides import Img

# Image with caption
Img("path/to/image.jpg", "Image caption")

# Image without caption
Img("path/to/image.jpg")
```

### Layout Elements

#### Center Layout
```python
from pyzlides import Center, Head1

# Center any element on the slide
slide = [
    Center(Head1("Centered Title"))
]
```

#### Bottom Layout
```python
from pyzlides import Bottom, BodyText

# Position element at bottom of slide
slide = [
    BodyText("Main content here"),
    Bottom(BodyText("Footer text"))
]
```

#### Title Slide Layout
```python
from pyzlides import TitleSlide, Head1

# Special layout for title slides
slide = [
    TitleSlide(Head1("Presentation Title"))
]
```

#### Grid Layout
```python
from pyzlides import GridLayout, BodyText, Img

# Create multi-column layouts
left_content = BodyText("Left column") + Img("image1.jpg")
right_content = BodyText("Right column") + Img("image2.jpg")

slide = [
    GridLayout([left_content, right_content], columns=2)
]
```

### Background Elements

```python
from pyzlides import BackgroundImage

# Custom background image
slide = [
    BackgroundImage("path/to/background.jpg"),
    # ... other slide content
]
```

## Combining Elements

Elements can be combined using the `+` operator:

```python
from pyzlides import BodyText, Bold, Img

# Combine multiple elements
combined_content = (
    BodyText("Introduction text") + 
    Bold("Important note") + 
    Img("diagram.jpg", "Process diagram")
)

slide = [combined_content]
```

## Configuration File

The `config.yaml` file controls themes and slide ordering:

```yaml
theme:
  # Background and text colors
  background_color: "#FFFFFF"
  font_color: "#000000"
  
  # Font settings
  font: "Helvetica"
  font_size: 24
  
  # Header styling
  header_color: "#2E86AB"
  header_font_size: 48

# Define slide order
slide_order:
  - "slide1.py"
  - "slide2.py"
  - "slide3.py"
```

### Theme Options

- `background_color`: Slide background color (hex format)
- `font_color`: Default text color (hex format)
- `font`: Font family (e.g., "Helvetica", "Times-Roman")
- `font_size`: Default font size for body text
- `header_color`: Color for header elements (hex format)
- `header_font_size`: Font size for H1 headers

## Command Line Usage

### Generate PDF
```bash
# From project root
python -m pyzlides generate_pdf

# Alternative syntax
python pyzlides.py generate_pdf
```

### Running from Different Directories

If running from a subdirectory (like examples), update your `config.yaml` paths accordingly:

```yaml
slide_order:
  - "../slides/slide1.py"
  - "../slides/slide2.py"
```

## Examples

The `examples/` folder contains several demonstration presentations:

### Basic Presentation (`examples/basic-presentation/`)
- Simple text slides with headers and body text
- Demonstrates basic layout and formatting

### Text and Code (`examples/text-and-code/`)
- Text wrapping with long content
- Code blocks with syntax highlighting
- Mixed formatting examples

### Mixed Content (`examples/mixed-content/`)
- Combination of text, images, and various elements
- Shows element composition techniques

### Custom Background (`examples/custom-background/`)
- Custom background images
- Title slide layouts
- Background image positioning

### Grid Layout (`examples/grid-layout/`)
- Multi-column layouts
- Complex content organization
- Column-based design patterns

### Dark Mode (`examples/dark-mode/`)
- Dark theme configuration
- Light text on dark backgrounds
- Theme customization examples

### Title Slides (`examples/title-slides/`)
- Title slide layouts and positioning
- Large header formatting
- Presentation opening slides

### Running Examples

```bash
# Navigate to any example directory
cd examples/basic-presentation

# Generate the presentation
python -m pyzlides generate_pdf

# View the generated presentation.pdf
```

Each example includes:
- `config.yaml` - Theme and slide configuration
- `slide*.py` - Individual slide definitions
- `presentation.pdf` - Generated output (after running)

## Advanced Usage

### Custom Slide Classes

You can create reusable slide templates:

```python
from pyzlides import Head1, BodyText, Center, Bottom

def title_slide(title, subtitle):
    return [
        Center(Head1(title)),
        Center(BodyText(subtitle))
    ]

def content_slide(title, content_list):
    elements = [Head2(title)]
    for item in content_list:
        elements.append(BodyText(f"• {item}"))
    return elements

# Usage
slide = title_slide("My Presentation", "Subtitle Here")
```

### Dynamic Content

Generate slides programmatically:

```python
from pyzlides import Head2, BodyText, Code

# Generate slides from data
data_points = ["Point 1", "Point 2", "Point 3"]

slide = [Head2("Data Overview")]
for point in data_points:
    slide.append(BodyText(f"• {point}"))
```

## Troubleshooting

### Common Issues

1. **"Slide file not found" error**
   - Check that slide file paths in `config.yaml` are correct
   - Ensure slide files exist in the specified locations

2. **"No slide files specified" error**
   - Verify your `config.yaml` has a `slide_order` section
   - Check YAML syntax is correct

3. **Image not displaying**
   - Verify image file paths are correct and accessible
   - Supported formats: JPG, PNG, GIF

4. **Font issues**
   - Use standard fonts like "Helvetica", "Times-Roman"
   - Check font name spelling in config.yaml

### Getting Help

- Check the examples folder for usage patterns
- Verify your Python version is 3.13 or higher
- Ensure all dependencies are installed correctly

## Contributing

Pyzlides is designed to be extensible. You can:

- Add new slide element types by extending `BaseElement`
- Create custom layout classes
- Contribute new themes and examples
- Improve documentation and examples

## License

This project is open source. Please check the project repository for license details.