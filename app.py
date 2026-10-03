import streamlit as st
import requests
import os
import base64
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(
    page_title="AI Vision Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Vision Chatbot")
st.write("Ask questions or upload an image for AI analysis!")

uploaded_image = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_image:
    st.image(uploaded_image, caption="Your uploaded image", use_container_width=True)

user_input = st.chat_input("Ask me anything about the image...")

if user_input:
    st.chat_message("user").write(user_input)

    if not API_KEY:
        st.error("Gemini API key not found. Check your .env file.")

    else:
        try:
            url = (
                "https://generativelanguage.googleapis.com/v1beta/"
                "models/gemini-3.8-flash:generateContent"
                f"?key={API_KEY}"
            )

            parts = [{"text": user_input}]

            if uploaded_image:
                image_data = base64.b64encode(
                    uploaded_image.getvalue()
                ).decode("utf-8")

                parts.append({
                    "inline_data": {
                        "mime_type": uploaded_image.type,
                        "data": image_data
                    }
                })

            payload = {
                "system_instruction": {
                    "parts": [{"text": SYSTEM_PROMPT}]
                },
                "contents": [{
                    "role": "user",
                    "parts": parts
                }]
            }

            response = requests.post(
                url,
                json=payload,
                timeout=60
            )

            if response.status_code == 200:
                answer = response.json()["candidates"][0]["content"]["parts"][0]["text"]

                st.chat_message("assistant").write(answer)

            else:
                st.error(f"Gemini error: {response.text}")

        except Exception as e:
            st.error(f"Something went wrong: {e}")