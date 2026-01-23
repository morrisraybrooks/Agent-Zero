## code_refactor tool

Automated code refactoring for renaming, extracting functions, and improving code structure.

### Available Methods

Use `code_refactor:method_name` to call specific methods:

| Method | Description | Required Args |
|--------|-------------|---------------|
| `rename` | Rename a symbol throughout code | `code`/`file_path`, `old_name`, `new_name` |
| `extract_function` | Extract code block into function | `code`, `start_line`, `end_line`, `function_name` |
| `inline_variable` | Replace variable with its value | `code`, `variable` |
| `add_docstring` | Suggest docstrings for functions/classes | `code` |
| `format_code` | Apply basic formatting fixes | `code` |
| `remove_unused_imports` | Detect and suggest removing unused imports | `code` |

### Usage Examples

**Rename a symbol:**
~~~json
{
    "thoughts": ["I need to rename the function 'calc' to 'calculate_total'"],
    "tool_name": "code_refactor:rename",
    "tool_args": {
        "code": "def calc(x): return x * 2\nresult = calc(5)",
        "old_name": "calc",
        "new_name": "calculate_total"
    }
}
~~~

**Extract a function:**
~~~json
{
    "thoughts": ["Lines 10-15 should be extracted into a helper function"],
    "tool_name": "code_refactor:extract_function",
    "tool_args": {
        "code": "...",
        "start_line": 10,
        "end_line": 15,
        "function_name": "validate_user_input"
    }
}
~~~

**Inline a variable:**
~~~json
{
    "thoughts": ["The variable 'temp' is only used once, inline it"],
    "tool_name": "code_refactor:inline_variable",
    "tool_args": {
        "code": "temp = get_value()\nresult = temp * 2",
        "variable": "temp"
    }
}
~~~

**Add docstrings:**
~~~json
{
    "thoughts": ["Generate docstring suggestions for all undocumented functions"],
    "tool_name": "code_refactor:add_docstring",
    "tool_args": {
        "code": "def process(data, limit=10): ..."
    }
}
~~~

**Format code:**
~~~json
{
    "thoughts": ["Apply basic formatting fixes to this code"],
    "tool_name": "code_refactor:format_code",
    "tool_args": {
        "code": "x=1+2\ny=  3"
    }
}
~~~

**Find unused imports:**
~~~json
{
    "thoughts": ["Check for any unused imports that can be removed"],
    "tool_name": "code_refactor:remove_unused_imports",
    "tool_args": {
        "code": "import os\nimport json\nprint('hello')"
    }
}
~~~

### When to Use
- Renaming variables, functions, or classes consistently
- Extracting repeated code into reusable functions
- Simplifying code by inlining single-use variables
- Adding documentation to undocumented code
- Cleaning up code style and formatting
- Removing dead/unused imports

