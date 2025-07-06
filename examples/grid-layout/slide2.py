from pyzlides import Head2, BodyText, Img, GridLayout

# Create combined elements for each column
left_column = BodyText("Left Column Content:") + BodyText("• Feature descriptions") + BodyText("• Key benefits") + BodyText("• Important details") + Img("../images/cat.jpg", "Sample Image")

right_column = BodyText("Right Column Content:") + BodyText("• Additional information") + BodyText("• Supporting data") + BodyText("• Visual elements") + Img("../images/dog.jpg", "Another Image")

slide = [
    Head2("Two Column Layout"),
    GridLayout([left_column, right_column], columns=2)
]
