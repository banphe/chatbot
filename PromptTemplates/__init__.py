from .template import Template
from .template_registry import TemplateRegistry
from .translator_template import translator_template
from .polite_template import polite_template

# Initialize the registry
template_registry = TemplateRegistry()

# Register templates
template_registry.register_template(translator_template)
template_registry.register_template(polite_template)

# You can add more template registrations here