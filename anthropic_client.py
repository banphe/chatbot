import anthropic
from Tools import initialize_tools
import os 
from content_constructor import text_content, image_content, tool_use_content, tool_result_content
from extended_message import ExtendedMessage
import uuid

class AnthropicClient:
    msgApi = anthropic.Client().messages
    sonnet = "claude-3-5-sonnet-20240620"
    anthropic_api_key = os.environ.get('ANTHROPIC_API_KEY')
    def __init__(self, user='Jacob'):
        self.tool_registry = initialize_tools()
        self.user = user
    def _convert_response_content(self, response):
        converted_content = []
        for block in response.content:
            if block.type == 'text':
                converted_content.append(text_content(block.text))
            elif block.type == 'tool_use':
                converted_content.append(tool_use_content(id=block.id, name=block.name, input=block.input))
            elif block.type == 'image':
                converted_content.append(image_content(block.source.media_type, block.source.data))
        return converted_content

    def ProcessMessage(self, thread, prompt, agent, image_paths=[]):
        run_id = str(uuid.uuid4())
        thread.add_user_message(prompt, image_paths, self.user, agent.get_name(), run_id)
        all_tools = self.tool_registry.list_tools()
        available_tools = [tool for tool in all_tools if tool['name'] in agent.get_tools()]
        response = self._CallAPI(thread.get_conversation(), agent, available_tools)
        while response.stop_reason == "tool_use":
            converted_content = self._convert_response_content(response)
            thread.add_assistant_message(converted_content, "system", "tool_use", run_id) #Add Assistant Message
            tool_use_blocks = [block for block in response.content if block.type == "tool_use"]
            
            tool_results = []
            for tool_use in tool_use_blocks:
                tool_result = self.tool_registry.process_tool_call(tool_use.name, tool_use.input)
                tool_results.append(tool_result_content(tool_use.id, tool_result))

            thread.add_tool_request_message(tool_results,"system", "tool_result", run_id) #Add User Message
            response = self._CallAPI(thread.get_conversation(), agent, available_tools) 

        final_response = self._convert_response_content(response)
        thread.add_assistant_message(final_response, agent.get_name(), self.user, run_id) #Add Assistant Message
    # Add other content types as needed

        return thread
  
    def _CallAPI(self, messages, agent, available_tools):
        return self.msgApi.create(
            model=self.sonnet,
            max_tokens=4096,
            tools=available_tools,
            messages=messages,
            system=agent.get_instructions(),
            temperature=agent.get_temperature()
        )