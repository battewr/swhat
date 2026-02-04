# Data Model: Template Command

**Feature**: 001-template-command
**Date**: 2026-01-28

## Entities

### Template

A named text block representing a workflow artifact structure.

| Attribute | Type | Description | Constraints |
|-----------|------|-------------|-------------|
| name | string | Unique identifier for the template | Lowercase, alphanumeric + hyphens only |
| content | string | Full template text (Markdown) | Non-empty |
| description | string | Brief one-line description for list output | Non-empty, <80 chars |

**Identity**: Templates are uniquely identified by `name` (case-insensitive lookup).

**Lifecycle**: Static. Templates are defined at build time and do not change at runtime.

### Template Registry

In-memory collection of all available templates.

| Operation | Input | Output | Notes |
|-----------|-------|--------|-------|
| get | name: str | Template or None | Case-insensitive lookup |
| list_all | - | list[Template] | Returns all templates |
| names | - | list[str] | Returns sorted list of names |

## Data Structures (Python)

```python
# Type alias for registry entries
TemplateEntry = tuple[str, str]  # (content, description)

# Registry type
TEMPLATES: dict[str, TemplateEntry] = {
    "specification": (SPEC_TEMPLATE_CONTENT, "Feature specification template"),
    "specification-checklist": (CHECKLIST_CONTENT, "Spec quality validation checklist"),
}
```

## Initial Template Content

### specification

Source: `.specify/templates/spec-template.md`

Embedded as `SPEC_TEMPLATE_CONTENT` string constant.

### specification-checklist

Content (from clarification session):

```markdown
# Specification Quality Checklist: [FEATURE NAME]

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: [DATE]
**Feature**: [Link to spec.md]

## Content Quality

- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value and business needs
- [ ] Written for non-technical stakeholders
- [ ] All mandatory sections completed

## Requirement Completeness

- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable
- [ ] Success criteria are technology-agnostic (no implementation details)
- [ ] All acceptance scenarios are defined
- [ ] Edge cases are identified
- [ ] Scope is clearly bounded
- [ ] Dependencies and assumptions identified

## Feature Readiness

- [ ] All functional requirements have clear acceptance criteria
- [ ] User scenarios cover primary flows
- [ ] Feature meets measurable outcomes defined in Success Criteria
- [ ] No implementation details leak into specification

## Notes

- Items marked incomplete require spec updates before `/speckit.clarify` or `/speckit.plan`
```

Embedded as `CHECKLIST_CONTENT` string constant.

## Validation Rules

| Rule | Enforcement |
|------|-------------|
| Template name must exist in registry | Return error + available names |
| Template name normalized to lowercase | `name.lower()` before lookup |
| Empty/whitespace name treated as no argument | Show list |

## State Transitions

N/A - Templates are immutable static data.
