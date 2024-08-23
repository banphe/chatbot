class TemplateRegistry:
    def __init__(self):
        self.templates = {}

    def register_template(self, template):
        self.templates[template.name] = template

    def get_template(self, name):
        return self.templates.get(name)

    def list_templates(self):
        return [{"name": t.name, "description": t.description} for t in self.templates.values()]

    def apply_template(self, message, template_name):
        template = self.get_template(template_name)
        if template:
            return template.apply(message)
        return message  # Return original message if template not found

    def extract_content(self, message, template_name):
        template = self.get_template(template_name)
        if template:
            return template.extract(message)
        return message  # Return original message if template not found