## code_review

Automated code review with quality, security, and style checks.

### Methods

| Method | Description | Args |
|--------|-------------|------|
| `review` | Full code review | `code` or `file_path` |
| `security` | Security vulnerability scan | `code` or `file_path` |
| `style` | Style convention check | `code` or `file_path` |
| `quality` | Quality metrics check | `code` or `file_path` |
| `checklist` | Generate review checklist | `category` |

### Examples

**Full code review:**
~~~json
{
    "thoughts": ["Review this code for issues"],
    "tool_name": "code_review:review",
    "tool_args": {"file_path": "/path/to/file.py"}
}
~~~

**Security scan:**
~~~json
{
    "thoughts": ["Check for security vulnerabilities"],
    "tool_name": "code_review:security",
    "tool_args": {"file_path": "/path/to/file.py"}
}
~~~

**Style check:**
~~~json
{
    "thoughts": ["Check code style compliance"],
    "tool_name": "code_review:style",
    "tool_args": {"code": "def foo(): pass"}
}
~~~

**Generate checklist:**
~~~json
{
    "thoughts": ["Get a PR review checklist"],
    "tool_name": "code_review:checklist",
    "tool_args": {"category": "pr"}
}
~~~

### Checklist Categories

- `general` - Full code review checklist
- `security` - Security-focused review
- `pr` - Pull request review

### Security Checks

- Hardcoded credentials (passwords, API keys, secrets)
- SQL injection vulnerabilities
- Use of `eval()` / `exec()`
- Unsafe subprocess calls
- Pickle deserialization risks
- YAML unsafe load

### Quality Checks

- Long functions (>50 lines)
- Too many function arguments
- Missing docstrings
- Bare except clauses
- Syntax errors

### When to Use

- Before submitting a PR
- During code review process
- When auditing code for security
- To ensure code quality standards

