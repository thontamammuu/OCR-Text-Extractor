import streamlit as st
import easyocr
import fitz
import numpy as np
from PIL import Image


st.title("📄 Document & Image OCR")


reader = easyocr.Reader(["en"])


def ocr(img):
    text = reader.readtext(
        np.array(img),
        detail=0
    )
    return "\n".join(text)


def pdf_ocr(file):

    doc = fitz.open(
        stream=file.read(),
        filetype="pdf"
    )

    text=""

    for page in doc:

        pix = page.get_pixmap(
            dpi=200
        )

        img = Image.frombytes(
            "RGB",
            [pix.width,pix.height],
            pix.samples
        )

        text += ocr(img)+"\n"

    return text



def image_ocr(file):

    img = Image.open(file)

    st.image(
        img,
        caption="Uploaded Image"
    )

    return ocr(img)



file = st.file_uploader(
    "Upload PDF/Image",
    type=["pdf","jpg","jpeg","png"]
)


if file:

    if file.name.endswith(".pdf"):
        text = pdf_ocr(file)

    else:
        text=image_ocr(file)


    st.text_area(
        "Extracted Text",
        text,
        height=300
    )