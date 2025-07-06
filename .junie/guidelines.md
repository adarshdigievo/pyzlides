# Project Guidelines

## Project Overview

**Pyzlides** is a Python library that allows users to generate presentation slides in PDF format using Python code. The library enables declarative slide creation through Python classes and supports customizable themes, layouts, and slide ordering via configuration files.

### Key Features
- **Declarative Slide Creation**: Define slides using Python classes (`Head1`, `BodyText`, `Img`, `Bold`, etc.)
- **Custom Layouts**: Position elements using layout classes (`Center`, `Bottom`, etc.)
- **Configurable Themes**: Specify colors, fonts, and backgrounds via YAML configuration
- **Slide Ordering**: Define slide sequence through configuration files
- **PDF Output**: Generate presentations in standard PPT resolution using ReportLab

## Project Structure

```
project_root/
├── pyproject.toml          # Project dependencies and metadata
├── readme.md              # Comprehensive project documentation
├── uv.lock               # Lock file for dependencies
├── pyzlides.py           # Main command-line tool
├── config.yaml           # Theme and slide ordering configuration
├── slide1.py, slide2.py  # Individual slide definition files
└── .junie/
    └── guidelines.md     # This file
```

### Core Components
- **Base Slide Elements**: `Head1`, `BodyText`, `Img`, `Bold` classes for content
- **Layout Classes**: `Center`, `Bottom` for element positioning
- **Slide Class**: Container for ordered list of elements
- **Configuration Class**: Handles YAML config parsing
- **PDF Generator**: Uses ReportLab for PDF creation

## Dependencies

The project requires:
- **ReportLab**: For PDF slide generation
- **Pillow**: For image handling in slides
- **PyYAML**: For configuration file parsing

## Running the Project

### Main Command
```bash
python pyzlides.py generate_pdf
```

### Workflow
1. Reads `config.yaml` for theme settings and slide order
2. Imports slide Python files specified in configuration
3. Renders elements and assembles final PDF presentation

## Testing Guidelines

- Test slide element rendering with various content types
- Verify PDF generation with different themes and layouts
- Test configuration file parsing with valid/invalid YAML
- Validate slide ordering and element positioning
- Test image handling and caption rendering

## Code Style Guidelines

- Follow Python PEP 8 conventions
- Use descriptive class names for slide elements
- Keep slide definition files simple and focused
- Use type hints for method parameters
- Document complex rendering logic
- Maintain separation between slide content and presentation logic

## Development Notes

- Each slide should be defined in a separate Python file
- Configuration changes require regenerating the PDF
- New slide elements should extend base classes
- Layout classes should handle positioning logic
- Theme customization is done through YAML configuration
