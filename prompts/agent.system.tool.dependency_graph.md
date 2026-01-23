## dependency_graph tool

Map imports, module relationships, and project dependencies.

### Available Methods

Use `dependency_graph:method_name` to call specific methods:

| Method | Description | Required Args |
|--------|-------------|---------------|
| `analyze` | Analyze dependencies for file/directory | `path` |
| `imports` | List all imports in a file with details | `file_path` |
| `dependents` | Find files that depend on a module | `module`, `directory` |
| `graph` | Generate text-based dependency graph | `path` |

### Usage Examples

**Analyze file dependencies:**
~~~json
{
    "thoughts": ["I need to understand what this file depends on"],
    "tool_name": "dependency_graph:analyze",
    "tool_args": {
        "path": "/path/to/file.py"
    }
}
~~~

**Analyze project dependencies:**
~~~json
{
    "thoughts": ["What are all the third-party dependencies in this project?"],
    "tool_name": "dependency_graph:analyze",
    "tool_args": {
        "path": "/path/to/project/"
    }
}
~~~

**List detailed imports:**
~~~json
{
    "thoughts": ["Show me all imports with their line numbers"],
    "tool_name": "dependency_graph:imports",
    "tool_args": {
        "file_path": "/path/to/file.py"
    }
}
~~~

**Find what depends on a module:**
~~~json
{
    "thoughts": ["What files use the database module?"],
    "tool_name": "dependency_graph:dependents",
    "tool_args": {
        "module": "database",
        "directory": "/path/to/project/"
    }
}
~~~

**Generate dependency graph:**
~~~json
{
    "thoughts": ["Visualize the project dependencies"],
    "tool_name": "dependency_graph:graph",
    "tool_args": {
        "path": "/path/to/project/"
    }
}
~~~

### Categories
- **Standard Library**: Built-in Python modules (os, sys, json, etc.)
- **Third Party**: External packages (requests, numpy, etc.)
- **Local/Project**: Project-internal modules

### When to Use
- Understanding project structure
- Identifying external dependencies
- Finding circular dependencies
- Preparing for refactoring
- Documenting architecture

