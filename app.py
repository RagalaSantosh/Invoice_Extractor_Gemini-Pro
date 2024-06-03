from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai


print(os.getenv("GOOGLE_API_KEY"))

genai.configure(api_key =os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel("gemini-pro-vision")


def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type":uploaded_file.type,
                "data": bytes_data

            }
        ]

        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


st.set_page_config(page_title = "Invoice Extractor")

st.header("Invoice Extractor")

input = st.text_input("Input Prompt: ", key = "input")
uploaded_image = st.file_uploader("Upload your image invoice", type=['png', 'jpeg', 'jpg'])

image = ""

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption = "Uploaded Image", use_column_width = True)

submit = st.button("Extract the invoice")

input_prompt ="""
You are an expert in understanding of invoices. We will upload an image and you will read
the image and answer the questions which I am going to ask
"""

if submit:

    image_data = input_image_details(uploaded_image)
    response = get_gemini_response(input_prompt, image_data, input)

    st.subheader("The Response is")
    st.write(response)