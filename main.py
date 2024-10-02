import uuid, os 
import streamlit as st
from streamlit import session_state as cache
from thread import Thread
from anthropic_client import AnthropicClient
from Agents import *
from whisper_stt import whisper_stt
from PromptTemplates import template_registry
import image_processor 
from streamlit_extras.stylable_container import stylable_container
from itertools import groupby
from operator import attrgetter
import base64
from io import BytesIO
from PIL import Image

# Define colors
border_color = "#4a4a4a"  # Light variation of gray
assistant_bg_color = "#1e1e2d"  # Lighter variation of main area background
user_bg_color = "transparent"

user_css = f"""{{
    border: 1px solid {border_color};
    border-radius: 5px;
    padding: 10px;
    margin-bottom: 10px;
    background-color: {user_bg_color};
}}"""

assistant_css = f"""{{
    border: 1px solid {border_color};
    border-radius: 5px;
    padding: 10px;
    margin-bottom: 10px;
    background-color: {assistant_bg_color};
}}"""

    
def display_conversation_backup(thread, show_full_message):
    # Divide conversation into two lists
    non_system_messages = []
    system_messages = []
    for m in thread.get_full_conversation():
        if m.sender == "system":
            system_messages.append(m)
        else:
            non_system_messages.append(m)

    # Iterate only over non-system messages
    for m in non_system_messages:

        css = user_css if m.role == 'user' else assistant_css
        with stylable_container(key= f"message_{m.role}_{m.get_run_id()}", css_styles=css):
            st.subheader(m.sender)
            for content in m.content:
                    if content['type'] == 'text':
                        if cache.selected_agent.get_name() == "Translator" and not show_full_message:
                            displayed_text = template_registry.extract_content(content['text'], "translator")
                        else:
                            displayed_text = content['text']
                        with st.container():
                            st.write(displayed_text)
                    elif content['type'] == 'image':
                        image = image_processor.base64_to_image(content['source']['data'])
                        with st.container():
                            st.image(image, caption="Uploaded Image", use_column_width=True)
                    elif content['type'] in ['tool_use', 'tool_result']:
                        with st.container():
                            st.code(content)

# New display_conversation function
def display_conversation(thread, show_full_message):
    messages = thread.get_full_conversation()
    calls = [list(group) for _, group in groupby(messages, key=attrgetter('run_id'))]

    for call in calls:
        # Container for the first message (user input) and tool use
        with stylable_container(key=f"user_input_{call[0].get_run_id()}", css_styles=user_css):
            first_message = call[0]
            st.write(first_message.sender.capitalize())  # Show sender field
            for content in first_message.content:
                if content['type'] == 'text':
                    with st.container():
                        st.write(content['text'])
                    break  # Only display the first text content

            # Display tool use in the first container
            tool_uses = [content for msg in call for content in msg.content if content['type'] == 'tool_use']
            for tool_use in tool_uses:
                with st.expander(f"Tool Use: {tool_use['name']}"):
                    st.json(tool_use['input'])

        # Container for the last message (usually assistant message) and tool results
        with stylable_container(key=f"assistant_{call[-1].get_run_id()}", css_styles=assistant_css):
            st.write(call[-1].sender.capitalize())  # Show sender field
            last_message = call[-1]
            for content in reversed(last_message.content):
                if content['type'] == 'text':
                    with st.container():
                        st.write(content['text'])
                    break  # Only display the last text content

            # Display tool results in the assistant container
            tool_results = [content for msg in call for content in msg.content if content['type'] == 'tool_result']
            for result in tool_results:
                error_status = "Error" if result['is_error'] else "Success"
                with st.expander(f"Tool Result ({error_status})"):
                    if isinstance(result['content'], list) and len(result['content']) > 0:
                        for item in result['content']:
                            if isinstance(item, dict) and item.get('type') == 'image':
                                image_data = base64.b64decode(item['source']['data'])
                                image = Image.open(BytesIO(image_data))
                                st.image(image, caption="Generated Image", use_column_width=True)
                    else:
                        st.write(result['content'])

    return calls

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
            cache.uploaded_files = image_processor.process_multiple_images(uploaded_files)
            st.success(f"{len(cache.uploaded_files)} image(s) uploaded and processed successfully!")
        
        
        cache.selected_agent = st.radio(
            "Choose an agent:",
            options=[BusinessPlanAgent(), ToolsOperatorAgent(), TranslatorAgent()],
            format_func=lambda x: x.get_name()
        )

       
        available_templates = template_registry.list_templates()
        cache.selected_template = st.selectbox(
            "Choose a template to apply:",
            options=[None] + [t["name"] for t in available_templates],
            format_func=lambda x: "No template" if x is None else next(t["description"] for t in available_templates if t["name"] == x)
        )

        cache.show_full_message = st.checkbox("Show full message (including template)", value=False)

        lang = st.radio(label="Input Language", options=['en','pl','th'])
        text = whisper_stt(language=lang)
        if text: cache.recording = text

    user_message = st.chat_input("Your message")
    if cache.recording:
        user_message = cache.recording
        cache.recording = ''

    if user_message:
        # Apply selected template
        if cache.selected_template:
            user_message = template_registry.apply_template(user_message, cache.selected_template)

       
        # Initialize AnthropicClient directly and call ProcessMessage
        anthropic_client = AnthropicClient()
        cache.thread = anthropic_client.ProcessMessage(cache.thread, user_message, cache.selected_agent, cache.uploaded_files)

        # Clear uploaded files after processing
        cache.uploaded_files = []

    display_conversation(cache.thread, cache.show_full_message)

    # Display thread ID (for demonstration purposes)
    st.sidebar.text(f"Current Thread ID: {cache.thread.get_id()}")

if __name__ == "__main__":
    main()