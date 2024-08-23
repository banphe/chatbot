import PIL.Image
import streamlit as st
from streamlit import session_state as cache
import os, io, base64, uuid
from thread import Thread
from anthropic_client import AnthropicClient
from Agents import *
from whisper_stt import whisper_stt
from PromptTemplates import template_registry

def display_conversation(thread, show_full_message):
    for m in thread.get_conversation():
        with st.chat_message(name=m['role']):
            for content in m['content']:
                if content['type'] == 'text':
                    if cache.selected_agent.get_name() == "Translator" and not show_full_message:
                        displayed_text = template_registry.extract_content(content['text'], "translator")
                    else:
                        displayed_text = content['text']
                    st.write(displayed_text)
                elif content['type'] == 'image':
                    image_data = base64.b64decode(content['source']['data'])
                    image = PIL.Image.open(io.BytesIO(image_data))
                    st.image(image, caption="Uploaded Image")
                else:
                    st.code(content)

def main():
    st.set_page_config(layout='wide')
    
    if "recording" not in cache: cache.recording = ""
    if "thread" not in cache: cache.thread = Thread(id=str(uuid.uuid4()))
    if "uploaded_files" not in cache: cache.uploaded_files = []
    if "selected_agent" not in cache: cache.selected_agent = BusinessPlanAgent()
    if "selected_template" not in cache: cache.selected_template = None
    if "show_full_message" not in cache: cache.show_full_message = False

    # Sidebar for file uploading, agent selection, and template selection
    with st.sidebar:
        st.header("Upload Images")
        uploaded_files = st.file_uploader("Choose images", accept_multiple_files=True, type=['png', 'jpg', 'jpeg', 'gif', 'webp'])
        if uploaded_files:
            cache.uploaded_files = uploaded_files
            st.success(f"{len(uploaded_files)} image(s) uploaded successfully!")
        
        st.header("Select Agent")
        cache.selected_agent = st.radio(
            "Choose an agent:",
            options=[BusinessPlanAgent(), ToolsOperatorAgent(), TranslatorAgent()],
            format_func=lambda x: x.get_name()
        )

        st.header("Select Template")
        available_templates = template_registry.list_templates()
        cache.selected_template = st.selectbox(
            "Choose a template to apply:",
            options=[None] + [t["name"] for t in available_templates],
            format_func=lambda x: "No template" if x is None else next(t["description"] for t in available_templates if t["name"] == x)
        )

        cache.show_full_message = st.checkbox("Show full message (including template)", value=False)

        lang = st.radio(label="Input Language", options=['en','pl','th'])
        text = whisper_stt(openai_api_key="your_openai_api_key", language=lang)
        if text: cache.recording = text

    user_message = st.chat_input("Your message")
    if cache.recording:
        user_message = cache.recording
        cache.recording = ''

    if user_message:
        # Apply selected template
        if cache.selected_template:
            user_message = template_registry.apply_template(user_message, cache.selected_template)

        image_paths = []
        if cache.uploaded_files:
            for uploaded_file in cache.uploaded_files:
                with open(uploaded_file.name, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                image_paths.append(uploaded_file.name)
        
        # Initialize AnthropicClient directly and call ProcessMessage
        anthropic_client = AnthropicClient()
        cache.thread = anthropic_client.ProcessMessage(cache.thread, user_message, cache.selected_agent, image_paths)
        
        # Clean up temporary files
        for path in image_paths:
            if os.path.exists(path):
                os.remove(path)
        
        # Clear uploaded files after processing
        cache.uploaded_files = []

    display_conversation(cache.thread, cache.show_full_message)

    # Display thread ID (for demonstration purposes)
    st.sidebar.text(f"Current Thread ID: {cache.thread.get_id()}")

if __name__ == "__main__":
    main()