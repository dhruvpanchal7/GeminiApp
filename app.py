from dotenv import load_dotenv
load_dotenv()  

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image

import google.generativeai as genai


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input,image,prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input,image[0],prompt])
    return response.text
    

def input_image_setup(uploaded_file):
    
    if uploaded_file is not None:
       
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")




st.set_page_config(page_title="Gemini Image Processing",layout="wide")
st.markdown("<h1 style='text-align: center'>Gemini App ♊</h1>", unsafe_allow_html=True)
st.markdown("*Upload an image of your choice. If you desire specific details, enter a prompt, press enter, and then click 'Describe the Image' for customized information. For a comprehensive overview, simply click the 'Describe the Image' button to receive all details about the image. After viewing the image, scroll down to see the response.*")
input=st.text_input("Enter Your Prompt: ",key="input")
submit=st.button("Describe the Image")
uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


input_prompt = """
               You are an expert in understanding images.
               You will tell everything about the images in bullet points and will not miss any details.
               You will explain the image in extreme detail.
               """

if submit:
    image_data = input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("Gemini's ♊ Response:")
    st.write(response)
