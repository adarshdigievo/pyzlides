from pyzlides import Head2, BodyText, Img, Bold

slide = [
    Head2("Title with Image and Text"),
    BodyText("This slide demonstrates how to combine:"),
    BodyText("• " + Bold("Headers") + " for section titles"),
    BodyText("• " + Bold("Images") + " for visual content"),
    BodyText("• " + Bold("Text") + " for detailed explanations"),
    Img("../images/dog.jpg", "A friendly dog image")
]
