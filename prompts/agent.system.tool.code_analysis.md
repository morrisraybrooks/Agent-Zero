## code_analysis tool

Analyze source code structure, find definitions, references, and understand code relationships.

### Available Methods

Use `code_analysis:method_name` to call specific methods:

| Method | Description | Required Args |
|--------|-------------|---------------|
| `parse` | Parse code and extract structure | `code` or `file_path` |
| `find_definition` | Find where a symbol is defined | `symbol`, `code`/`file_path` |
| `find_references` | Find all uses of a symbol | `symbol`, `code`/`file_path` |
| `analyze_imports` | List and categorize imports | `code` or `file_path` |
| `get_call_graph` | Show function call relationships | `code` or `file_path` |
| `get_structure` | High-level code overview | `code` or `file_path` |

### Usage Examples

**Parse code structure:**
~~~json
{
    "thoughts": ["I need to understand the structure of this Python file"],
    "tool_name": "code_analysis:parse",
    "tool_args": {
        "file_path": "/path/to/file.py",
        "language": "python"
    }
}
~~~

**Find where a function is defined:**
~~~json
{
    "thoughts": ["I need to find where process_data is defined"],
    "tool_name": "code_analysis:find_definition",
    "tool_args": {
        "file_path": "/path/to/file.py",
        "symbol": "process_data"
    }
}
~~~

**Find all references to a class:**
~~~json
{
    "thoughts": ["I need to find all places where UserManager is used"],
    "tool_name": "code_analysis:find_references",
    "tool_args": {
        "code": "class UserManager:...",
        "symbol": "UserManager"
    }
}
~~~

**Analyze imports:**
~~~json
{
    "thoughts": ["I want to see what dependencies this file has"],
    "tool_name": "code_analysis:analyze_imports",
    "tool_args": {
        "file_path": "/path/to/file.py"
    }
}
~~~

**Get function call graph:**
~~~json
{
    "thoughts": ["I need to understand the call flow in this code"],
    "tool_name": "code_analysis:get_call_graph",
    "tool_args": {
        "file_path": "/path/to/file.py"
    }
}
~~~

### Supported Languages
- **Python**: Full AST parsing support
- **JavaScript/TypeScript**: Basic pattern-based parsing

### When to Use
- Understanding unfamiliar codebases
- Before refactoring to find all references
- Debugging to trace function calls
- Reviewing code dependencies
- Finding where symbols are defined

