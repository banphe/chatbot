from .template import Template

polite_template = Template(
    name="polite",
    description="Adds polite opening and closing to the message",
    start_tag="<polite_message>",
    end_tag="</polite_message>",
    pre_text="I hope this message finds you well.",
    post_text="Thank you for your assistance."
)