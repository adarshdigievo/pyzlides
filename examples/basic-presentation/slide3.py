from pyzlides import Head3, BodyText, Bold, Bottom

slide = [
    Head3("Getting Started", "#2E86AB"),
    BodyText("1. Install the library: " + Bold("pip install pyzlides")),
    BodyText("2. Create slide files using Python classes"),
    BodyText("3. Configure themes in " + Bold("config.yaml")),
    BodyText("4. Generate PDF: " + Bold("python -m pyzlides generate_pdf")),
    Bottom(BodyText("Thank you for using Pyzlides!", "#666666"))
]