## git_tool

Comprehensive git version control operations without terminal access.

### Available Methods

Use `git_tool:method_name` to call specific methods:

| Method | Description | Key Args |
|--------|-------------|----------|
| `status` | Working directory status | `repo_path` (optional) |
| `diff` | Show changes | `target`, `staged` |
| `log` | Commit history | `count`, `author`, `oneline` |
| `blame` | Line-by-line history | `file` |
| `branch` | Branch operations | `action` (list/create/delete), `name` |
| `show` | Commit details | `commit` |
| `add` | Stage files | `files` |
| `commit` | Create commit | `message`, `add_all` |
| `stash` | Stash changes | `action` (push/pop/list), `message` |
| `checkout` | Switch branch/restore | `target`, `create` |
| `merge` | Merge branch | `branch` |
| `pull` | Pull from remote | `remote`, `branch` |
| `push` | Push to remote | `remote`, `branch`, `set_upstream` |

### Usage Examples

**Check status:**
~~~json
{
    "thoughts": ["Let me check the current git status"],
    "tool_name": "git_tool:status",
    "tool_args": {}
}
~~~

**View recent commits:**
~~~json
{
    "thoughts": ["Show last 5 commits"],
    "tool_name": "git_tool:log",
    "tool_args": {
        "count": 5
    }
}
~~~

**Create and commit:**
~~~json
{
    "thoughts": ["Stage all changes and commit"],
    "tool_name": "git_tool:commit",
    "tool_args": {
        "message": "Add new feature",
        "add_all": true
    }
}
~~~

**Create new branch:**
~~~json
{
    "thoughts": ["Create feature branch"],
    "tool_name": "git_tool:checkout",
    "tool_args": {
        "target": "feature/new-feature",
        "create": true
    }
}
~~~

**View diff:**
~~~json
{
    "thoughts": ["See what changed"],
    "tool_name": "git_tool:diff",
    "tool_args": {
        "staged": false
    }
}
~~~

**Blame a file:**
~~~json
{
    "thoughts": ["Who changed this file?"],
    "tool_name": "git_tool:blame",
    "tool_args": {
        "file": "path/to/file.py"
    }
}
~~~

**Merge branch:**
~~~json
{
    "thoughts": ["Merge feature branch into current"],
    "tool_name": "git_tool:merge",
    "tool_args": {
        "branch": "feature/new-feature"
    }
}
~~~

### When to Use
- Checking repository status before making changes
- Committing completed work
- Managing branches for features/fixes
- Viewing history and blame
- Syncing with remote repositories

