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

1. **Generate a concise short name** (2-4 words) for the feature directory:
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

2. Retrieve the specification template by running `swhat template specification` to understand required sections.

3. Follow this execution flow:

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

4. Write the specification to `.swhat/{FEATURE_SHORT_NAME}/{SPEC_FILE}` using the template structure, replacing placeholders with concrete details derived from the feature description (arguments) while preserving section order and headings.

5. **Specification Quality Validation**: After writing the initial spec, validate it against quality criteria:

   a. **Create Spec Quality Checklist**: Retrieve the checklist template by running `swhat template specification-checklist` and write it to `.swhat/{FEATURE_SHORT_NAME}/requirements.md`, replacing placeholders with feature-specific values.

   b. **Run Validation Check**: Review the spec against each checklist item:
      - For each item, determine if it passes or fails
      - Document specific issues found (quote relevant spec sections)

   c. **Handle Validation Results**:

      - **If all items pass**: Mark checklist complete and proceed to step 5

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

6. **Report**:
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

1. **Generate a concise short name** (2-4 words) for the feature directory:
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

2. Retrieve the specification template by running `swhat template specification` to understand required sections.

3. Follow this execution flow:

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

4. Write the specification to `.swhat/{FEATURE_SHORT_NAME}/{SPEC_FILE}` using the template structure, replacing placeholders with concrete details derived from the feature description while preserving section order and headings.

5. **Specification Quality Validation**: After writing the initial spec, validate it against quality criteria:

   a. **Create Spec Quality Checklist**: Retrieve the checklist template by running `swhat template specification-checklist` and write it to `.swhat/{FEATURE_SHORT_NAME}/requirements.md`, replacing placeholders with feature-specific values.

   b. **Run Validation Check**: Review the spec against each checklist item:
      - For each item, determine if it passes or fails
      - Document specific issues found (quote relevant spec sections)

   c. **Handle Validation Results**:

      - **If all items pass**: Mark checklist complete and proceed to step 5

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

6. **Report**:
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

# Agent skill that auto-triggers when user requests a feature (Claude Code)
# Goes in .claude/skills/swhat-feature-workflow/SKILL.md
CLAUDE_FEATURE_SKILL = """\
---
name: swhat-feature-workflow
description: When the user asks to implement, build, create, or add a new feature, use this workflow to clarify requirements and create a specification before writing code. Activates for feature requests, not bug fixes or small tweaks.
user-invocable: false
---

# Feature Request Workflow

When the user asks you to implement, build, create, or add a **new feature**, follow this complete workflow BEFORE writing any code.

## When This Skill Does NOT Apply

- Bug fixes with clear reproduction steps
- Small tweaks to existing features ("change the button color")
- Refactoring with no behavior change
- Documentation updates
- User explicitly says "just do it" or "skip the spec"

---

## Step 1: Generate Feature Short Name

Create a concise short name (2-4 words) for the feature:

- Analyze the feature description and extract the most meaningful keywords
- Use action-noun format when possible (e.g., "add-user-auth", "fix-payment-bug")
- Preserve technical terms and acronyms (OAuth2, API, JWT, etc.)
- Keep it concise but descriptive enough to understand the feature at a glance
- **Append 12 random alphanumeric characters** to the short name, separated by an underscore
- Generate the random characters using lowercase letters and digits (a-z, 0-9)

**Examples**:
- "I want to add user authentication" -> "user-auth_a3b7x9k2m4n1"
- "Implement OAuth2 integration for the API" -> "oauth2-api-integration_p8q2w5e1r7t3"
- "Create a dashboard for analytics" -> "analytics-dashboard_j6h4f2d9s1l8"

---

## Step 2: Analyze and Extract Requirements

Parse the user's feature description and extract key concepts:

1. **Identify actors**: Who uses this feature? (user roles, personas)
2. **Identify actions**: What can they do? (core behaviors)
3. **Identify data**: What information is involved? (entities, attributes)
4. **Identify constraints**: What limits or rules apply? (validation, permissions)

### Handling Unclear Aspects

- **Make informed guesses** based on context and industry standards
- Only mark with `[NEEDS CLARIFICATION: specific question]` if:
  - The choice significantly impacts feature scope or user experience
  - Multiple reasonable interpretations exist with different implications
  - No reasonable default exists
- **LIMIT: Maximum 3 [NEEDS CLARIFICATION] markers total**
- **Prioritize clarifications by impact**: scope > security/privacy > user experience > technical details

---

## Step 3: Retrieve and Fill Specification Template

Run this command to get the template:

```bash
swhat template specification
```

Write the specification to `.swhat/{FEATURE_SHORT_NAME}/spec.md` using the template structure.

### Execution Flow

1. If description is empty: ERROR "No feature description provided"
2. Extract key concepts (actors, actions, data, constraints)
3. Fill **User Scenarios & Testing** section
   - If no clear user flow: ERROR "Cannot determine user scenarios"
   - Each user story must be independently testable
   - Include Given/When/Then acceptance scenarios
4. Generate **Functional Requirements**
   - Each requirement must be testable
   - Use reasonable defaults for unspecified details
5. Define **Success Criteria**
   - Create measurable, technology-agnostic outcomes
   - Include quantitative metrics (time, performance, volume)
   - Include qualitative measures (user satisfaction, task completion)
   - Each criterion must be verifiable without implementation details
6. Identify **Key Entities** (if data involved)

---

## Step 4: Validate Specification Quality

Run this command to get the checklist:

```bash
swhat template specification-checklist
```

Write the checklist to `.swhat/{FEATURE_SHORT_NAME}/requirements.md` and validate:

### Validation Check

For each checklist item:
- Determine if it passes or fails
- Document specific issues found (quote relevant spec sections)

### Handle Validation Results

**If all items pass**: Mark checklist complete and proceed.

**If items fail (excluding [NEEDS CLARIFICATION])**:
1. List the failing items and specific issues
2. Update the spec to address each issue
3. Re-run validation until all items pass (max 3 iterations)
4. If still failing after 3 iterations, document remaining issues and warn user

**If [NEEDS CLARIFICATION] markers remain**:
1. Extract all `[NEEDS CLARIFICATION: ...]` markers from the spec
2. **LIMIT CHECK**: If more than 3 markers exist, keep only the 3 most critical and make informed guesses for the rest
3. Present options to user in this format:

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

4. Number questions sequentially (Q1, Q2, Q3 - max 3 total)
5. Present all questions together before waiting for responses
6. After user responds, update spec with their answers
7. Re-run validation after all clarifications are resolved

---

## Step 5: Report

1. Present the final specification content to the user in full
2. Report status:
   - **Successful**: All checklist items pass, no ambiguities - spec is ready for implementation
   - **Needs refinement**: Details are still too vague - explain what aspects are unclear

3. **If needs refinement**, ask the user:

> "The specification has some gaps. Would you like to:
> 1. **Clarify** - Answer the open questions to improve the spec
> 2. **Proceed anyway** - Start implementation with current spec (may require changes later)
> 3. **Abandon** - Cancel this feature request"

If user chooses to proceed anyway, acknowledge the risks and begin implementation.

---

## Guidelines

### Focus on WHAT and WHY, Not HOW

- Focus on **WHAT** users need and **WHY**
- Avoid HOW to implement (no tech stack, APIs, code structure)
- Written for business stakeholders, not developers
- DO NOT create any checklists embedded in the spec

### Section Requirements

- **Mandatory sections**: Must be completed for every feature
- **Optional sections**: Include only when relevant to the feature
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### Making Informed Guesses

When creating specs, use reasonable defaults instead of asking about:

- **Data retention**: Industry-standard practices for the domain
- **Performance targets**: Standard web/mobile app expectations unless specified
- **Error handling**: User-friendly messages with appropriate fallbacks
- **Authentication method**: Standard session-based or OAuth2 for web apps
- **Integration patterns**: RESTful APIs unless specified otherwise

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
- "API response time is under 200ms" (too technical)
- "Database can handle 1000 TPS" (implementation detail)
- "React components render efficiently" (framework-specific)
- "Redis cache hit rate above 80%" (technology-specific)

---

## Why This Matters

Writing code for unclear requirements wastes time. A short conversation about requirements saves hours of rework. Your job is to build what the user actually needs, not what they initially said.
"""

# Agent skill that auto-triggers when user requests a feature (Roo)
# Goes in .roo/skills/swhat-feature-workflow/SKILL.md
ROO_FEATURE_SKILL = """\
---
name: swhat-feature-workflow
description: When the user asks to implement, build, create, or add a new feature, use this workflow to clarify requirements and create a specification before writing code. Activates for feature requests, not bug fixes or small tweaks.
---

# Feature Request Workflow

When the user asks you to implement, build, create, or add a **new feature**, follow this complete workflow BEFORE writing any code.

## When This Skill Does NOT Apply

- Bug fixes with clear reproduction steps
- Small tweaks to existing features ("change the button color")
- Refactoring with no behavior change
- Documentation updates
- User explicitly says "just do it" or "skip the spec"

---

## Step 1: Generate Feature Short Name

Create a concise short name (2-4 words) for the feature:

- Analyze the feature description and extract the most meaningful keywords
- Use action-noun format when possible (e.g., "add-user-auth", "fix-payment-bug")
- Preserve technical terms and acronyms (OAuth2, API, JWT, etc.)
- Keep it concise but descriptive enough to understand the feature at a glance
- **Append 12 random alphanumeric characters** to the short name, separated by an underscore
- Generate the random characters using lowercase letters and digits (a-z, 0-9)

**Examples**:
- "I want to add user authentication" -> "user-auth_a3b7x9k2m4n1"
- "Implement OAuth2 integration for the API" -> "oauth2-api-integration_p8q2w5e1r7t3"
- "Create a dashboard for analytics" -> "analytics-dashboard_j6h4f2d9s1l8"

---

## Step 2: Analyze and Extract Requirements

Parse the user's feature description and extract key concepts:

1. **Identify actors**: Who uses this feature? (user roles, personas)
2. **Identify actions**: What can they do? (core behaviors)
3. **Identify data**: What information is involved? (entities, attributes)
4. **Identify constraints**: What limits or rules apply? (validation, permissions)

### Handling Unclear Aspects

- **Make informed guesses** based on context and industry standards
- Only mark with `[NEEDS CLARIFICATION: specific question]` if:
  - The choice significantly impacts feature scope or user experience
  - Multiple reasonable interpretations exist with different implications
  - No reasonable default exists
- **LIMIT: Maximum 3 [NEEDS CLARIFICATION] markers total**
- **Prioritize clarifications by impact**: scope > security/privacy > user experience > technical details

---

## Step 3: Retrieve and Fill Specification Template

Run this command to get the template:

```bash
swhat template specification
```

Write the specification to `.swhat/{FEATURE_SHORT_NAME}/spec.md` using the template structure.

### Execution Flow

1. If description is empty: ERROR "No feature description provided"
2. Extract key concepts (actors, actions, data, constraints)
3. Fill **User Scenarios & Testing** section
   - If no clear user flow: ERROR "Cannot determine user scenarios"
   - Each user story must be independently testable
   - Include Given/When/Then acceptance scenarios
4. Generate **Functional Requirements**
   - Each requirement must be testable
   - Use reasonable defaults for unspecified details
5. Define **Success Criteria**
   - Create measurable, technology-agnostic outcomes
   - Include quantitative metrics (time, performance, volume)
   - Include qualitative measures (user satisfaction, task completion)
   - Each criterion must be verifiable without implementation details
6. Identify **Key Entities** (if data involved)

---

## Step 4: Validate Specification Quality

Run this command to get the checklist:

```bash
swhat template specification-checklist
```

Write the checklist to `.swhat/{FEATURE_SHORT_NAME}/requirements.md` and validate:

### Validation Check

For each checklist item:
- Determine if it passes or fails
- Document specific issues found (quote relevant spec sections)

### Handle Validation Results

**If all items pass**: Mark checklist complete and proceed.

**If items fail (excluding [NEEDS CLARIFICATION])**:
1. List the failing items and specific issues
2. Update the spec to address each issue
3. Re-run validation until all items pass (max 3 iterations)
4. If still failing after 3 iterations, document remaining issues and warn user

**If [NEEDS CLARIFICATION] markers remain**:
1. Extract all `[NEEDS CLARIFICATION: ...]` markers from the spec
2. **LIMIT CHECK**: If more than 3 markers exist, keep only the 3 most critical and make informed guesses for the rest
3. Present options to user in this format:

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

4. Number questions sequentially (Q1, Q2, Q3 - max 3 total)
5. Present all questions together before waiting for responses
6. After user responds, update spec with their answers
7. Re-run validation after all clarifications are resolved

---

## Step 5: Report

1. Present the final specification content to the user in full
2. Report status:
   - **Successful**: All checklist items pass, no ambiguities - spec is ready for implementation
   - **Needs refinement**: Details are still too vague - explain what aspects are unclear

3. **If needs refinement**, ask the user:

> "The specification has some gaps. Would you like to:
> 1. **Clarify** - Answer the open questions to improve the spec
> 2. **Proceed anyway** - Start implementation with current spec (may require changes later)
> 3. **Abandon** - Cancel this feature request"

If user chooses to proceed anyway, acknowledge the risks and begin implementation.

---

## Guidelines

### Focus on WHAT and WHY, Not HOW

- Focus on **WHAT** users need and **WHY**
- Avoid HOW to implement (no tech stack, APIs, code structure)
- Written for business stakeholders, not developers
- DO NOT create any checklists embedded in the spec

### Section Requirements

- **Mandatory sections**: Must be completed for every feature
- **Optional sections**: Include only when relevant to the feature
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### Making Informed Guesses

When creating specs, use reasonable defaults instead of asking about:

- **Data retention**: Industry-standard practices for the domain
- **Performance targets**: Standard web/mobile app expectations unless specified
- **Error handling**: User-friendly messages with appropriate fallbacks
- **Authentication method**: Standard session-based or OAuth2 for web apps
- **Integration patterns**: RESTful APIs unless specified otherwise

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
- "API response time is under 200ms" (too technical)
- "Database can handle 1000 TPS" (implementation detail)
- "React components render efficiently" (framework-specific)
- "Redis cache hit rate above 80%" (technology-specific)

---

## Why This Matters

Writing code for unclear requirements wastes time. A short conversation about requirements saves hours of rework. Your job is to build what the user actually needs, not what they initially said.
"""


def _write_file(path: Path, content: str, display_path: str) -> None:
    """Write a file and report status."""
    action = "Updated" if path.exists() else "Created"
    path.write_text(content)
    click.echo(f"  {action} {display_path}")


def initialize_project() -> bool:
    """Initialize the current directory for swhat specification workflow.

    Creates:
        - .swhat/ directory for user workspace
        - .claude/commands/swhat.specify.md for Claude Code
        - .claude/skills/swhat-feature-workflow/SKILL.md for Claude Code
        - .roo/commands/swhat-specify.md for Roo
        - .roo/skills/swhat-feature-workflow/SKILL.md for Roo

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

    # Claude Code: commands
    claude_commands_dir = cwd / ".claude" / "commands"
    claude_commands_dir.mkdir(parents=True, exist_ok=True)
    _write_file(
        claude_commands_dir / "swhat.specify.md",
        CLAUDE_SPECIFY_COMMAND,
        ".claude/commands/swhat.specify.md",
    )

    # Claude Code: skills
    claude_skill_dir = cwd / ".claude" / "skills" / "swhat-feature-workflow"
    claude_skill_dir.mkdir(parents=True, exist_ok=True)
    _write_file(
        claude_skill_dir / "SKILL.md",
        CLAUDE_FEATURE_SKILL,
        ".claude/skills/swhat-feature-workflow/SKILL.md",
    )

    # Roo: commands (uses dashes, not dots)
    roo_commands_dir = cwd / ".roo" / "commands"
    roo_commands_dir.mkdir(parents=True, exist_ok=True)
    _write_file(
        roo_commands_dir / "swhat-specify.md",
        ROO_SPECIFY_COMMAND,
        ".roo/commands/swhat-specify.md",
    )

    # Roo: skills
    roo_skill_dir = cwd / ".roo" / "skills" / "swhat-feature-workflow"
    roo_skill_dir.mkdir(parents=True, exist_ok=True)
    _write_file(
        roo_skill_dir / "SKILL.md",
        ROO_FEATURE_SKILL,
        ".roo/skills/swhat-feature-workflow/SKILL.md",
    )

    click.echo("")
    click.echo("Initialization complete!")
    click.echo("")
    click.echo("Commands installed:")
    click.echo("  Claude Code: /swhat.specify <feature description>")
    click.echo("  Roo:         /swhat-specify <feature description>")
    click.echo("")
    click.echo("Skills installed (auto-activate on feature requests):")
    click.echo("  swhat-feature-workflow - clarifies requirements before coding")
    return True
