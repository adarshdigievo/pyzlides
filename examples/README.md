# Pyzlides Examples

This folder contains example presentations demonstrating various features of the Pyzlides library. The `images` folder
stores images used in presentations, including background images and content images.

## Example Presentations

### basic-presentation

Demonstrates simple text slides with headers and body text using a standard white theme.

```bash
cd examples/basic-presentation
python -m pyzlides generate_pdf
```

### custom-background

Shows how to use custom background images and title slide layouts.

```bash
cd examples/custom-background
python -m pyzlides generate_pdf
```

### dark-mode

Demonstrates dark theme configuration with light text on dark backgrounds.

```bash
cd examples/dark-mode
python -m pyzlides generate_pdf
```

### grid-layout

Shows multi-column layouts and complex content organization using GridLayout.

```bash
cd examples/grid-layout
python -m pyzlides generate_pdf
```

### mixed-content

Demonstrates combination of text, images, and various elements with composition techniques.

```bash
cd examples/mixed-content
python -m pyzlides generate_pdf
```

### text-and-code

Shows text wrapping with long content and code blocks with syntax highlighting.

```bash
cd examples/text-and-code
python -m pyzlides generate_pdf
```

### title-slides

Demonstrates title slide layouts and positioning with large header formatting.

```bash
cd examples/title-slides
python -m pyzlides generate_pdf
```

## Images Folder

The `images` folder stores images used in presentations:

- **Background images**: `bg_white.jpg`, `bg_black1.jpg`, `bg_blck2.jpg`
- **Content images**: `cat.jpg`, `dog.jpg`

## Running Examples

Each example folder contains:

- `config.yaml` - Theme and slide configuration
- `slide*.py` - Individual slide definitions
- `presentation.pdf` - Generated output (after running)

To run any example:

1. Navigate to the example directory
2. Run `python -m pyzlides generate_pdf`
3. View the generated `presentation.pdf`

