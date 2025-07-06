from pyzlides import Head3, BodyText, Bold, Bottom

slide = [
    Head3("Color Customization", "#E91E63"),
    BodyText("You can customize colors for any element:"),
    BodyText(""),
    BodyText("• " + Bold("Headers", "#FF5722") + " with custom colors"),
    BodyText("• " + Bold("Body text", "#2196F3") + " in different shades"),
    BodyText("• " + Bold("Bold text", "#4CAF50") + " for emphasis"),
    BodyText(""),
    Bottom(BodyText("Mix and match to create stunning presentations!", "#9C27B0"))
]