from pyzlides import Head3, BodyText, BackgroundImage, Center

slide = [
    BackgroundImage("../images/bg_blck2.jpg"),
    Head3("Usage Instructions"),
    BodyText("1. Add BackgroundImage() as the first element"),
    BodyText("2. Specify the image file path"),
    BodyText("3. Add your content elements"),
    BodyText("4. Adjust text colors for visibility"),
    BodyText(""),
    Center(BodyText("Create stunning visual presentations!", "#FFD700"))
]
