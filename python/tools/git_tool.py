"""
Git Integration Tool for Agent Zero
Provides comprehensive git operations without terminal access.
"""
import subprocess
import os
from python.helpers.tool import Tool, Response


class GitTool(Tool):
    """
    Tool for git version control operations.
    
    Methods:
    - status: Show working directory status
    - diff: Show changes between commits/working directory
    - log: Show commit history
    - blame: Show who changed each line
    - branch: List, create, switch branches
    - commit: Stage and commit changes
    - stash: Stash/unstash changes
    - remote: Remote repository operations
    """

    async def execute(self, **kwargs) -> Response:
        method = self.method or self.args.get("method", "status")
        
        methods = {
            "status": self.git_status,
            "diff": self.git_diff,
            "log": self.git_log,
            "blame": self.git_blame,
            "branch": self.git_branch,
            "commit": self.git_commit,
            "stash": self.git_stash,
            "show": self.git_show,
            "add": self.git_add,
            "checkout": self.git_checkout,
            "merge": self.git_merge,
            "pull": self.git_pull,
            "push": self.git_push,
        }
        
        if method in methods:
            return await methods[method]()
        else:
            return Response(
                message=f"Unknown method '{method}'. Available: {', '.join(methods.keys())}",
                break_loop=False
            )

    def _run_git(self, *args, cwd=None) -> tuple[bool, str]:
        """Execute a git command and return (success, output)."""
        try:
            cwd = cwd or self.args.get("repo_path", "") or os.getcwd()
            result = subprocess.run(
                ["git"] + list(args),
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return True, result.stdout.strip()
            else:
                return False, result.stderr.strip()
        except subprocess.TimeoutExpired:
            return False, "Git command timed out"
        except Exception as e:
            return False, str(e)

    async def git_status(self) -> Response:
        """Show working directory status."""
        success, output = self._run_git("status", "--short", "--branch")
        if not success:
            return Response(message=f"Error: {output}", break_loop=False)
        
        # Parse status output
        lines = output.split('\n')
        branch_line = lines[0] if lines else ""
        file_lines = lines[1:] if len(lines) > 1 else []
        
        result = "## Git Status\n\n"
        result += f"**Branch:** `{branch_line.replace('## ', '')}`\n\n"
        
        if file_lines:
            staged = [l for l in file_lines if l and l[0] in 'MADRCU']
            unstaged = [l for l in file_lines if l and l[1] in 'MADRCU']
            untracked = [l for l in file_lines if l.startswith('??')]
            
            if staged:
                result += "### Staged Changes\n"
                for f in staged[:15]:
                    result += f"- `{f}`\n"
                if len(staged) > 15:
                    result += f"- ... and {len(staged) - 15} more\n"
                result += "\n"
            
            if unstaged:
                result += "### Unstaged Changes\n"
                for f in unstaged[:15]:
                    result += f"- `{f}`\n"
                result += "\n"
            
            if untracked:
                result += "### Untracked Files\n"
                for f in untracked[:10]:
                    result += f"- `{f[3:]}`\n"
                if len(untracked) > 10:
                    result += f"- ... and {len(untracked) - 10} more\n"
        else:
            result += "*Working directory clean*\n"
        
        return Response(message=result, break_loop=False)

    async def git_diff(self) -> Response:
        """Show diff of changes."""
        target = self.args.get("target", "")  # commit/branch/file
        staged = self.args.get("staged", False)
        
        cmd = ["diff"]
        if staged:
            cmd.append("--cached")
        if target:
            cmd.append(target)
        cmd.extend(["--stat", "--color=never"])
        
        success, output = self._run_git(*cmd)
        if not success:
            return Response(message=f"Error: {output}", break_loop=False)
        
        result = "## Git Diff\n\n"
        if staged:
            result += "*Showing staged changes*\n\n"
        result += f"```\n{output[:3000]}\n```\n"
        if len(output) > 3000:
            result += "\n*Output truncated...*"
        
        return Response(message=result, break_loop=False)

    async def git_log(self) -> Response:
        """Show commit history."""
        count = self.args.get("count", "10")
        oneline = self.args.get("oneline", True)
        author = self.args.get("author", "")
        
        cmd = ["log", f"-{count}"]
        if oneline:
            cmd.append("--oneline")
        else:
            cmd.append("--pretty=format:%h|%an|%ar|%s")
        if author:
            cmd.append(f"--author={author}")
        
        success, output = self._run_git(*cmd)
        if not success:
            return Response(message=f"Error: {output}", break_loop=False)
        
        result = f"## Recent Commits (last {count})\n\n"
        if oneline:
            result += "```\n" + output + "\n```"
        else:
            result += "| Hash | Author | When | Message |\n"
            result += "|------|--------|------|--------|\n"
            for line in output.split('\n')[:20]:
                parts = line.split('|')
                if len(parts) >= 4:
                    result += f"| `{parts[0]}` | {parts[1]} | {parts[2]} | {parts[3][:50]} |\n"

        return Response(message=result, break_loop=False)

    async def git_blame(self) -> Response:
        """Show who changed each line of a file."""
        file_path = self.args.get("file", "") or self.args.get("file_path", "")

        if not file_path:
            return Response(message="Please provide 'file' argument.", break_loop=False)

        success, output = self._run_git("blame", "--line-porcelain", file_path)
        if not success:
            return Response(message=f"Error: {output}", break_loop=False)

        # Parse blame output
        result = f"## Git Blame: `{file_path}`\n\n"
        result += "| Line | Author | Date | Content |\n"
        result += "|------|--------|------|--------|\n"

        lines = output.split('\n')
        line_num = 0
        current_author = ""
        current_time = ""

        for line in lines[:200]:  # Limit processing
            if line.startswith('author '):
                current_author = line[7:]
            elif line.startswith('author-time '):
                import datetime
                ts = int(line[12:])
                current_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            elif line.startswith('\t'):
                line_num += 1
                content = line[1:40] + "..." if len(line) > 41 else line[1:]
                result += f"| {line_num} | {current_author[:15]} | {current_time} | `{content}` |\n"
                if line_num >= 30:
                    result += f"| ... | ... | ... | ... |\n"
                    break

        return Response(message=result, break_loop=False)

    async def git_branch(self) -> Response:
        """List, create, or delete branches."""
        action = self.args.get("action", "list")  # list, create, delete
        name = self.args.get("name", "")

        if action == "list":
            success, output = self._run_git("branch", "-a", "-v")
            if not success:
                return Response(message=f"Error: {output}", break_loop=False)

            result = "## Git Branches\n\n```\n" + output + "\n```"
            return Response(message=result, break_loop=False)

        elif action == "create":
            if not name:
                return Response(message="Please provide 'name' for new branch.", break_loop=False)
            success, output = self._run_git("branch", name)
            msg = f"✅ Created branch `{name}`" if success else f"Error: {output}"
            return Response(message=msg, break_loop=False)

        elif action == "delete":
            if not name:
                return Response(message="Please provide 'name' to delete.", break_loop=False)
            success, output = self._run_git("branch", "-d", name)
            msg = f"✅ Deleted branch `{name}`" if success else f"Error: {output}"
            return Response(message=msg, break_loop=False)

        return Response(message=f"Unknown action: {action}", break_loop=False)

    async def git_show(self) -> Response:
        """Show details of a commit."""
        commit = self.args.get("commit", "HEAD")

        success, output = self._run_git("show", commit, "--stat", "--format=fuller")
        if not success:
            return Response(message=f"Error: {output}", break_loop=False)

        result = f"## Commit: `{commit}`\n\n```\n{output[:3000]}\n```"
        return Response(message=result, break_loop=False)

    async def git_add(self) -> Response:
        """Stage files for commit."""
        files = self.args.get("files", ".")

        if isinstance(files, str):
            files = [files]

        success, output = self._run_git("add", *files)
        if not success:
            return Response(message=f"Error: {output}", break_loop=False)

        return Response(message=f"✅ Staged: {', '.join(files)}", break_loop=False)

    async def git_commit(self) -> Response:
        """Create a commit."""
        message = self.args.get("message", "")
        add_all = self.args.get("add_all", False)

        if not message:
            return Response(message="Please provide 'message' for commit.", break_loop=False)

        if add_all:
            self._run_git("add", "-A")

        success, output = self._run_git("commit", "-m", message)
        if not success:
            return Response(message=f"Error: {output}", break_loop=False)

        return Response(message=f"✅ Committed: {message}\n\n```\n{output}\n```", break_loop=False)

    async def git_stash(self) -> Response:
        """Stash or unstash changes."""
        action = self.args.get("action", "push")  # push, pop, list

        if action == "push":
            msg = self.args.get("message", "")
            cmd = ["stash", "push"]
            if msg:
                cmd.extend(["-m", msg])
            success, output = self._run_git(*cmd)
        elif action == "pop":
            success, output = self._run_git("stash", "pop")
        elif action == "list":
            success, output = self._run_git("stash", "list")
        else:
            return Response(message=f"Unknown action: {action}", break_loop=False)

        if not success:
            return Response(message=f"Error: {output}", break_loop=False)

        return Response(message=f"## Stash {action}\n\n```\n{output}\n```", break_loop=False)

    async def git_checkout(self) -> Response:
        """Checkout branch or files."""
        target = self.args.get("target", "") or self.args.get("branch", "")
        create = self.args.get("create", False)

        if not target:
            return Response(message="Please provide 'target' (branch or file).", break_loop=False)

        cmd = ["checkout"]
        if create:
            cmd.append("-b")
        cmd.append(target)

        success, output = self._run_git(*cmd)
        msg = f"✅ Checked out `{target}`" if success else f"Error: {output}"
        return Response(message=msg, break_loop=False)

    async def git_merge(self) -> Response:
        """Merge a branch."""
        branch = self.args.get("branch", "")

        if not branch:
            return Response(message="Please provide 'branch' to merge.", break_loop=False)

        success, output = self._run_git("merge", branch)
        if not success:
            return Response(message=f"Merge failed:\n```\n{output}\n```", break_loop=False)

        return Response(message=f"✅ Merged `{branch}`\n\n```\n{output}\n```", break_loop=False)

    async def git_pull(self) -> Response:
        """Pull from remote."""
        remote = self.args.get("remote", "origin")
        branch = self.args.get("branch", "")

        cmd = ["pull", remote]
        if branch:
            cmd.append(branch)

        success, output = self._run_git(*cmd)
        if not success:
            return Response(message=f"Pull failed:\n```\n{output}\n```", break_loop=False)

        return Response(message=f"✅ Pulled from `{remote}`\n\n```\n{output}\n```", break_loop=False)

    async def git_push(self) -> Response:
        """Push to remote."""
        remote = self.args.get("remote", "origin")
        branch = self.args.get("branch", "")
        set_upstream = self.args.get("set_upstream", False)

        cmd = ["push"]
        if set_upstream:
            cmd.append("-u")
        cmd.append(remote)
        if branch:
            cmd.append(branch)

        success, output = self._run_git(*cmd)
        if not success:
            return Response(message=f"Push failed:\n```\n{output}\n```", break_loop=False)

        return Response(message=f"✅ Pushed to `{remote}`\n\n```\n{output}\n```", break_loop=False)
