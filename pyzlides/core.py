from typing import List, Union, Any
import yaml
import importlib.util
import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from PIL import Image
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import get_formatter_by_name
from pygments.util import ClassNotFound

# Define 16:9 aspect ratio page size (1920x1080 points scaled down)
SLIDE_16_9 = (792, 445.5)  # 16:9 ratio in points (11 x 6.1875 inches)

# Default margins for slides
DEFAULT_MARGIN_LEFT = 50
DEFAULT_MARGIN_RIGHT = 50
DEFAULT_MARGIN_TOP = 50
DEFAULT_MARGIN_BOTTOM = 50


def wrap_text(canvas_obj, text: str, font_name: str, font_size: int, max_width: float) -> List[str]:
    """
    Wrap text to fit within the specified width.
    Returns a list of lines that fit within the max_width.
    """
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        # Test if adding this word would exceed the width
        test_line = current_line + (" " if current_line else "") + word
        text_width = canvas_obj.stringWidth(test_line, font_name, font_size)

        if text_width <= max_width:
            current_line = test_line
        else:
            # If current line is not empty, save it and start new line
            if current_line:
                lines.append(current_line)
                current_line = word
            else:
                # Single word is too long, break it
                lines.append(word)
                current_line = ""

    # Add the last line if it's not empty
    if current_line:
        lines.append(current_line)

    return lines


def get_available_width() -> float:
    """Get the available width for text content considering margins."""
    return SLIDE_16_9[0] - DEFAULT_MARGIN_LEFT - DEFAULT_MARGIN_RIGHT


class BaseElement:
    """Base class for all slide elements"""

    def __init__(self):
        pass

    def render(self, canvas_obj, x: float, y: float, theme: dict) -> float:
        """Render the element on the canvas and return the height used"""
        pass

    def __add__(self, other):
        """Support for + operator to combine elements"""
        if isinstance(other, BaseElement):
            return CombinedElement([self, other])
        return NotImplemented


class CombinedElement(BaseElement):
    """Element that combines multiple elements"""

    def __init__(self, elements: List[BaseElement]):
        super().__init__()
        self.elements = elements

    def render(self, canvas_obj, x: float, y: float, theme: dict) -> float:
        total_height = 0
        current_y = y
        for element in self.elements:
            height = element.render(canvas_obj, x, current_y, theme)
            current_y -= height
            total_height += height
        return total_height

    def __add__(self, other):
        if isinstance(other, BaseElement):
            return CombinedElement(self.elements + [other])
        return NotImplemented


class Head1(BaseElement):
    """Header element with large font size"""

    def __init__(self, text: str, color: str = None):
        super().__init__()
        self.text = text
        self.color = color

    def render(self, canvas_obj, x: float, y: float, theme: dict) -> float:
        font_name = theme.get('font', 'Helvetica') + '-Bold'
        font_size = theme.get('header_font_size', 48)
        canvas_obj.setFont(font_name, font_size)
        color = self.color if self.color else theme.get('header_color', '#FF5733')
        canvas_obj.setFillColor(HexColor(color))

        # Calculate available width considering margins
        max_width = get_available_width()
        lines = wrap_text(canvas_obj, self.text, font_name, font_size, max_width)

        # Render each line
        current_y = y
        for line in lines:
            canvas_obj.drawString(x, current_y, line)
            current_y -= font_size + 5  # Line spacing

        # Return total height used
        total_height = len(lines) * (font_size + 5) + 5  # Extra spacing after element
        return total_height

    def __add__(self, other):
        if isinstance(other, str):
            return Head1(self.text + other, self.color)
        return super().__add__(other)


class Head2(BaseElement):
    """Secondary header element with medium font size"""

    def __init__(self, text: str, color: str = None):
        super().__init__()
        self.text = text
        self.color = color

    def render(self, canvas_obj, x: float, y: float, theme: dict) -> float:
        font_name = theme.get('font', 'Helvetica') + '-Bold'
        font_size = theme.get('header_font_size', 48) * 0.75  # 75% of H1 size
        canvas_obj.setFont(font_name, font_size)
        color = self.color if self.color else theme.get('header_color', '#FF5733')
        canvas_obj.setFillColor(HexColor(color))

        # Calculate available width considering margins
        max_width = get_available_width()
        lines = wrap_text(canvas_obj, self.text, font_name, font_size, max_width)

        # Render each line
        current_y = y
        for line in lines:
            canvas_obj.drawString(x, current_y, line)
            current_y -= font_size + 4  # Line spacing

        # Return total height used
        total_height = len(lines) * (font_size + 4) + 4  # Extra spacing after element
        return total_height

    def __add__(self, other):
        if isinstance(other, str):
            return Head2(self.text + other, self.color)
        return super().__add__(other)


class Head3(BaseElement):
    """Tertiary header element with smaller font size"""

    def __init__(self, text: str, color: str = None):
        super().__init__()
        self.text = text
        self.color = color

    def render(self, canvas_obj, x: float, y: float, theme: dict) -> float:
        font_name = theme.get('font', 'Helvetica') + '-Bold'
        font_size = theme.get('header_font_size', 48) * 0.6  # 60% of H1 size
        canvas_obj.setFont(font_name, font_size)
        color = self.color if self.color else theme.get('header_color', '#FF5733')
        canvas_obj.setFillColor(HexColor(color))

        # Calculate available width considering margins
        max_width = get_available_width()
        lines = wrap_text(canvas_obj, self.text, font_name, font_size, max_width)

        # Render each line
        current_y = y
        for line in lines:
            canvas_obj.drawString(x, current_y, line)
            current_y -= font_size + 3  # Line spacing

        # Return total height used
        total_height = len(lines) * (font_size + 3) + 3  # Extra spacing after element
        return total_height

    def __add__(self, other):
        if isinstance(other, str):
            return Head3(self.text + other, self.color)
        return super().__add__(other)


class BodyText(BaseElement):
    """Body text element with normal font size"""

    def __init__(self, text: str, color: str = None):
        super().__init__()
        self.text = text
        self.color = color

    def render(self, canvas_obj, x: float, y: float, theme: dict) -> float:
        font_name = theme.get('font', 'Helvetica')
        font_size = theme.get('font_size', 24)
        canvas_obj.setFont(font_name, font_size)
        color = self.color if self.color else theme.get('font_color', '#000000')
        canvas_obj.setFillColor(HexColor(color))

        # Calculate available width considering margins
        max_width = get_available_width()
        lines = wrap_text(canvas_obj, self.text, font_name, font_size, max_width)

        # Render each line
        current_y = y
        for line in lines:
            canvas_obj.drawString(x, current_y, line)
            current_y -= font_size + 2  # Line spacing

        # Return total height used
        total_height = len(lines) * (font_size + 2) + 3  # Extra spacing after element
        return total_height

    def __add__(self, other):
        if isinstance(other, str):
            return BodyText(self.text + other, self.color)
        return super().__add__(other)


class Bold(BaseElement):
    """Bold text element"""

    def __init__(self, text: str, color: str = None):
        super().__init__()
        self.text = text
        self.color = color

    def render(self, canvas_obj, x: float, y: float, theme: dict) -> float:
        font_name = theme.get('font', 'Helvetica') + '-Bold'
        font_size = theme.get('font_size', 24)
        canvas_obj.setFont(font_name, font_size)
        color = self.color if self.color else theme.get('font_color', '#000000')
        canvas_obj.setFillColor(HexColor(color))

        # Calculate available width considering margins
        max_width = get_available_width()
        lines = wrap_text(canvas_obj, self.text, font_name, font_size, max_width)

        # Render each line
        current_y = y
        for line in lines:
            canvas_obj.drawString(x, current_y, line)
            current_y -= font_size + 2  # Line spacing

        # Return total height used
        total_height = len(lines) * (font_size + 2) + 3  # Extra spacing after element
        return total_height

    def __add__(self, other):
        if isinstance(other, str):
            return Bold(self.text + other, self.color)
        return super().__add__(other)

    def __radd__(self, other):
        """Support for string + Bold"""
        if isinstance(other, str):
            return other + self.text
        return NotImplemented


class Code(BaseElement):
    """Code element with syntax highlighting"""

    def __init__(self, code: str, language: str = None, background_color: str = "#F5F5F5"):
        super().__init__()
        self.code = code
        self.language = language
        self.background_color = background_color

    def render(self, canvas_obj, x: float, y: float, theme: dict) -> float:
        font_name = "Courier"  # Monospace font for code
        font_size = theme.get('font_size', 24) * 0.8  # Slightly smaller for code

        # Calculate available width considering margins and padding
        max_width = get_available_width() - 20  # Extra padding for code blocks

        # Try to apply syntax highlighting if language is specified
        highlighted_code = self.code
        if self.language:
            try:
                lexer = get_lexer_by_name(self.language, stripall=True)
                # Use a simple formatter that just adds basic coloring
                # For PDF, we'll implement basic syntax highlighting with colors
                highlighted_code = self._apply_basic_highlighting(self.code, self.language)
            except ClassNotFound:
                # If language not found, use plain text
                highlighted_code = self.code

        # Split code into lines - preserve original spacing and indentation
        code_lines = highlighted_code.split('\n')

        # Remove only leading and trailing empty lines, but preserve indentation
        while code_lines and not code_lines[0].strip():
            code_lines.pop(0)
        while code_lines and not code_lines[-1].strip():
            code_lines.pop()

        # Calculate total height needed
        line_height = font_size + 2
        padding = 10
        total_content_height = len(code_lines) * line_height + (2 * padding)

        # Draw background rectangle
        canvas_obj.setFillColor(HexColor(self.background_color))
        canvas_obj.rect(x - 10, y - total_content_height + padding, 
                       max_width + 20, total_content_height, fill=1, stroke=1)

        # Set text color for code
        canvas_obj.setFillColor(HexColor(theme.get('font_color', '#000000')))
        canvas_obj.setFont(font_name, font_size)

        # Render each line of code with basic syntax highlighting
        current_y = y - padding
        for line in code_lines:
            # For code, preserve original spacing and don't wrap unless absolutely necessary
            # Check if line fits within max_width
            line_width = canvas_obj.stringWidth(line, font_name, font_size)
            if line_width <= max_width:
                # Line fits, render as-is to preserve spacing
                self._render_highlighted_line(canvas_obj, line, x, current_y, font_name, font_size, theme)
                current_y -= line_height
            else:
                # Line is too long, but preserve indentation when wrapping
                wrapped_lines = self._wrap_code_line(canvas_obj, line, font_name, font_size, max_width)
                for wrapped_line in wrapped_lines:
                    self._render_highlighted_line(canvas_obj, wrapped_line, x, current_y, font_name, font_size, theme)
                    current_y -= line_height

        return total_content_height + 10  # Extra spacing after code block

    def _wrap_code_line(self, canvas_obj, line: str, font_name: str, font_size: int, max_width: float) -> List[str]:
        """Wrap a code line while preserving indentation"""
        # Get the leading whitespace (indentation)
        leading_whitespace = ""
        for char in line:
            if char in [' ', '\t']:
                leading_whitespace += char
            else:
                break

        # If the line is just whitespace, return it as-is
        if not line.strip():
            return [line]

        # Try to fit the line as-is first
        if canvas_obj.stringWidth(line, font_name, font_size) <= max_width:
            return [line]

        # If line is too long, we need to wrap it
        # For code, we'll break at reasonable points (spaces, operators) when possible
        wrapped_lines = []
        remaining_line = line

        while remaining_line:
            # Calculate how much we can fit
            current_line = ""
            i = 0

            # For continuation lines, add some indentation
            if wrapped_lines:
                indent = leading_whitespace + "    "  # Add 4 spaces for continuation
            else:
                indent = leading_whitespace

            # Start with the indentation
            current_line = indent
            remaining_content = remaining_line.lstrip() if wrapped_lines else remaining_line[len(leading_whitespace):]

            # Add characters until we exceed the width
            for i, char in enumerate(remaining_content):
                test_line = current_line + char
                if canvas_obj.stringWidth(test_line, font_name, font_size) <= max_width:
                    current_line = test_line
                else:
                    break
            else:
                # We fit the entire remaining content
                wrapped_lines.append(current_line)
                break

            # Find a good break point (prefer spaces, then operators)
            break_point = i
            for j in range(i, max(0, i - 20), -1):  # Look back up to 20 characters
                if remaining_content[j] in [' ', '\t', ',', ';', '(', ')', '[', ']', '{', '}']:
                    break_point = j + 1
                    break

            # If we couldn't find a good break point, just break at the limit
            if break_point == i and i > 0:
                break_point = i

            # Add the current line
            wrapped_lines.append(current_line[:len(indent) + break_point])

            # Update remaining line
            remaining_line = remaining_content[break_point:].lstrip()
            if not remaining_line:
                break

        return wrapped_lines

    def _apply_basic_highlighting(self, code: str, language: str) -> str:
        """Apply basic syntax highlighting by identifying keywords and strings"""
        # For now, return the original code - we'll implement basic highlighting
        # This is a simplified approach since ReportLab doesn't support rich text easily
        return code

    def _render_highlighted_line(self, canvas_obj, line: str, x: float, y: float, font_name: str, font_size: int, theme: dict):
        """Render a line of code with basic syntax highlighting"""
        # Define color scheme for different elements
        colors = {
            'keyword': '#0000FF',      # Blue for keywords
            'string': '#008000',       # Green for strings
            'comment': '#808080',      # Gray for comments
            'number': '#FF6600',       # Orange for numbers
            'default': theme.get('font_color', '#000000')  # Default text color
        }

        # Simple syntax highlighting based on patterns
        current_x = x
        i = 0
        while i < len(line):
            char = line[i]

            # Check for comments
            if char == '#' or (char == '/' and i + 1 < len(line) and line[i + 1] == '/'):
                # Rest of line is a comment
                comment_text = line[i:]
                canvas_obj.setFillColor(HexColor(colors['comment']))
                canvas_obj.drawString(current_x, y, comment_text)
                break

            # Check for strings
            elif char in ['"', "'"]:
                quote_char = char
                string_start = i
                i += 1
                # Find end of string
                while i < len(line) and line[i] != quote_char:
                    if line[i] == '\\' and i + 1 < len(line):  # Handle escaped characters
                        i += 2
                    else:
                        i += 1
                if i < len(line):
                    i += 1  # Include closing quote

                string_text = line[string_start:i]
                canvas_obj.setFillColor(HexColor(colors['string']))
                canvas_obj.drawString(current_x, y, string_text)
                current_x += canvas_obj.stringWidth(string_text, font_name, font_size)
                continue

            # Check for numbers
            elif char.isdigit():
                number_start = i
                while i < len(line) and (line[i].isdigit() or line[i] == '.'):
                    i += 1

                number_text = line[number_start:i]
                canvas_obj.setFillColor(HexColor(colors['number']))
                canvas_obj.drawString(current_x, y, number_text)
                current_x += canvas_obj.stringWidth(number_text, font_name, font_size)
                continue

            # Check for keywords (basic set)
            elif char.isalpha() or char == '_':
                word_start = i
                while i < len(line) and (line[i].isalnum() or line[i] == '_'):
                    i += 1

                word = line[word_start:i]

                # Define basic keywords for common languages
                keywords = {
                    'python': ['def', 'class', 'if', 'else', 'elif', 'for', 'while', 'import', 'from', 'return', 'try', 'except', 'finally', 'with', 'as', 'and', 'or', 'not', 'in', 'is', 'lambda', 'yield', 'global', 'nonlocal', 'True', 'False', 'None'],
                    'javascript': ['function', 'var', 'let', 'const', 'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'default', 'break', 'continue', 'return', 'try', 'catch', 'finally', 'throw', 'new', 'this', 'typeof', 'instanceof', 'true', 'false', 'null', 'undefined'],
                    'java': ['public', 'private', 'protected', 'static', 'final', 'class', 'interface', 'extends', 'implements', 'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'default', 'break', 'continue', 'return', 'try', 'catch', 'finally', 'throw', 'throws', 'new', 'this', 'super', 'true', 'false', 'null']
                }

                language_keywords = keywords.get(self.language, [])

                if word in language_keywords:
                    canvas_obj.setFillColor(HexColor(colors['keyword']))
                else:
                    canvas_obj.setFillColor(HexColor(colors['default']))

                canvas_obj.drawString(current_x, y, word)
                current_x += canvas_obj.stringWidth(word, font_name, font_size)
                continue

            # Default character rendering
            else:
                canvas_obj.setFillColor(HexColor(colors['default']))
                canvas_obj.drawString(current_x, y, char)
                current_x += canvas_obj.stringWidth(char, font_name, font_size)
                i += 1

    def __add__(self, other):
        if isinstance(other, str):
            return Code(self.code + other, self.language, self.background_color)
        return super().__add__(other)


class Img(BaseElement):
    """Image element with optional caption"""

    def __init__(self, path: str, caption: str = ""):
        super().__init__()
        self.path = path
        self.caption = caption

    def render(self, canvas_obj, x: float, y: float, theme: dict) -> float:
        try:
            if os.path.exists(self.path):
                # Load and draw image
                img = ImageReader(self.path)
                img_width, img_height = img.getSize()

                # Scale image to fit within reasonable bounds
                max_width = 400
                max_height = 300

                scale = min(max_width / img_width, max_height / img_height, 1.0)
                scaled_width = img_width * scale
                scaled_height = img_height * scale

                canvas_obj.drawImage(img, x, y - scaled_height, scaled_width, scaled_height)

                total_height = scaled_height

                # Add caption if provided
                if self.caption:
                    canvas_obj.setFont(theme.get('font', 'Helvetica'), theme.get('font_size', 20))
                    canvas_obj.setFillColor(HexColor(theme.get('font_color', '#000000')))
                    canvas_obj.drawString(x, y - scaled_height - 25, self.caption)
                    total_height += 30

                return total_height
            else:
                # If image doesn't exist, render placeholder text
                canvas_obj.setFont(theme.get('font', 'Helvetica'), theme.get('font_size', 24))
                canvas_obj.setFillColor(HexColor('#FF0000'))
                canvas_obj.drawString(x, y, f"[Image not found: {self.path}]")
                if self.caption:
                    canvas_obj.drawString(x, y - 30, self.caption)
                    return 60
                return 30
        except Exception as e:
            # Error handling - render error message
            canvas_obj.setFont(theme.get('font', 'Helvetica'), theme.get('font_size', 24))
            canvas_obj.setFillColor(HexColor('#FF0000'))
            canvas_obj.drawString(x, y, f"[Error loading image: {str(e)}]")
            return 30


class Center(BaseElement):
    """Layout class to center an element"""

    def __init__(self, element: BaseElement):
        super().__init__()
        self.element = element

    def render(self, canvas_obj, x: float, y: float, theme: dict) -> float:
        # Center the element horizontally within available width
        page_width = SLIDE_16_9[0]
        available_width = page_width - DEFAULT_MARGIN_LEFT - DEFAULT_MARGIN_RIGHT

        # Calculate proper center position
        center_x = DEFAULT_MARGIN_LEFT + (available_width / 2)

        # For text elements, we need to adjust based on estimated text width
        if isinstance(self.element, (Head1, Head2, Head3, BodyText, Bold)):
            estimated_text_width = self._estimate_text_width(self.element, canvas_obj, theme)
            # Adjust center position to account for text width
            center_x = max(DEFAULT_MARGIN_LEFT, center_x - (estimated_text_width / 2))
            # Ensure text doesn't go beyond right margin
            center_x = min(center_x, page_width - DEFAULT_MARGIN_RIGHT - estimated_text_width)

        return self.element.render(canvas_obj, center_x, y, theme)

    def _estimate_text_width(self, element: BaseElement, canvas_obj, theme: dict) -> float:
        """Estimate the width of text elements"""
        if isinstance(element, Head1):
            font_name = theme.get('font', 'Helvetica') + '-Bold'
            font_size = theme.get('header_font_size', 48)
            return canvas_obj.stringWidth(element.text, font_name, font_size)
        elif isinstance(element, Head2):
            font_name = theme.get('font', 'Helvetica') + '-Bold'
            font_size = theme.get('header_font_size', 48) * 0.75
            return canvas_obj.stringWidth(element.text, font_name, font_size)
        elif isinstance(element, Head3):
            font_name = theme.get('font', 'Helvetica') + '-Bold'
            font_size = theme.get('header_font_size', 48) * 0.6
            return canvas_obj.stringWidth(element.text, font_name, font_size)
        elif isinstance(element, (BodyText, Bold)):
            font_name = theme.get('font', 'Helvetica')
            if isinstance(element, Bold):
                font_name += '-Bold'
            font_size = theme.get('font_size', 24)
            return canvas_obj.stringWidth(element.text, font_name, font_size)
        return 0


class Bottom(BaseElement):
    """Layout class to position an element at the bottom"""

    def __init__(self, element: BaseElement):
        super().__init__()
        self.element = element

    def render(self, canvas_obj, x: float, y: float, theme: dict) -> float:
        # Position at bottom of page
        bottom_y = 50  # 50 points from bottom
        return self.element.render(canvas_obj, x, bottom_y, theme)


class TitleSlide(BaseElement):
    """Layout class to center an element both horizontally and vertically (for title slides)"""

    def __init__(self, element: BaseElement):
        super().__init__()
        self.element = element

    def render(self, canvas_obj, x: float, y: float, theme: dict) -> float:
        # Center the element both horizontally and vertically
        page_width = SLIDE_16_9[0]
        page_height = SLIDE_16_9[1]
        available_width = page_width - DEFAULT_MARGIN_LEFT - DEFAULT_MARGIN_RIGHT

        # Calculate proper center positions
        center_y = page_height / 2  # Vertical center

        # For text elements, adjust horizontal position based on text width
        if isinstance(self.element, (Head1, Head2, Head3, BodyText, Bold)):
            estimated_text_width = self._estimate_text_width(self.element, canvas_obj, theme)
            # Center the text properly - start position should be center minus half text width
            center_x = (page_width / 2) - (estimated_text_width / 2)
            # Only constrain if text would go beyond page boundaries
            center_x = max(DEFAULT_MARGIN_LEFT, center_x)
            center_x = min(center_x, page_width - DEFAULT_MARGIN_RIGHT - estimated_text_width)
        else:
            # For non-text elements, use simple centering
            center_x = DEFAULT_MARGIN_LEFT + (available_width / 2)

        return self.element.render(canvas_obj, center_x, center_y, theme)

    def _estimate_text_width(self, element: BaseElement, canvas_obj, theme: dict) -> float:
        """Estimate the width of text elements accounting for text wrapping"""
        if isinstance(element, Head1):
            font_name = theme.get('font', 'Helvetica') + '-Bold'
            font_size = theme.get('header_font_size', 48)
            max_width = get_available_width()
            lines = wrap_text(canvas_obj, element.text, font_name, font_size, max_width)
            # Return the width of the longest line
            max_line_width = 0
            for line in lines:
                line_width = canvas_obj.stringWidth(line, font_name, font_size)
                max_line_width = max(max_line_width, line_width)
            return max_line_width
        elif isinstance(element, Head2):
            font_name = theme.get('font', 'Helvetica') + '-Bold'
            font_size = theme.get('header_font_size', 48) * 0.75
            max_width = get_available_width()
            lines = wrap_text(canvas_obj, element.text, font_name, font_size, max_width)
            # Return the width of the longest line
            max_line_width = 0
            for line in lines:
                line_width = canvas_obj.stringWidth(line, font_name, font_size)
                max_line_width = max(max_line_width, line_width)
            return max_line_width
        elif isinstance(element, Head3):
            font_name = theme.get('font', 'Helvetica') + '-Bold'
            font_size = theme.get('header_font_size', 48) * 0.6
            max_width = get_available_width()
            lines = wrap_text(canvas_obj, element.text, font_name, font_size, max_width)
            # Return the width of the longest line
            max_line_width = 0
            for line in lines:
                line_width = canvas_obj.stringWidth(line, font_name, font_size)
                max_line_width = max(max_line_width, line_width)
            return max_line_width
        elif isinstance(element, (BodyText, Bold)):
            font_name = theme.get('font', 'Helvetica')
            if isinstance(element, Bold):
                font_name += '-Bold'
            font_size = theme.get('font_size', 24)
            max_width = get_available_width()
            lines = wrap_text(canvas_obj, element.text, font_name, font_size, max_width)
            # Return the width of the longest line
            max_line_width = 0
            for line in lines:
                line_width = canvas_obj.stringWidth(line, font_name, font_size)
                max_line_width = max(max_line_width, line_width)
            return max_line_width
        return 0


class GridLayout(BaseElement):
    """Layout class to arrange elements in a horizontal grid"""

    def __init__(self, elements: List[BaseElement], columns: int = 2):
        super().__init__()
        self.elements = elements
        self.columns = columns

    def render(self, canvas_obj, x: float, y: float, theme: dict) -> float:
        page_width = SLIDE_16_9[0]
        column_width = (page_width - 100) / self.columns  # 50pt margin on each side
        max_height = 0

        for i, element in enumerate(self.elements):
            if i >= self.columns:  # Only render up to the number of columns
                break
            column_x = 50 + (i * column_width)
            height = element.render(canvas_obj, column_x, y, theme)
            max_height = max(max_height, height)

        return max_height


class BackgroundImage(BaseElement):
    """Element to set a background image for the slide"""

    def __init__(self, path: str):
        super().__init__()
        self.path = path

    def render(self, canvas_obj, x: float, y: float, theme: dict) -> float:
        try:
            if os.path.exists(self.path):
                # Load and draw background image
                img = ImageReader(self.path)
                page_width = SLIDE_16_9[0]
                page_height = SLIDE_16_9[1]

                # Draw image to fill entire page
                canvas_obj.drawImage(img, 0, 0, page_width, page_height)
                return 0  # Background doesn't take up space
            else:
                # If image doesn't exist, just return 0
                return 0
        except Exception as e:
            # Error handling - just return 0 for background
            return 0


class Slide:
    """Represents a single slide with ordered list of elements"""

    def __init__(self, elements: Union[BaseElement, List[BaseElement]]):
        if isinstance(elements, list):
            self.elements = elements
        else:
            # Treat as a single element (BaseElement or any object with render method)
            self.elements = [elements]

    def render(self, canvas_obj, theme: dict):
        """Render all elements on the slide"""
        page_height = SLIDE_16_9[1]
        current_y = page_height - DEFAULT_MARGIN_TOP  # Start from top with margin
        bottom_margin = DEFAULT_MARGIN_BOTTOM

        for element in self.elements:
            height = element.render(canvas_obj, DEFAULT_MARGIN_LEFT, current_y, theme)
            current_y -= height + 10  # Add spacing between elements

    def render_with_overflow_detection(self, canvas_obj, theme: dict) -> List['Slide']:
        """Render elements and return multiple slides if content overflows"""
        page_height = SLIDE_16_9[1]
        current_y = page_height - DEFAULT_MARGIN_TOP  # Start from top with margin
        bottom_margin = DEFAULT_MARGIN_BOTTOM

        slides = []
        current_slide_elements = []

        for element in self.elements:
            # Check if this element would fit on the current slide
            # We need to estimate the height first
            estimated_height = self._estimate_element_height(element, theme)

            if current_y - estimated_height - 10 < bottom_margin and current_slide_elements:
                # Element won't fit, create a new slide with current elements
                slides.append(Slide(current_slide_elements))
                current_slide_elements = [element]
                current_y = page_height - DEFAULT_MARGIN_TOP - estimated_height - 10
            else:
                # Element fits on current slide
                current_slide_elements.append(element)
                current_y -= estimated_height + 10

        # Add the last slide if it has elements
        if current_slide_elements:
            slides.append(Slide(current_slide_elements))

        # If no slides were created (all elements fit), return self
        if not slides:
            slides = [self]

        return slides

    def _estimate_element_height(self, element: BaseElement, theme: dict) -> float:
        """Estimate the height an element will take when rendered"""
        # This is a rough estimation - in practice, we might need to render to a dummy canvas
        if isinstance(element, Head1):
            font_size = theme.get('header_font_size', 48)
            # Estimate based on text length and wrapping
            max_width = get_available_width()
            estimated_lines = max(1, len(element.text) * font_size // max_width + 1)
            return estimated_lines * (font_size + 5) + 5
        elif isinstance(element, Head2):
            font_size = theme.get('header_font_size', 48) * 0.75
            max_width = get_available_width()
            estimated_lines = max(1, len(element.text) * font_size // max_width + 1)
            return estimated_lines * (font_size + 4) + 4
        elif isinstance(element, Head3):
            font_size = theme.get('header_font_size', 48) * 0.6
            max_width = get_available_width()
            estimated_lines = max(1, len(element.text) * font_size // max_width + 1)
            return estimated_lines * (font_size + 3) + 3
        elif isinstance(element, BodyText):
            font_size = theme.get('font_size', 24)
            max_width = get_available_width()
            estimated_lines = max(1, len(element.text) * font_size // max_width + 1)
            return estimated_lines * (font_size + 2) + 3
        elif isinstance(element, Bold):
            font_size = theme.get('font_size', 24)
            max_width = get_available_width()
            estimated_lines = max(1, len(element.text) * font_size // max_width + 1)
            return estimated_lines * (font_size + 2) + 3
        elif isinstance(element, Code):
            font_size = theme.get('font_size', 24) * 0.8
            code_lines = element.code.strip().split('\n')
            line_height = font_size + 2
            padding = 10
            return len(code_lines) * line_height + (2 * padding) + 10
        elif isinstance(element, Img):
            return 350  # Rough estimate for image + caption
        elif isinstance(element, Center):
            return self._estimate_element_height(element.element, theme)
        elif isinstance(element, Bottom):
            return self._estimate_element_height(element.element, theme)
        elif isinstance(element, TitleSlide):
            return self._estimate_element_height(element.element, theme)
        elif isinstance(element, GridLayout):
            max_height = 0
            for grid_element in element.elements[:element.columns]:
                height = self._estimate_element_height(grid_element, theme)
                max_height = max(max_height, height)
            return max_height
        elif isinstance(element, BackgroundImage):
            return 0  # Background doesn't take space
        elif hasattr(element, 'elements'):  # CombinedElement
            total_height = 0
            for sub_element in element.elements:
                total_height += self._estimate_element_height(sub_element, theme)
            return total_height
        else:
            return 50  # Default estimate


class Config:
    """Handles configuration file parsing"""

    def __init__(self, config_file: str = "config.yaml"):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self) -> dict:
        """Parse the YAML configuration file"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Warning: Config file {self.config_file} not found. Using defaults.")
            return self.get_default_config()
        except yaml.YAMLError as e:
            print(f"Error parsing config file: {e}")
            return self.get_default_config()

    def get_default_config(self) -> dict:
        """Return default configuration"""
        return {
            'theme': {
                'background_color': '#FFFFFF',
                'font_color': '#000000',
                'font_size': 24,  # Increased from 12 for presentations
                'header_color': '#FF5733',
                'header_font_size': 48,  # Increased from 24 for presentations
                'font': 'Helvetica'
            },
            'slide_order': []
        }

    def get_theme(self) -> dict:
        """Get theme configuration"""
        return self.config.get('theme', {})

    def get_slide_order(self) -> List[str]:
        """Get ordered list of slide files"""
        return self.config.get('slide_order', [])


class PyzlidesPDF:
    """Main PDF generator class"""

    def __init__(self, output_file: str = "presentation.pdf"):
        self.output_file = output_file
        self.canvas = canvas.Canvas(self.output_file, pagesize=SLIDE_16_9)

    def render_slide(self, slide: Slide, theme: dict):
        """Render a single slide"""
        # Set background color
        bg_color = theme.get('background_color', '#FFFFFF')
        self.canvas.setFillColor(HexColor(bg_color))
        self.canvas.rect(0, 0, SLIDE_16_9[0], SLIDE_16_9[1], fill=1, stroke=0)

        # Render slide elements
        slide.render(self.canvas, theme)
        self.canvas.showPage()

    def generate(self, slides: List[Slide], theme: dict):
        """Generate PDF with all slides"""
        total_slides_rendered = 0
        for slide in slides:
            # Use overflow detection to potentially split slides
            overflow_slides = slide.render_with_overflow_detection(None, theme)
            for overflow_slide in overflow_slides:
                self.render_slide(overflow_slide, theme)
                total_slides_rendered += 1
        self.canvas.save()
        print(f"PDF generated: {self.output_file} ({total_slides_rendered} slides)")


def load_slide_from_file(file_path: str) -> Slide:
    """Load a slide from a Python file"""
    try:
        spec = importlib.util.spec_from_file_location("slide_module", file_path)
        slide_module = importlib.util.module_from_spec(spec)

        # Add pyzlides classes to the module's namespace
        slide_module.Head1 = Head1
        slide_module.Head2 = Head2
        slide_module.Head3 = Head3
        slide_module.BodyText = BodyText
        slide_module.Img = Img
        slide_module.Bold = Bold
        slide_module.Code = Code
        slide_module.Center = Center
        slide_module.Bottom = Bottom
        slide_module.TitleSlide = TitleSlide
        slide_module.GridLayout = GridLayout
        slide_module.BackgroundImage = BackgroundImage
        slide_module.Slide = Slide

        spec.loader.exec_module(slide_module)

        if hasattr(slide_module, 'slide'):
            slide_obj = slide_module.slide
            # Check if the object is a list of elements
            if isinstance(slide_obj, list):
                return Slide(slide_obj)
            # Check if the object is an instance of any of the classes we added to the module
            elif (isinstance(slide_obj, slide_module.Head1) or 
                isinstance(slide_obj, slide_module.Head2) or 
                isinstance(slide_obj, slide_module.Head3) or 
                isinstance(slide_obj, slide_module.BodyText) or 
                isinstance(slide_obj, slide_module.Img) or 
                isinstance(slide_obj, slide_module.Bold) or 
                isinstance(slide_obj, slide_module.Code) or 
                isinstance(slide_obj, slide_module.Center) or 
                isinstance(slide_obj, slide_module.Bottom) or 
                isinstance(slide_obj, slide_module.TitleSlide) or 
                isinstance(slide_obj, slide_module.GridLayout) or 
                isinstance(slide_obj, slide_module.BackgroundImage) or 
                hasattr(slide_obj, 'elements')):  # CombinedElement has elements attribute
                return Slide(slide_obj)
            elif isinstance(slide_obj, slide_module.Slide):
                return slide_obj
            else:
                raise ValueError(f"Invalid slide object in {file_path}: {type(slide_obj)}")
        else:
            raise ValueError(f"No 'slide' variable found in {file_path}")

    except Exception as e:
        print(f"Error loading slide from {file_path}: {e}")
        # Return a slide with error message
        return Slide(BodyText(f"Error loading slide: {file_path}"))
