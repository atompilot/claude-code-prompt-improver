---
name: prompt-improver
description: This skill enriches vague prompts with targeted research and clarification before execution. Should be used when a prompt is determined to be vague and requires systematic research, question generation, and execution guidance.
---

# Prompt Improver Skill

## Purpose

Transform vague, ambiguous prompts into actionable, well-defined requests through systematic research and targeted clarification. This skill is invoked via the `/prompt-improver` command.

## When This Skill is Invoked

**Via command:**
- User runs `/prompt-improver [prompt]` to explicitly request prompt improvement
- The command skips clarity evaluation and proceeds directly to research and clarification

**Direct invocation:**
- To enrich a vague prompt with research-based questions
- When building or testing prompt evaluation systems
- When prompt lacks sufficient context even with conversation history

**Assumptions:**
- User has explicitly requested prompt improvement
- Proceed directly to research and clarification

## Quick Mode

When the prompt has **only one clear ambiguity** (e.g., "which file?" or "which approach?"), skip the full 4-phase workflow:

1. Identify the single ambiguity from conversation context or a quick codebase check
2. Ask **1 question** via AskUserQuestion with 2-4 research-grounded options
3. Execute immediately with the user's answer

Use the full workflow below only when multiple aspects need clarification.

## Core Workflow

This skill follows a 4-phase approach to prompt enrichment:

### Phase 1: Research

Plan your research approach (optionally use TodoWrite for complex investigations).

**Research Plan Template:**
1. **Read CLAUDE.md first** - Understand project conventions, architecture, and patterns before exploring
2. **Check conversation history** - Avoid redundant exploration if context already exists
3. **Review codebase** if needed:
   - Use Agent tool with `subagent_type=Explore` for broad architecture discovery and pattern finding
   - Grep/Glob for specific patterns, related files
   - Check git log for recent changes
   - Search for errors, failing tests, TODO/FIXME comments
4. **Gather additional context** as needed:
   - Read local documentation files
   - WebFetch for online documentation
   - WebSearch for best practices, common approaches, current information
5. **Document findings** to ground questions in actual project context

**Critical Rules:**
- NEVER skip research
- Read CLAUDE.md before exploring codebase — it contains project-specific conventions and architecture
- Use Agent tool with `subagent_type=Explore` for broad codebase exploration (not manual Glob/Grep chains)
- Check conversation history before exploring codebase
- Questions must be grounded in actual findings, not assumptions or base knowledge

For detailed research strategies, patterns, and examples, see [references/research-strategies.md](references/research-strategies.md).

### Phase 2: Generate Targeted Questions

Based on research findings, formulate 1-6 questions that will clarify the ambiguity.

**Question Guidelines:**
- **Grounded**: Every option comes from research (codebase findings, documentation, common patterns)
- **Specific**: Avoid vague options like "Other approach"
- **Multiple choice**: Provide 2-4 concrete options per question
- **Focused**: Each question addresses one decision point
- **Contextual**: Include brief explanations of trade-offs

**Number of Questions:**
- **1-2 questions**: Simple ambiguity (which file? which approach?)
- **3-4 questions**: Moderate complexity (scope + approach + validation)
- **5-6 questions**: Complex scenarios (major feature with multiple decision points)

For question templates, effective patterns, and examples, see [references/question-patterns.md](references/question-patterns.md).

### Phase 3: Get Clarification

Use the AskUserQuestion tool to present your research-grounded questions.

**AskUserQuestion Format:**
```
- question: Clear, specific question ending with ?
- header: Short label (max 12 chars) for UI display
- multiSelect: false (unless choices aren't mutually exclusive)
- options: Array of 2-4 specific choices from research
  - label: Concise choice text (1-5 words)
  - description: Context about this option (trade-offs, implications)
```

**Important:** Always include multiSelect field (true/false). User can always select "Other" for custom input.

### Phase 4: Execute with Context

Proceed with the original user request using:
- Original prompt intent
- Clarification answers from user
- Research findings and context
- Conversation history

Execute the request as if it had been clear from the start.

## Examples

### Example 1: Command Invocation → Research → Questions → Execution

**User runs:** `/prompt-improver fix the bug`
**Skill invoked:** Yes (user requested improvement)

**Research plan:**
1. Check conversation history for recent errors
2. Explore codebase for failing tests
3. Grep for TODO/FIXME comments
4. Check git log for recent problem areas

**Research findings:**
- Recent conversation mentions login failures
- auth.py:145 has try/catch swallowing errors
- Tests failing in test_auth.py

**Questions generated:**
1. Which bug are you referring to?
   - Login authentication failure (auth.py:145)
   - Session timeout issues (session.py:89)
   - Other

**User answer:** Login authentication failure

**Execution:** Fix the error handling in auth.py:145 that's causing login failures

For comprehensive examples showing various prompt types and transformations, see [references/examples.md](references/examples.md).

## Key Principles

1. **Assume Vagueness**: Skill is invoked on-demand via `/prompt-improver` command
2. **Research First**: Always gather context before formulating questions
3. **Ground Questions**: Use research findings, not assumptions or base knowledge
4. **Be Specific**: Provide concrete options from actual codebase/context
5. **Stay Focused**: Max 1-6 questions, each addressing one decision point
6. **Systematic Approach**: Follow 4-phase workflow (Research → Questions → Clarify → Execute)

## Progressive Disclosure

This SKILL.md contains the core workflow and essentials. For deeper guidance:

- **Research strategies**: [references/research-strategies.md](references/research-strategies.md)
- **Question patterns**: [references/question-patterns.md](references/question-patterns.md)
- **Comprehensive examples**: [references/examples.md](references/examples.md)

Load these references only when detailed guidance is needed on specific aspects of prompt improvement.
