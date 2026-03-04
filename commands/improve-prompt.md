---
name: improve-prompt
description: Manually optimize a vague prompt through research and clarifying questions before execution. Usage: /improve-prompt [your prompt]
---

# Prompt Improver Command

The user wants to improve and execute the following prompt:

**"$ARGUMENTS"**

## Instructions

This prompt has been explicitly submitted for improvement. Treat it as vague and proceed directly with the prompt-improver skill.

1. Invoke the **prompt-improver** skill to research and generate clarifying questions
2. The skill will guide you through: Research → Questions → Clarify → Execute
3. After getting the user's answers, execute the original request with full context

Do NOT evaluate whether the prompt is clear or vague — the user has chosen to improve it. Skip evaluation and go straight to the skill workflow.

If no arguments were provided, ask the user: "Please provide the prompt you want to improve. Usage: `/improve-prompt [your prompt]`"
