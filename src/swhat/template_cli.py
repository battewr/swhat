"""Template registry for swhat CLI.

This module provides the registry and lookup functions for templates.
Template content is stored in the templates/ subpackage.
"""

from swhat.templates import (
    SPEC_TEMPLATE_CONTENT,
    CHECKLIST_CONTENT,
    PLAN_TEMPLATE_CONTENT,
    TASKS_TEMPLATE_CONTENT,
)

# Type alias for registry entries: (content, description)
TemplateEntry = tuple[str, str]

# Template registry: name -> (content, description)
TEMPLATES: dict[str, TemplateEntry] = {
    "specification": (SPEC_TEMPLATE_CONTENT, "Feature specification template"),
    "specification-checklist": (CHECKLIST_CONTENT, "Spec quality validation checklist"),
    "plan": (PLAN_TEMPLATE_CONTENT, "Implementation plan template"),
    "tasks": (TASKS_TEMPLATE_CONTENT, "Task list template for implementation"),
}


def get_template(name: str) -> TemplateEntry | None:
    """Get a template by name (case-insensitive lookup).

    Args:
        name: Template name to look up.

    Returns:
        Tuple of (content, description) if found, None otherwise.
    """
    return TEMPLATES.get(name.lower())


def list_templates() -> list[tuple[str, str]]:
    """List all available templates.

    Returns:
        List of (name, description) tuples, sorted by name.
    """
    return sorted((name, entry[1]) for name, entry in TEMPLATES.items())
