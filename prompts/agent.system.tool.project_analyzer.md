## project_analyzer

Analyze project structure, detect frameworks, and understand codebases.

### Methods

| Method | Description | Args |
|--------|-------------|------|
| `analyze` | Full project analysis | `path` |
| `tree` | Generate file tree | `path`, `depth` |
| `detect` | Detect framework/type | `path` |
| `stats` | Project statistics | `path` |
| `find` | Find files by pattern | `path`, `pattern` |

### Examples

**Full project analysis:**
~~~json
{
    "thoughts": ["Understand this project structure"],
    "tool_name": "project_analyzer:analyze",
    "tool_args": {"path": "/path/to/project"}
}
~~~

**Generate file tree:**
~~~json
{
    "thoughts": ["Show project file structure"],
    "tool_name": "project_analyzer:tree",
    "tool_args": {
        "path": "/path/to/project",
        "depth": 3
    }
}
~~~

**Detect framework:**
~~~json
{
    "thoughts": ["What framework is this project using?"],
    "tool_name": "project_analyzer:detect",
    "tool_args": {"path": "/path/to/project"}
}
~~~

**Get statistics:**
~~~json
{
    "thoughts": ["Get project size and language breakdown"],
    "tool_name": "project_analyzer:stats",
    "tool_args": {"path": "/path/to/project"}
}
~~~

**Find files:**
~~~json
{
    "thoughts": ["Find all Python test files"],
    "tool_name": "project_analyzer:find",
    "tool_args": {
        "path": "/path/to/project",
        "pattern": "test_*.py"
    }
}
~~~

### Detected Frameworks

**Python:** Django, Flask, FastAPI
**JavaScript:** React, Vue.js, Next.js, Express
**Java:** Maven, Gradle
**Other:** Go, Rust

### When to Use
- When starting work on a new codebase
- To understand project organization
- To find specific files or patterns
- Before major refactoring or changes
- To verify project structure follows conventions

