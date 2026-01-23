## debug_tool

Parse errors, analyze stack traces, and suggest fixes.

### Methods

| Method | Description | Args |
|--------|-------------|------|
| `parse` | Parse error message | `error` |
| `analyze` | Analyze stack trace | `traceback` |
| `suggest` | Suggest fixes | `error`, `context` |
| `explain` | Explain error type | `type` |
| `patterns` | Common error patterns | `language` |

### Examples

**Parse an error:**
~~~json
{
    "thoughts": ["Understand this error"],
    "tool_name": "debug_tool:parse",
    "tool_args": {
        "error": "NameError: name 'x' is not defined"
    }
}
~~~

**Analyze stack trace:**
~~~json
{
    "thoughts": ["Find where error occurred"],
    "tool_name": "debug_tool:analyze",
    "tool_args": {
        "traceback": "Traceback (most recent call last):\n  File 'app.py', line 10..."
    }
}
~~~

**Get fix suggestions:**
~~~json
{
    "thoughts": ["How do I fix this KeyError?"],
    "tool_name": "debug_tool:suggest",
    "tool_args": {
        "error": "KeyError: 'username'"
    }
}
~~~

**Explain error type:**
~~~json
{
    "thoughts": ["What is AttributeError?"],
    "tool_name": "debug_tool:explain",
    "tool_args": {
        "type": "AttributeError"
    }
}
~~~

**Show common patterns:**
~~~json
{
    "thoughts": ["Show me common Python errors"],
    "tool_name": "debug_tool:patterns",
    "tool_args": {
        "language": "python"
    }
}
~~~

### Supported Error Types

- `NameError` - Variable not defined
- `TypeError` - Wrong type
- `ValueError` - Invalid value
- `AttributeError` - Missing attribute
- `KeyError` - Dict key not found
- `IndexError` - Index out of range
- `ImportError` - Import failed
- `FileNotFoundError` - File missing
- `SyntaxError` - Invalid syntax
- `IndentationError` - Bad indentation

### When to Use

- When encountering errors during development
- To understand unfamiliar error types
- To get quick fix suggestions
- Before asking for help with an error

