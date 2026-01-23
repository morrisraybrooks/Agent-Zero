## Testing Tools

Two tools for generating and running tests: `test_generator` and `test_runner`.

---

## test_generator

Auto-generate unit tests from source code.

### Methods

| Method | Description | Args |
|--------|-------------|------|
| `generate` | Generate tests for file/code | `code` or `file_path` |
| `template` | Get test template for function | `function` |
| `fixtures` | Suggest pytest fixtures | `code` or `file_path` |
| `coverage` | Suggest tests for better coverage | `code` or `file_path` |

### Examples

~~~json
{
    "thoughts": ["Generate tests for this module"],
    "tool_name": "test_generator:generate",
    "tool_args": {"file_path": "/path/to/module.py"}
}
~~~

~~~json
{
    "thoughts": ["Get a test template for process_data"],
    "tool_name": "test_generator:template",
    "tool_args": {"function": "process_data"}
}
~~~

---

## test_runner

Run tests and analyze results.

### Methods

| Method | Description | Args |
|--------|-------------|------|
| `run` | Run tests | `path`, `target`, `framework` |
| `coverage` | Run with coverage | `path`, `target` |
| `failed` | Re-run failed tests | `path` |
| `watch` | Suggest watch command | `path` |
| `analyze` | Analyze test output | `output` |

### Examples

**Run all tests:**
~~~json
{
    "thoughts": ["Run the test suite"],
    "tool_name": "test_runner:run",
    "tool_args": {"path": "/path/to/project"}
}
~~~

**Run specific test:**
~~~json
{
    "thoughts": ["Run tests for user module"],
    "tool_name": "test_runner:run",
    "tool_args": {
        "path": "/path/to/project",
        "target": "tests/test_user.py"
    }
}
~~~

**Run with coverage:**
~~~json
{
    "thoughts": ["Check test coverage"],
    "tool_name": "test_runner:coverage",
    "tool_args": {"path": "/path/to/project"}
}
~~~

**Re-run failed:**
~~~json
{
    "thoughts": ["Re-run only the failed tests"],
    "tool_name": "test_runner:failed",
    "tool_args": {"path": "/path/to/project"}
}
~~~

### Supported Frameworks
- **pytest** (Python - default)
- **unittest** (Python)
- **npm test** (JavaScript/Node.js)

### When to Use
- After making code changes to verify correctness
- Before committing to ensure tests pass
- To generate test scaffolding for new code
- To improve test coverage

