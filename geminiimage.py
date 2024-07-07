from dotenv import load_dotenv ##Library for load the environment variable
import streamlit as st # For building user interface
import os # To get the gemini apikey
from PIL import Image # To import image
import google.generativeai as genai #Import google ai model

load_dotenv() ## This will load all the environment environment from .env

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Gemini-pro-vision
model = genai.GenerativeModel("gemini-pro-vision")

#Get response from gemini
def get_gemini_response(input,image,prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text


#Function that take an image and convert it to bites
def input_image_setup(uploaded_file):
    if uploaded_file is not None : 
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                'mime_type':uploaded_file.type,
                'data':bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("File not uploaded")



st.set_page_config(page_title="Gemini-Vision-Pro",
                   page_icon='🤖',
                   initial_sidebar_state='collapsed')

st.header("Genimi-Vision-Pro-🤖")

input = st.text_input("Input prompt: " , key='input')
uploaded_file = st.file_uploader('Choose an image...', type=['jpg','jpeg','png'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

submit = st.button('Submit')

input_prompt = """
    You are an expert in understanding invoices. We will upload a image as invoice and you will have
    to answer any questions based on the uploaded invoice image
"""

#If submit button button is clicked
if submit:
    image = input_image_setup(uploaded_file) 
    response = get_gemini_response(input_prompt, image, input)
    st.subheader('The response is :')
    st.write(response)


