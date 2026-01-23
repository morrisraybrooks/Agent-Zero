## code_complexity tool

Analyze code quality, measure complexity, and detect code smells.

### Available Methods

Use `code_complexity:method_name` to call specific methods:

| Method | Description | Required Args |
|--------|-------------|---------------|
| `analyze` | Full complexity analysis with smells | `code` or `file_path` |
| `cyclomatic` | Calculate cyclomatic complexity | `code` or `file_path` |
| `smells` | Detect common code smells | `code` or `file_path` |
| `metrics` | Get code metrics (lines, functions) | `code` or `file_path` |

### Usage Examples

**Full analysis:**
~~~json
{
    "thoughts": ["I need to understand the complexity of this module"],
    "tool_name": "code_complexity:analyze",
    "tool_args": {
        "file_path": "/path/to/file.py"
    }
}
~~~

**Check cyclomatic complexity:**
~~~json
{
    "thoughts": ["Check which functions are too complex"],
    "tool_name": "code_complexity:cyclomatic",
    "tool_args": {
        "code": "def process(x):\n    if x > 0:\n        if x > 10: ..."
    }
}
~~~

**Detect code smells:**
~~~json
{
    "thoughts": ["Look for code quality issues"],
    "tool_name": "code_complexity:smells",
    "tool_args": {
        "file_path": "/path/to/file.py"
    }
}
~~~

**Get metrics:**
~~~json
{
    "thoughts": ["How big is this file?"],
    "tool_name": "code_complexity:metrics",
    "tool_args": {
        "file_path": "/path/to/file.py"
    }
}
~~~

### Complexity Ratings
- **1-5**: ✅ Simple - Easy to understand and maintain
- **6-10**: ⚠️ Moderate - Consider breaking into smaller functions
- **11-20**: 🔶 Complex - Should be refactored
- **21+**: 🔴 Very Complex - Must be refactored immediately

### Code Smells Detected
- Long lines (>120 characters)
- Long functions (>50 lines)
- Too many parameters (>5)
- Deep nesting (>3 levels)
- TODO/FIXME comments
- Magic numbers

### When to Use
- Before refactoring to identify problem areas
- During code review to assess quality
- After writing code to check complexity
- Understanding unfamiliar codebases

