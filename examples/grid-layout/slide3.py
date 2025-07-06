from pyzlides import Head3, BodyText, Img, GridLayout, Bold

# Create content for three columns
column1 = BodyText("Column 1:") + BodyText("• " + Bold("Design")) + BodyText("• User Interface") + BodyText("• Visual Appeal")

column2 = BodyText("Column 2:") + BodyText("• " + Bold("Development")) + BodyText("• Code Quality") + BodyText("• Performance")

column3 = BodyText("Column 3:") + BodyText("• " + Bold("Testing")) + BodyText("• Quality Assurance") + BodyText("• User Experience")

slide = [
    Head3("Three Column Layout"),
    GridLayout([column1, column2, column3], columns=3),
    BodyText("Grid layouts help organize content efficiently across the slide width")
]