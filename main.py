import os
from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu
from gemini_utility import (load_gemini_pro_model,
                            gemini_pro_response,
                            gemini_pro_vision_response,
                            embeddings_model_response)

# Set page configuration at the top
st.set_page_config(
    page_title="LankaMate AI",
    page_icon="🤖",
    layout="centered",
)

# Custom CSS for improved styling with Bootstrap
st.markdown("""
    <style>
    /* Bootstrap CSS from CDN */
    @import url('https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css');

    /* General styling */
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f4f4f4;
        color: #333;
    }
    .main {
        background-color: white;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .btn-custom {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 15px;
        border: none;
        cursor: pointer;
        font-size: 16px;
    }
    .btn-custom:hover {
        background-color: #45a049;
    }
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .css-18e3th9 {
        padding: 20px;
    }
    .css-1d391kg h2 {
        color: #007bff;
        font-size: 22px;
    }
    .css-1d391kg .css-10trblm {
        color: #007bff;
        font-weight: bold;
    }
    /* Custom title */
    .st-title h1 {
        color: #007bff;
        font-size: 28px;
        font-weight: bold;
    }
    .st-title h2 {
        color: #6c757d;
        font-size: 18px;
        margin-bottom: 10px;
    }
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 20px;
        font-size: 14px;
        color: #888;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Add Bootstrap JavaScript for interactive components (if needed)
st.markdown("""
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
""", unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu('LankaMate AI',
                           ['ChatBot', 'Image Insight', 'Embed Text', 'Ask me anything'],
                           menu_icon='robot',
                           icons=['chat-dots-fill', 'image-fill', 'textarea-t', 'patch-question-fill'],
                           default_index=0)

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Chatbot page
if selected == 'ChatBot':
    model = load_gemini_pro_model()

    # Initialize chat session in Streamlit if not already present
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # Display the chatbot's title on the page
    st.title("🤖 LankaMate AI ChatBot")

    # Display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # Input field for user's message
    user_prompt = st.chat_input("Ask me anything...")  # Simplified prompt text
    if user_prompt:
        # Add user's message to chat and display it
        st.chat_message("user").markdown(user_prompt)

        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

# Image Insight page
if selected == "Image Insight":
    st.title("📷 Image Insight")

    uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

    if st.button("Generate Caption", key="caption"):
        if uploaded_image is not None:
            image = Image.open(uploaded_image)

            col1, col2 = st.columns(2)

            with col1:
                resized_img = image.resize((800, 500))
                st.image(resized_img)

            default_prompt = "Describe this image in a few words."

            # Get the caption of the image from the Gemini-Pro Vision model
            caption = gemini_pro_vision_response(default_prompt, image)

            with col2:
                st.info(caption)
        else:
            st.warning("Please upload an image first.")

# Embed Text page
if selected == "Embed Text":
    st.title("🔡 Embed Text")

    # Text box to enter prompt
    user_prompt = st.text_area(label='', placeholder="Enter text to get embeddings...")

    if st.button("Get Embeddings", key="embed"):
        response = embeddings_model_response(user_prompt)
        st.markdown(response)

# Ask me anything page
if selected == "Ask me anything":
    st.title("❓ Ask me anything")

    # Text box to enter prompt
    user_prompt = st.text_area(label='', placeholder="Ask me anything...")

    if st.button("Get Response", key="ask"):
        response = gemini_pro_response(user_prompt)
        st.markdown(response)

# Footer with developer credit
st.markdown("""
    <div class="footer">
        Created with ❤️ by Nithilan
    </div>
""", unsafe_allow_html=True)
