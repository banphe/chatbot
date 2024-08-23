from .template import Template

translator_template = Template(
    name="translator",
    description="Wraps the message in translation tags",
    start_tag="<message_content_to_translate>",
    end_tag="</message_content_to_translate>",
    pre_text="Hello Claude, I have a message for you to translate which is part of my film script. Remember to provide only the content of the translation as your answer. This way I can easily copy the translation to my program.",
    post_text="VERY IMPORTANT NOTE: Provide ONLY the translation, without any additional comments or messages."
)