"""
Project Analyzer Tool for Agent Zero
Analyzes project structure, detects frameworks, and provides overview.
"""
import os
import json
from pathlib import Path
from python.helpers.tool import Tool, Response


class ProjectAnalyzer(Tool):
    """
    Tool for analyzing project structure and understanding codebases.
    
    Methods:
    - analyze: Full project analysis
    - tree: Generate file tree
    - detect: Detect framework and project type
    - stats: Get project statistics
    - find: Find files matching pattern
    """

    async def execute(self, **kwargs) -> Response:
        method = self.method or self.args.get("method", "analyze")
        
        if method == "analyze":
            return await self.analyze_project()
        elif method == "tree":
            return await self.generate_tree()
        elif method == "detect":
            return await self.detect_framework()
        elif method == "stats":
            return await self.project_stats()
        elif method == "find":
            return await self.find_files()
        else:
            return Response(
                message=f"Unknown method '{method}'. Available: analyze, tree, detect, stats, find",
                break_loop=False
            )

    def _get_path(self) -> str:
        return self.args.get("path", "") or self.args.get("directory", "") or os.getcwd()

    async def analyze_project(self) -> Response:
        """Full project analysis."""
        path = self._get_path()
        if not os.path.isdir(path):
            return Response(message=f"Invalid directory: {path}", break_loop=False)
        
        # Detect project type and framework
        project_type, framework = self._detect_project_type(path)
        
        # Get file stats
        stats = self._get_stats(path)
        
        # Get structure
        tree = self._build_tree(path, max_depth=2)
        
        result = f"## Project Analysis: `{os.path.basename(path)}`\n\n"
        result += f"**Type:** {project_type}\n"
        result += f"**Framework:** {framework}\n\n"
        
        result += "### Statistics\n"
        result += f"- **Total Files:** {stats['files']}\n"
        result += f"- **Directories:** {stats['dirs']}\n"
        result += f"- **Code Files:** {stats['code_files']}\n"
        result += f"- **Test Files:** {stats['test_files']}\n\n"
        
        result += "### Languages\n"
        for lang, count in sorted(stats['languages'].items(), key=lambda x: -x[1])[:5]:
            result += f"- **{lang}:** {count} files\n"
        
        result += "\n### Structure\n```\n"
        result += tree
        result += "\n```\n"
        
        # Key files
        result += "\n### Key Files\n"
        key_files = self._find_key_files(path)
        for name, exists in key_files.items():
            emoji = "✅" if exists else "❌"
            result += f"- {emoji} {name}\n"
        
        return Response(message=result, break_loop=False)

    def _detect_project_type(self, path: str) -> tuple[str, str]:
        """Detect project type and framework."""
        project_type = "Unknown"
        framework = "None detected"
        
        files = os.listdir(path)
        
        # Python projects
        if "pyproject.toml" in files or "setup.py" in files or "requirements.txt" in files:
            project_type = "Python"
            if "django" in str(files).lower() or os.path.exists(os.path.join(path, "manage.py")):
                framework = "Django"
            elif os.path.exists(os.path.join(path, "app.py")) or "flask" in self._check_requirements(path):
                framework = "Flask"
            elif "fastapi" in self._check_requirements(path):
                framework = "FastAPI"
        
        # JavaScript/Node projects
        elif "package.json" in files:
            project_type = "JavaScript/Node.js"
            pkg = self._read_package_json(path)
            if "react" in pkg.get("dependencies", {}):
                framework = "React"
            elif "vue" in pkg.get("dependencies", {}):
                framework = "Vue.js"
            elif "next" in pkg.get("dependencies", {}):
                framework = "Next.js"
            elif "express" in pkg.get("dependencies", {}):
                framework = "Express"
        
        # Java projects
        elif "pom.xml" in files:
            project_type = "Java"
            framework = "Maven"
        elif "build.gradle" in files:
            project_type = "Java"
            framework = "Gradle"
        
        # Go projects
        elif "go.mod" in files:
            project_type = "Go"
        
        # Rust projects
        elif "Cargo.toml" in files:
            project_type = "Rust"
        
        return project_type, framework

    def _check_requirements(self, path: str) -> str:
        """Read requirements.txt content."""
        req_file = os.path.join(path, "requirements.txt")
        if os.path.exists(req_file):
            with open(req_file, 'r') as f:
                return f.read().lower()
        return ""

    def _read_package_json(self, path: str) -> dict:
        """Read package.json."""
        pkg_file = os.path.join(path, "package.json")
        if os.path.exists(pkg_file):
            with open(pkg_file, 'r') as f:
                return json.load(f)
        return {}

    def _get_stats(self, path: str) -> dict:
        """Get project statistics."""
        stats = {"files": 0, "dirs": 0, "code_files": 0, "test_files": 0, "languages": {}}
        
        ext_lang = {
            '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
            '.java': 'Java', '.go': 'Go', '.rs': 'Rust', '.rb': 'Ruby',
            '.php': 'PHP', '.c': 'C', '.cpp': 'C++', '.cs': 'C#',
            '.html': 'HTML', '.css': 'CSS', '.md': 'Markdown'
        }
        
        for root, dirs, files in os.walk(path):
            # Skip hidden and vendor directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('node_modules', 'venv', '__pycache__', '.git')]
            stats["dirs"] += len(dirs)
            
            for f in files:
                stats["files"] += 1
                ext = os.path.splitext(f)[1].lower()
                
                if ext in ext_lang:
                    stats["code_files"] += 1
                    lang = ext_lang[ext]
                    stats["languages"][lang] = stats["languages"].get(lang, 0) + 1
                
                if 'test' in f.lower() or f.startswith('test_'):
                    stats["test_files"] += 1

        return stats

    def _build_tree(self, path: str, prefix: str = "", max_depth: int = 3, current_depth: int = 0) -> str:
        """Build a tree representation of the directory."""
        if current_depth >= max_depth:
            return ""

        tree = ""
        try:
            entries = sorted(os.listdir(path))
        except PermissionError:
            return prefix + "... (permission denied)\n"

        # Filter out hidden and ignored directories
        ignored = {'.git', '__pycache__', 'node_modules', 'venv', '.venv', '.idea', '.vscode'}
        entries = [e for e in entries if not e.startswith('.') and e not in ignored]

        dirs = [e for e in entries if os.path.isdir(os.path.join(path, e))]
        files = [e for e in entries if os.path.isfile(os.path.join(path, e))]

        # Show directories first
        for i, d in enumerate(dirs):
            is_last = (i == len(dirs) - 1) and not files
            connector = "└── " if is_last else "├── "
            tree += prefix + connector + d + "/\n"

            extension = "    " if is_last else "│   "
            subtree = self._build_tree(os.path.join(path, d), prefix + extension, max_depth, current_depth + 1)
            tree += subtree

        # Show files (limited)
        for i, f in enumerate(files[:10]):
            is_last = i == len(files[:10]) - 1
            connector = "└── " if is_last else "├── "
            tree += prefix + connector + f + "\n"

        if len(files) > 10:
            tree += prefix + "    ... and " + str(len(files) - 10) + " more files\n"

        return tree

    def _find_key_files(self, path: str) -> dict:
        """Find key configuration and documentation files."""
        key_files = {
            "README.md": False, "LICENSE": False, "Dockerfile": False,
            ".gitignore": False, "requirements.txt": False, "package.json": False,
            "pyproject.toml": False, ".env.example": False, "Makefile": False
        }

        for f in os.listdir(path):
            if f in key_files:
                key_files[f] = True
            elif f.lower() == "readme.md":
                key_files["README.md"] = True

        return key_files

    async def generate_tree(self) -> Response:
        """Generate file tree for project."""
        path = self._get_path()
        max_depth = int(self.args.get("depth", 3))

        if not os.path.isdir(path):
            return Response(message=f"Invalid directory: {path}", break_loop=False)

        tree = self._build_tree(path, max_depth=max_depth)

        result = f"## Project Tree: `{os.path.basename(path)}`\n\n```\n{tree}```"

        return Response(message=result, break_loop=False)

    async def detect_framework(self) -> Response:
        """Detect framework and project type."""
        path = self._get_path()

        project_type, framework = self._detect_project_type(path)

        result = f"## Framework Detection\n\n"
        result += f"**Project Type:** {project_type}\n"
        result += f"**Framework:** {framework}\n\n"

        # Provide recommendations
        result += "### Recommendations\n"

        if framework == "Django":
            result += "- Use `python manage.py runserver` to start dev server\n"
            result += "- Run migrations: `python manage.py migrate`\n"
            result += "- Create superuser: `python manage.py createsuperuser`\n"
        elif framework == "Flask":
            result += "- Set `FLASK_APP=app.py` environment variable\n"
            result += "- Run: `flask run` or `python app.py`\n"
        elif framework == "FastAPI":
            result += "- Run: `uvicorn main:app --reload`\n"
        elif framework == "React":
            result += "- Install: `npm install`\n"
            result += "- Start: `npm start`\n"
            result += "- Build: `npm run build`\n"
        elif framework == "Express":
            result += "- Install: `npm install`\n"
            result += "- Start: `npm start` or `node app.js`\n"

        return Response(message=result, break_loop=False)

    async def project_stats(self) -> Response:
        """Get detailed project statistics."""
        path = self._get_path()

        stats = self._get_stats(path)

        result = "## Project Statistics\n\n"
        result += f"| Metric | Count |\n|--------|-------|\n"
        result += f"| Total Files | {stats['files']} |\n"
        result += f"| Directories | {stats['dirs']} |\n"
        result += f"| Code Files | {stats['code_files']} |\n"
        result += f"| Test Files | {stats['test_files']} |\n\n"

        result += "### Language Breakdown\n"
        total_code = sum(stats['languages'].values())
        for lang, count in sorted(stats['languages'].items(), key=lambda x: -x[1]):
            pct = (count / total_code * 100) if total_code > 0 else 0
            bar = "█" * int(pct / 5)
            result += f"- **{lang}**: {count} ({pct:.1f}%) {bar}\n"

        return Response(message=result, break_loop=False)

    async def find_files(self) -> Response:
        """Find files matching a pattern."""
        path = self._get_path()
        pattern = self.args.get("pattern", "")

        if not pattern:
            return Response(message="Please provide 'pattern' argument.", break_loop=False)

        import fnmatch
        matches = []

        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('node_modules', 'venv', '__pycache__')]

            for f in files:
                if fnmatch.fnmatch(f.lower(), pattern.lower()):
                    rel_path = os.path.relpath(os.path.join(root, f), path)
                    matches.append(rel_path)

        result = f"## Files Matching `{pattern}`\n\n"
        result += f"**Found {len(matches)} files:**\n\n"

        for m in matches[:30]:
            result += f"- `{m}`\n"

        if len(matches) > 30:
            result += f"\n... and {len(matches) - 30} more\n"

        return Response(message=result, break_loop=False)
