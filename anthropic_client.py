import anthropic
from Tools import initialize_tools
import os 
from content_constructor import text_content, image_content, tool_use_content, tool_result_content
from extended_message import ExtendedMessage

class AnthropicClient:
    msgApi = anthropic.Client().messages
    sonnet = "claude-3-5-sonnet-20240620"
    anthropic_api_key = os.environ.get('ANTHROPIC_API_KEY')
    def __init__(self):
        self.tool_registry = initialize_tools()

    def ProcessMessage(self, thread, prompt, agent, image_paths=[]):
        #1 USER
        thread.add_user_message(prompt, image_paths)
        all_tools = self.tool_registry.list_tools()
        available_tools = [tool for tool in all_tools if tool['name'] in agent.get_tools()]
        response = self._CallAPI(thread.get_conversation(), agent, available_tools)
        while response.stop_reason == "tool_use":
            converted_content = []
            for block in response.content:
                if block.type == 'text':
                    converted_content.append(text_content(block.text))
                elif block.type == 'tool_use':
                    converted_content.append(tool_use_content(id=block.id, name=block.name, input=block.input))
            #2 ASSISTANT
            thread.add_assistant_message(converted_content)
            tool_use_blocks = [block for block in response.content if block.type == "tool_use"]
            
            tool_results = []
            for tool_use in tool_use_blocks:
                tool_result = self.tool_registry.process_tool_call(tool_use.name, tool_use.input)
                tool_results.append(tool_result_content(tool_use.id, tool_result))

            #3 USER
            thread.add_tool_request_message(tool_results)

            #4 ASSISTANT
            response = self._CallAPI(thread.get_conversation(), agent, available_tools)

        final_response = next(({'type': 'text', 'text': block.text} for block in response.content if block.type == 'text'), None)
        thread.add_assistant_message([final_response] if final_response else [])
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