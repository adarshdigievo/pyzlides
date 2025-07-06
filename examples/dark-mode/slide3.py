from pyzlides import Head3, BodyText, Bold, Center

slide = [
    Head3("Customization Options"),
    BodyText("Change colors in " + Bold("config.yaml", "#00D4AA") + ":"),
    BodyText(""),
    BodyText("background_color: \"#1A1A1A\"", "#A0A0A0"),
    BodyText("font_color: \"#FFFFFF\"", "#A0A0A0"),
    BodyText("header_color: \"#00D4AA\"", "#A0A0A0"),
    BodyText(""),
    Center(BodyText("Perfect for developer presentations!", "#00D4AA"))
]
