from pyzlides import Head2, BodyText, Bold

slide = [
    Head2("Text Wrapping Demo - This is a very long heading that should automatically wrap to the next line when it exceeds the available width of the slide"),
    BodyText("This is a demonstration of automatic text wrapping functionality. When text becomes too long to fit within the available width of the slide, it should automatically wrap to the next line. This ensures that no text flows out of the visible area and maintains proper margins on all sides of the slide."),
    BodyText("Here's another paragraph with " + Bold("bold text that is also very long and should wrap properly when it exceeds the available width") + " to test mixed formatting with text wrapping."),
    BodyText("• This is a bullet point with extremely long text that should demonstrate how bullet points and other formatted text elements handle automatic line wrapping when the content is too wide for the slide"),
    BodyText("• Another bullet point to show consistent behavior"),
    BodyText("• And a third one with " + Bold("bold formatting") + " mixed in")
]