## code_generator

Generate code from templates, scaffolding, and design patterns.

### Methods

| Method | Description | Args |
|--------|-------------|------|
| `scaffold` | Project scaffolding | `type`, `name` |
| `template` | Code templates | `type`, `language`, `name` |
| `pattern` | Design patterns | `pattern`, `language` |
| `boilerplate` | Boilerplate code | `type` |
| `api` | API endpoints | `framework`, `resource` |

### Examples

**Generate project scaffold:**
~~~json
{
    "thoughts": ["Create a new FastAPI project structure"],
    "tool_name": "code_generator:scaffold",
    "tool_args": {
        "type": "fastapi",
        "name": "my_api"
    }
}
~~~

**Get function template:**
~~~json
{
    "thoughts": ["Need a Python async function template"],
    "tool_name": "code_generator:template",
    "tool_args": {
        "type": "async",
        "language": "python",
        "name": "fetch_data"
    }
}
~~~

**Generate design pattern:**
~~~json
{
    "thoughts": ["Implement singleton pattern"],
    "tool_name": "code_generator:pattern",
    "tool_args": {
        "pattern": "singleton",
        "language": "python"
    }
}
~~~

**Generate API endpoint:**
~~~json
{
    "thoughts": ["Create CRUD API for users"],
    "tool_name": "code_generator:api",
    "tool_args": {
        "framework": "fastapi",
        "resource": "user"
    }
}
~~~

### Scaffold Types
- `python` - Standard Python package
- `fastapi` - FastAPI project
- `express` - Express.js project

### Template Types
- `function` - Function with docstring
- `class` - Class with methods
- `async` - Async function

### Design Patterns
- `singleton` - Single instance pattern
- `factory` - Object creation pattern
- `observer` - Event subscription pattern
- `decorator` - Function wrapper pattern

### Boilerplate Types
- `cli` - Command-line interface
- `config` - Configuration management
- `logging` - Logging setup

### When to Use
- Starting new projects
- Need standardized code structures
- Implementing design patterns
- Creating CRUD APIs quickly

