# Question Patterns for Effective Clarification

This reference provides templates, patterns, and best practices for formulating clarifying questions that are grounded in research and lead to actionable answers.

## Table of Contents

- [Question Construction Principles](#question-construction-principles)
- [AskUserQuestion Tool Format](#askuserquestion-tool-format)
- [Question Templates by Category](#question-templates-by-category)
- [Number of Questions Guidelines](#number-of-questions-guidelines)
- [Option Generation Best Practices](#option-generation-best-practices)
- [Common Pitfalls](#common-pitfalls)

## Question Construction Principles

### Core Principles

1. **Ground in Research**: Every option must come from actual findings
   - Codebase exploration results
   - Documentation references
   - Web search for best practices
   - Git history for patterns

2. **Be Specific**: Avoid generic options
   - Bad: "Use a different approach"
   - Good: "Use JWT tokens with HttpOnly cookies"

3. **Provide Context**: Explain trade-offs in descriptions
   - Why this option exists
   - What it implies
   - When it's appropriate

4. **Stay Focused**: One decision point per question
   - Bad: "Which file and what approach?"
   - Good: "Which file?" (separate question for approach)

5. **Enable Choice**: 2-4 options per question
   - Fewer than 2: Not a choice
   - More than 4: Overwhelming
   - "Other" is always available automatically

### Question Quality Checklist

Before formulating questions, verify:

- [ ] Completed research phase with documented findings
- [ ] Each option based on actual research (not assumptions)
- [ ] Each option is specific and actionable
- [ ] Context/trade-offs included in descriptions
- [ ] Questions are independent (can be answered in any order)
- [ ] Total questions: 1-6 based on complexity

## AskUserQuestion Tool Format

### Complete Tool Structure

```json
{
  "questions": [
    {
      "question": "Clear, specific question ending with ?",
      "header": "Short label (max 12 chars)",
      "multiSelect": false,
      "options": [
        {
          "label": "Concise choice (1-5 words)",
          "description": "Context about this option, trade-offs, implications"
        },
        {
          "label": "Another choice",
          "description": "Why this option, when to use it"
        }
      ]
    }
  ]
}
```

### Field Guidelines

**question:**
- Must end with `?`
- Should be conversational and clear
- Include context from research if helpful
- Examples:
  - "Which authentication approach should we implement?"
  - "Where should the validation logic be added?"
  - "What scope should this refactoring cover?"

**header:**
- Maximum 12 characters (strict limit)
- Acts as visual label/tag in UI
- Should be noun or noun phrase
- Examples:
  - "Auth method" (11 chars)
  - "File target" (11 chars)
  - "Scope" (5 chars)
  - "Approach" (8 chars)

**multiSelect:**
- `false`: User selects exactly one option (default for most cases)
- `true`: User can select multiple options (when choices aren't mutually exclusive)
- Always explicitly specify (don't rely on defaults)

**options:**
- Minimum 2, maximum 4 options
- Each must have `label` and `description`

**label:**
- 1-5 words typically
- Specific and scannable
- Examples:
  - "JWT with refresh tokens"
  - "Session-based auth"
  - "OAuth 2.0 integration"

**description:**
- Explain what this option means
- Include trade-offs or implications
- Provide context for decision-making
- Examples:
  - "Stateless authentication using JWT access tokens (short-lived) and refresh tokens (stored securely). Best for distributed systems."
  - "Server-side session storage using Redis. Simpler but requires sticky sessions or shared session store."

## Question Templates by Category

### Target Identification Questions

**When:** Unclear which file, function, or component to modify

**Template 1: File Selection**
```json
{
  "question": "Which file should be modified?",
  "header": "Target file",
  "multiSelect": false,
  "options": [
    {
      "label": "src/auth/login.ts",
      "description": "Main login handler with authentication logic (currently 245 lines)"
    },
    {
      "label": "src/auth/middleware.ts",
      "description": "Authentication middleware used by all protected routes (89 lines)"
    },
    {
      "label": "src/auth/session.ts",
      "description": "Session management and validation utilities (156 lines)"
    }
  ]
}
```

**Other target templates:** Function/Method Selection (header: "Function", options list specific functions with file:line references).

### Approach/Implementation Questions

**When:** Target is clear, but implementation approach is ambiguous

**Template: Technical Approach**
```json
{
  "question": "Which authentication approach should we implement?",
  "header": "Auth method",
  "multiSelect": false,
  "options": [
    {
      "label": "JWT with HttpOnly cookies",
      "description": "Store JWT in HttpOnly cookies. Prevents XSS attacks, simpler client-side code. Requires CSRF protection."
    },
    {
      "label": "JWT in Authorization header",
      "description": "Client stores JWT in memory, sends in Bearer token. More flexible for mobile apps, requires client-side token management."
    },
    {
      "label": "Session-based with Redis",
      "description": "Server-side sessions stored in Redis. Traditional approach, easier to invalidate, requires session store infrastructure."
    }
  ]
}
```

**Other approach templates:** Architectural Pattern (header: "Pattern", options compare middleware vs service layer vs schema-based approaches with trade-offs).

### Scope Questions

**When:** Unclear how much work should be done

**Template: Feature Scope**
```json
{
  "question": "What scope should this refactoring cover?",
  "header": "Scope",
  "multiSelect": false,
  "options": [
    {
      "label": "Single function only",
      "description": "Refactor just getUserById(). Minimal change, quick to implement and test."
    },
    {
      "label": "Entire UserRepository class",
      "description": "Refactor all user data access methods (8 functions). Consistent patterns across class."
    },
    {
      "label": "All repository classes",
      "description": "Apply pattern to UserRepository, ProductRepository, OrderRepository (3 classes, 24 functions). Codebase-wide consistency."
    }
  ]
}
```

**Other scope templates:** Test Coverage Scope (header: "Test scope", options: happy path only / + error cases / full coverage with edge cases).

### Other Question Categories

**Priority/Order** (header: "Priority" or "Order") — When multiple tasks exist, list them by severity with descriptions. Include dependency context.

**Configuration** (header: "Library", "Timeout", etc.) — For library/tool selection or configuration values. Always mention what's already in the project (e.g., "Already in package.json").

## Number of Questions Guidelines

- **1 question**: Single ambiguity — which file, which approach, or which scope (Quick Mode)
- **2-3 questions**: Moderate complexity — approach + scope, or target + configuration
- **4-6 questions**: Major features with multiple architectural decisions — use sparingly, most scenarios need 1-3

## Option Generation Best Practices

### Grounding Options in Research

**Bad (Assumption-Based):**
```json
{
  "label": "Use MongoDB",
  "description": "NoSQL database, good for flexibility"
}
```

**Good (Research-Grounded):**
```json
{
  "label": "Use MongoDB",
  "description": "NoSQL database. Project already uses MongoDB for user data (see db/connection.ts). Consistent with existing stack."
}
```

### Providing Actionable Context

**Bad (Vague):**
```json
{
  "label": "Refactor approach",
  "description": "Better way to organize code"
}
```

**Good (Specific):**
```json
{
  "label": "Extract to service layer",
  "description": "Move business logic from controllers to UserService class. Follows repository pattern already used in OrderService and ProductService."
}
```

### Including Trade-offs

**Bad (One-Sided):**
```json
{
  "label": "Microservices architecture",
  "description": "Modern, scalable approach"
}
```

**Good (Balanced):**
```json
{
  "label": "Microservices architecture",
  "description": "Split into auth-service and user-service. Better scaling and independence, but adds deployment complexity. Team has Docker expertise."
}
```

### Using Codebase Evidence

**Research findings inform options:**

```
Research Results:
- Found 3 API clients: src/api/rest-client.ts, src/api/graphql-client.ts, src/api/websocket-client.ts
- rest-client.ts has timeout config (line 23: timeout: 30000)
- graphql-client.ts missing timeout (potential bug)
- websocket-client.ts uses different pattern (reconnect logic)
```

**Generated question:**
```json
{
  "question": "Which API client needs timeout configuration?",
  "header": "API client",
  "multiSelect": false,
  "options": [
    {
      "label": "REST client (src/api/rest-client.ts)",
      "description": "Already has 30s timeout. Update existing configuration."
    },
    {
      "label": "GraphQL client (src/api/graphql-client.ts)",
      "description": "Missing timeout configuration. Likely the source of hanging requests."
    },
    {
      "label": "WebSocket client (src/api/websocket-client.ts)",
      "description": "Uses reconnect pattern instead of timeout. Different approach needed."
    }
  ]
}
```

## Common Pitfalls

### Pitfall 1: Generic Options

**Bad:**
```json
{
  "label": "Best practice approach",
  "description": "Use industry standard methods"
}
```

**Why bad:** Not actionable, no clear guidance

**Fix:**
```json
{
  "label": "Repository pattern with dependency injection",
  "description": "Separate data access into UserRepository, injected via constructor. Used in OrderService (see src/services/order.service.ts:15)."
}
```

### Pitfall 2: Too Many Options

**Bad:**
```json
{
  "question": "Which approach?",
  "options": [
    "Approach A",
    "Approach B",
    "Approach C",
    "Approach D",
    "Approach E",
    "Approach F"
  ]
}
```

**Why bad:** Overwhelming, decision paralysis

**Fix:** Narrow to 2-4 most relevant options based on research. If more than 4, create multiple questions or categorize.

### Pitfall 3: Leading Questions

**Bad:**
```json
{
  "question": "Should we use the superior JWT approach?",
  "options": ["Yes, JWT", "No, sessions"]
}
```

**Why bad:** Biased question influences answer

**Fix:**
```json
{
  "question": "Which authentication mechanism should be implemented?",
  "options": [
    {
      "label": "JWT tokens",
      "description": "Stateless, scales horizontally. Client manages tokens. Trade-off: harder to invalidate."
    },
    {
      "label": "Server-side sessions",
      "description": "Stateful, easier to invalidate. Server manages state. Trade-off: requires shared session store."
    }
  ]
}
```

### Pitfall 4: Compound Questions

**Bad:**
```json
{
  "question": "Which library and what configuration should be used?",
  "options": [
    "Library A with Config X",
    "Library A with Config Y",
    "Library B with Config X",
    "Library B with Config Y"
  ]
}
```

**Why bad:** Mixing multiple decisions, exponential option growth

**Fix:** Separate into two questions
```json
[
  {
    "question": "Which library?",
    "options": ["Library A", "Library B"]
  },
  {
    "question": "What configuration?",
    "options": ["Config X", "Config Y"]
  }
]
```

### Pitfall 5: Asking Without Research

**Bad:**
```json
{
  "question": "How should we implement authentication?",
  "options": [
    {"label": "Some approach", "description": "I think this might work"},
    {"label": "Another approach", "description": "This could also work"}
  ]
}
```

**Why bad:** Not grounded in codebase reality, generic options

**Fix:** Research first
```
1. Explore codebase for existing auth patterns
2. Check package.json for auth libraries
3. Review similar implementations in repo
4. Web search for framework-specific best practices
5. Generate options based on findings
```

## Summary Checklist

Before using AskUserQuestion tool:

- [ ] Completed research phase with documented findings
- [ ] Each option grounded in research (not assumptions)
- [ ] Each option is specific and actionable (not generic)
- [ ] Descriptions include context and trade-offs
- [ ] Questions are focused (one decision per question)
- [ ] Using 1-6 questions based on complexity
- [ ] Each question has 2-4 options
- [ ] header field is ≤12 characters
- [ ] multiSelect explicitly set (true/false)
- [ ] question ends with `?`

**Remember:** The goal is clarity through specificity. Every option should be traceable back to research findings. Generic or assumed options undermine trust and lead to poor decisions.
