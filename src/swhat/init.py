"""Project initialization for swhat.

This module handles the `swhat init` command which sets up a project
for specification-driven development by creating directories and
installing AI agent command files.
"""

from pathlib import Path

import click

# Command file content for Claude Code (uses $ARGUMENTS placeholder)
CLAUDE_SPECIFY_COMMAND = """\
---
description: Create or update the feature specification from a natural language feature description.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

The text the user typed after `/swhat.specify` in the triggering message **is** the feature description. The `$ARGUMENTS` placeholder above contains that text. Do not ask the user to repeat it unless they provided an empty command.

Given that feature description, do this:

1. **Generate a concise short name** (2-4 words) for the branch:
   - Analyze the feature description and extract the most meaningful keywords
   - Create a 2-4 word short name that captures the essence of the feature
   - Use action-noun format when possible (e.g., "add-user-auth", "fix-payment-bug")
   - Preserve technical terms and acronyms (OAuth2, API, JWT, etc.)
   - Keep it concise but descriptive enough to understand the feature at a glance
   - **Append 12 random alphanumeric characters** to the short name, separated by an underscore
   - Generate the random characters using lowercase letters and digits (a-z, 0-9)
   - Examples:
     - "I want to add user authentication" -> "user-auth_a3b7x9k2m4n1"
     - "Implement OAuth2 integration for the API" -> "oauth2-api-integration_p8q2w5e1r7t3"
     - "Create a dashboard for analytics" -> "analytics-dashboard_j6h4f2d9s1l8"
     - "Fix payment processing timeout bug" -> "fix-payment-timeout_c5v3b7n9m2k4"

2. **Check for existing branches before creating new one**:

   a. You must only ever run this script once per feature
   b. The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for
   c. The JSON output will contain BRANCH_NAME and SPEC_FILE paths
   d. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\\''m Groot' (or double-quote if possible: "I'm Groot")

3. Retrieve the specification template by running `swhat template specification` to understand required sections.

4. Follow this execution flow:

    1. Parse user description from Input
       If empty: ERROR "No feature description provided"
    2. Extract key concepts from description
       Identify: actors, actions, data, constraints
    3. For unclear aspects:
       - Make informed guesses based on context and industry standards
       - Only mark with [NEEDS CLARIFICATION: specific question] if:
         - The choice significantly impacts feature scope or user experience
         - Multiple reasonable interpretations exist with different implications
         - No reasonable default exists
       - **LIMIT: Maximum 3 [NEEDS CLARIFICATION] markers total**
       - Prioritize clarifications by impact: scope > security/privacy > user experience > technical details
    4. Fill User Scenarios & Testing section
       If no clear user flow: ERROR "Cannot determine user scenarios"
    5. Generate Functional Requirements
       Each requirement must be testable
       Use reasonable defaults for unspecified details (document assumptions in Assumptions section)
    6. Define Success Criteria
       Create measurable, technology-agnostic outcomes
       Include both quantitative metrics (time, performance, volume) and qualitative measures (user satisfaction, task completion)
       Each criterion must be verifiable without implementation details
    7. Identify Key Entities (if data involved)
    8. Return: SUCCESS (spec ready for planning)

5. Write the specification to `.swhat/{FEATURE_SHORT_NAME}/{SPEC_FILE}` using the template structure, replacing placeholders with concrete details derived from the feature description (arguments) while preserving section order and headings.

6. **Specification Quality Validation**: After writing the initial spec, validate it against quality criteria:

   a. **Create Spec Quality Checklist**: Retrieve the checklist template by running `swhat template specification-checklist` and write it to `.swhat/{FEATURE_SHORT_NAME}/requirements.md`, replacing placeholders with feature-specific values.

   b. **Run Validation Check**: Review the spec against each checklist item:
      - For each item, determine if it passes or fails
      - Document specific issues found (quote relevant spec sections)

   c. **Handle Validation Results**:

      - **If all items pass**: Mark checklist complete and proceed to step 6

      - **If items fail (excluding [NEEDS CLARIFICATION])**:
        1. List the failing items and specific issues
        2. Update the spec to address each issue
        3. Re-run validation until all items pass (max 3 iterations)
        4. If still failing after 3 iterations, document remaining issues in checklist notes and warn user

      - **If [NEEDS CLARIFICATION] markers remain**:
        1. Extract all [NEEDS CLARIFICATION: ...] markers from the spec
        2. **LIMIT CHECK**: If more than 3 markers exist, keep only the 3 most critical (by scope/security/UX impact) and make informed guesses for the rest
        3. For each clarification needed (max 3), present options to user in this format:

           ```markdown
           ## Question [N]: [Topic]

           **Context**: [Quote relevant spec section]

           **What we need to know**: [Specific question from NEEDS CLARIFICATION marker]

           **Suggested Answers**:

           | Option | Answer | Implications |
           |--------|--------|--------------|
           | A      | [First suggested answer] | [What this means for the feature] |
           | B      | [Second suggested answer] | [What this means for the feature] |
           | C      | [Third suggested answer] | [What this means for the feature] |
           | Custom | Provide your own answer | [Explain how to provide custom input] |

           **Your choice**: _[Wait for user response]_
           ```

        4. **CRITICAL - Table Formatting**: Ensure markdown tables are properly formatted:
           - Use consistent spacing with pipes aligned
           - Each cell should have spaces around content: `| Content |` not `|Content|`
           - Header separator must have at least 3 dashes: `|--------|`
           - Test that the table renders correctly in markdown preview
        5. Number questions sequentially (Q1, Q2, Q3 - max 3 total)
        6. Present all questions together before waiting for responses
        7. Wait for user to respond with their choices for all questions (e.g., "Q1: A, Q2: Custom - [details], Q3: B")
        8. Update the spec by replacing each [NEEDS CLARIFICATION] marker with the user's selected or provided answer
        9. Re-run validation after all clarifications are resolved

   d. **Update Checklist**: After each validation iteration, update the checklist file with current pass/fail status

7. **Cleanup and Report**:
   - Delete the temporary files: `.swhat/{FEATURE_SHORT_NAME}/{SPEC_FILE}` and `.swhat/{FEATURE_SHORT_NAME}/requirements.md`
   - Present the final specification content to the user in full
   - Report whether the specification was **successful** (all checklist items pass, no ambiguities) or **needs refinement** (details are still too vague, clarifications needed)
   - If successful: The spec is ready to be used for implementation planning
   - If needs refinement: Explain what aspects are unclear and suggest the user provide more details

## General Guidelines

## Quick Guidelines

- Focus on **WHAT** users need and **WHY**.
- Avoid HOW to implement (no tech stack, APIs, code structure).
- Written for business stakeholders, not developers.
- DO NOT create any checklists that are embedded in the spec. That will be a separate command.

### Section Requirements

- **Mandatory sections**: Must be completed for every feature
- **Optional sections**: Include only when relevant to the feature
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### For AI Generation

When creating this spec from a user prompt:

1. **Make informed guesses**: Use context, industry standards, and common patterns to fill gaps
2. **Document assumptions**: Record reasonable defaults in the Assumptions section
3. **Limit clarifications**: Maximum 3 [NEEDS CLARIFICATION] markers - use only for critical decisions that:
   - Significantly impact feature scope or user experience
   - Have multiple reasonable interpretations with different implications
   - Lack any reasonable default
4. **Prioritize clarifications**: scope > security/privacy > user experience > technical details
5. **Think like a tester**: Every vague requirement should fail the "testable and unambiguous" checklist item
6. **Common areas needing clarification** (only if no reasonable default exists):
   - Feature scope and boundaries (include/exclude specific use cases)
   - User types and permissions (if multiple conflicting interpretations possible)
   - Security/compliance requirements (when legally/financially significant)

**Examples of reasonable defaults** (don't ask about these):

- Data retention: Industry-standard practices for the domain
- Performance targets: Standard web/mobile app expectations unless specified
- Error handling: User-friendly messages with appropriate fallbacks
- Authentication method: Standard session-based or OAuth2 for web apps
- Integration patterns: RESTful APIs unless specified otherwise

### Success Criteria Guidelines

Success criteria must be:

1. **Measurable**: Include specific metrics (time, percentage, count, rate)
2. **Technology-agnostic**: No mention of frameworks, languages, databases, or tools
3. **User-focused**: Describe outcomes from user/business perspective, not system internals
4. **Verifiable**: Can be tested/validated without knowing implementation details

**Good examples**:

- "Users can complete checkout in under 3 minutes"
- "System supports 10,000 concurrent users"
- "95% of searches return results in under 1 second"
- "Task completion rate improves by 40%"

**Bad examples** (implementation-focused):

- "API response time is under 200ms" (too technical, use "Users see results instantly")
- "Database can handle 1000 TPS" (implementation detail, use user-facing metric)
- "React components render efficiently" (framework-specific)
- "Redis cache hit rate above 80%" (technology-specific)
"""

# Command file content for Roo Code (no $ARGUMENTS - user input is in the message)
ROO_SPECIFY_COMMAND = """\
---
description: Create or update the feature specification from a natural language feature description.
argument-hint: <feature description in natural language>
---

## Outline

The text the user typed after `/swhat-specify` in the triggering message **is** the feature description. Look at the user's full message to find it. Do not ask the user to repeat it unless they provided an empty command.

Given that feature description, do this:

1. **Generate a concise short name** (2-4 words) for the branch:
   - Analyze the feature description and extract the most meaningful keywords
   - Create a 2-4 word short name that captures the essence of the feature
   - Use action-noun format when possible (e.g., "add-user-auth", "fix-payment-bug")
   - Preserve technical terms and acronyms (OAuth2, API, JWT, etc.)
   - Keep it concise but descriptive enough to understand the feature at a glance
   - **Append 12 random alphanumeric characters** to the short name, separated by an underscore
   - Generate the random characters using lowercase letters and digits (a-z, 0-9)
   - Examples:
     - "I want to add user authentication" -> "user-auth_a3b7x9k2m4n1"
     - "Implement OAuth2 integration for the API" -> "oauth2-api-integration_p8q2w5e1r7t3"
     - "Create a dashboard for analytics" -> "analytics-dashboard_j6h4f2d9s1l8"
     - "Fix payment processing timeout bug" -> "fix-payment-timeout_c5v3b7n9m2k4"

2. **Check for existing branches before creating new one**:

   a. You must only ever run this script once per feature
   b. The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for
   c. The JSON output will contain BRANCH_NAME and SPEC_FILE paths
   d. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\\''m Groot' (or double-quote if possible: "I'm Groot")

3. Retrieve the specification template by running `swhat template specification` to understand required sections.

4. Follow this execution flow:

    1. Parse user description from the user's message
       If empty: ERROR "No feature description provided"
    2. Extract key concepts from description
       Identify: actors, actions, data, constraints
    3. For unclear aspects:
       - Make informed guesses based on context and industry standards
       - Only mark with [NEEDS CLARIFICATION: specific question] if:
         - The choice significantly impacts feature scope or user experience
         - Multiple reasonable interpretations exist with different implications
         - No reasonable default exists
       - **LIMIT: Maximum 3 [NEEDS CLARIFICATION] markers total**
       - Prioritize clarifications by impact: scope > security/privacy > user experience > technical details
    4. Fill User Scenarios & Testing section
       If no clear user flow: ERROR "Cannot determine user scenarios"
    5. Generate Functional Requirements
       Each requirement must be testable
       Use reasonable defaults for unspecified details (document assumptions in Assumptions section)
    6. Define Success Criteria
       Create measurable, technology-agnostic outcomes
       Include both quantitative metrics (time, performance, volume) and qualitative measures (user satisfaction, task completion)
       Each criterion must be verifiable without implementation details
    7. Identify Key Entities (if data involved)
    8. Return: SUCCESS (spec ready for planning)

5. Write the specification to `.swhat/{FEATURE_SHORT_NAME}/{SPEC_FILE}` using the template structure, replacing placeholders with concrete details derived from the feature description while preserving section order and headings.

6. **Specification Quality Validation**: After writing the initial spec, validate it against quality criteria:

   a. **Create Spec Quality Checklist**: Retrieve the checklist template by running `swhat template specification-checklist` and write it to `.swhat/{FEATURE_SHORT_NAME}/requirements.md`, replacing placeholders with feature-specific values.

   b. **Run Validation Check**: Review the spec against each checklist item:
      - For each item, determine if it passes or fails
      - Document specific issues found (quote relevant spec sections)

   c. **Handle Validation Results**:

      - **If all items pass**: Mark checklist complete and proceed to step 6

      - **If items fail (excluding [NEEDS CLARIFICATION])**:
        1. List the failing items and specific issues
        2. Update the spec to address each issue
        3. Re-run validation until all items pass (max 3 iterations)
        4. If still failing after 3 iterations, document remaining issues in checklist notes and warn user

      - **If [NEEDS CLARIFICATION] markers remain**:
        1. Extract all [NEEDS CLARIFICATION: ...] markers from the spec
        2. **LIMIT CHECK**: If more than 3 markers exist, keep only the 3 most critical (by scope/security/UX impact) and make informed guesses for the rest
        3. For each clarification needed (max 3), present options to user in this format:

           ```markdown
           ## Question [N]: [Topic]

           **Context**: [Quote relevant spec section]

           **What we need to know**: [Specific question from NEEDS CLARIFICATION marker]

           **Suggested Answers**:

           | Option | Answer | Implications |
           |--------|--------|--------------|
           | A      | [First suggested answer] | [What this means for the feature] |
           | B      | [Second suggested answer] | [What this means for the feature] |
           | C      | [Third suggested answer] | [What this means for the feature] |
           | Custom | Provide your own answer | [Explain how to provide custom input] |

           **Your choice**: _[Wait for user response]_
           ```

        4. **CRITICAL - Table Formatting**: Ensure markdown tables are properly formatted:
           - Use consistent spacing with pipes aligned
           - Each cell should have spaces around content: `| Content |` not `|Content|`
           - Header separator must have at least 3 dashes: `|--------|`
           - Test that the table renders correctly in markdown preview
        5. Number questions sequentially (Q1, Q2, Q3 - max 3 total)
        6. Present all questions together before waiting for responses
        7. Wait for user to respond with their choices for all questions (e.g., "Q1: A, Q2: Custom - [details], Q3: B")
        8. Update the spec by replacing each [NEEDS CLARIFICATION] marker with the user's selected or provided answer
        9. Re-run validation after all clarifications are resolved

   d. **Update Checklist**: After each validation iteration, update the checklist file with current pass/fail status

7. **Cleanup and Report**:
   - Delete the temporary files: `.swhat/{FEATURE_SHORT_NAME}/{SPEC_FILE}` and `.swhat/{FEATURE_SHORT_NAME}/requirements.md`
   - Present the final specification content to the user in full
   - Report whether the specification was **successful** (all checklist items pass, no ambiguities) or **needs refinement** (details are still too vague, clarifications needed)
   - If successful: The spec is ready to be used for implementation planning
   - If needs refinement: Explain what aspects are unclear and suggest the user provide more details

## General Guidelines

## Quick Guidelines

- Focus on **WHAT** users need and **WHY**.
- Avoid HOW to implement (no tech stack, APIs, code structure).
- Written for business stakeholders, not developers.
- DO NOT create any checklists that are embedded in the spec. That will be a separate command.

### Section Requirements

- **Mandatory sections**: Must be completed for every feature
- **Optional sections**: Include only when relevant to the feature
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### For AI Generation

When creating this spec from a user prompt:

1. **Make informed guesses**: Use context, industry standards, and common patterns to fill gaps
2. **Document assumptions**: Record reasonable defaults in the Assumptions section
3. **Limit clarifications**: Maximum 3 [NEEDS CLARIFICATION] markers - use only for critical decisions that:
   - Significantly impact feature scope or user experience
   - Have multiple reasonable interpretations with different implications
   - Lack any reasonable default
4. **Prioritize clarifications**: scope > security/privacy > user experience > technical details
5. **Think like a tester**: Every vague requirement should fail the "testable and unambiguous" checklist item
6. **Common areas needing clarification** (only if no reasonable default exists):
   - Feature scope and boundaries (include/exclude specific use cases)
   - User types and permissions (if multiple conflicting interpretations possible)
   - Security/compliance requirements (when legally/financially significant)

**Examples of reasonable defaults** (don't ask about these):

- Data retention: Industry-standard practices for the domain
- Performance targets: Standard web/mobile app expectations unless specified
- Error handling: User-friendly messages with appropriate fallbacks
- Authentication method: Standard session-based or OAuth2 for web apps
- Integration patterns: RESTful APIs unless specified otherwise

### Success Criteria Guidelines

Success criteria must be:

1. **Measurable**: Include specific metrics (time, percentage, count, rate)
2. **Technology-agnostic**: No mention of frameworks, languages, databases, or tools
3. **User-focused**: Describe outcomes from user/business perspective, not system internals
4. **Verifiable**: Can be tested/validated without knowing implementation details

**Good examples**:

- "Users can complete checkout in under 3 minutes"
- "System supports 10,000 concurrent users"
- "95% of searches return results in under 1 second"
- "Task completion rate improves by 40%"

**Bad examples** (implementation-focused):

- "API response time is under 200ms" (too technical, use "Users see results instantly")
- "Database can handle 1000 TPS" (implementation detail, use user-facing metric)
- "React components render efficiently" (framework-specific)
- "Redis cache hit rate above 80%" (technology-specific)
"""


def initialize_project() -> bool:
    """Initialize the current directory for swhat specification workflow.

    Creates:
        - .swhat/ directory for user workspace
        - .claude/commands/swhat.specify.md for Claude Code
        - .roo/commands/swhat-specify.md for Roo

    Returns:
        True if initialization succeeded, False otherwise.
    """
    cwd = Path.cwd()

    click.echo("Initializing swhat in current directory...")

    # Create .swhat/ directory
    swhat_dir = cwd / ".swhat"
    if swhat_dir.exists():
        click.echo("  .swhat/ already exists")
    else:
        swhat_dir.mkdir(parents=True, exist_ok=True)
        click.echo("  Created .swhat/")

    # Create .claude/commands/ and write command file
    claude_commands_dir = cwd / ".claude" / "commands"
    claude_commands_dir.mkdir(parents=True, exist_ok=True)
    claude_command_file = claude_commands_dir / "swhat.specify.md"
    if claude_command_file.exists():
        claude_command_file.write_text(CLAUDE_SPECIFY_COMMAND)
        click.echo("  Updated .claude/commands/swhat.specify.md")
    else:
        claude_command_file.write_text(CLAUDE_SPECIFY_COMMAND)
        click.echo("  Created .claude/commands/swhat.specify.md")

    # Create .roo/commands/ and write command file
    # Note: Roo uses dashes in command names, not dots
    roo_commands_dir = cwd / ".roo" / "commands"
    roo_commands_dir.mkdir(parents=True, exist_ok=True)
    roo_command_file = roo_commands_dir / "swhat-specify.md"
    if roo_command_file.exists():
        roo_command_file.write_text(ROO_SPECIFY_COMMAND)
        click.echo("  Updated .roo/commands/swhat-specify.md")
    else:
        roo_command_file.write_text(ROO_SPECIFY_COMMAND)
        click.echo("  Created .roo/commands/swhat-specify.md")

    click.echo("Initialization complete!")
    click.echo("  - Claude Code: use /swhat.specify")
    click.echo("  - Roo: use /swhat-specify")
    return True
