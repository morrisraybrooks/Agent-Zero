"""
Dependency Graph Analyzer for Agent Zero
Maps imports, module relationships, and project dependencies.
"""
import ast
import os
import re
from pathlib import Path
from python.helpers.tool import Tool, Response


class DependencyGraph(Tool):
    """
    Tool for analyzing code dependencies and module relationships.
    
    Methods:
    - analyze: Analyze dependencies for a file or directory
    - imports: List all imports in a file
    - dependents: Find files that depend on a module
    - graph: Generate dependency graph visualization
    """

    async def execute(self, **kwargs) -> Response:
        method = self.method or self.args.get("method", "analyze")
        
        if method == "analyze":
            return await self.analyze_dependencies()
        elif method == "imports":
            return await self.list_imports()
        elif method == "dependents":
            return await self.find_dependents()
        elif method == "graph":
            return await self.generate_graph()
        else:
            return Response(
                message=f"Unknown method '{method}'. Available: analyze, imports, dependents, graph",
                break_loop=False
            )

    async def analyze_dependencies(self) -> Response:
        """Analyze all dependencies for a file or project."""
        path = self.args.get("path", "") or self.args.get("file_path", "")
        
        if not path or not os.path.exists(path):
            return Response(message="Please provide valid 'path' argument.", break_loop=False)
        
        if os.path.isfile(path):
            return await self._analyze_file(path)
        else:
            return await self._analyze_directory(path)

    async def _analyze_file(self, file_path: str) -> Response:
        """Analyze a single file's dependencies."""
        with open(file_path, 'r') as f:
            code = f.read()
        
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return Response(message=f"Syntax error: {e}", break_loop=False)
        
        imports = {"stdlib": [], "third_party": [], "local": []}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    category = self._categorize_import(alias.name)
                    imports[category].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    full_name = f"{module}.{alias.name}" if module else alias.name
                    category = self._categorize_import(module or alias.name)
                    imports[category].append(full_name)
        
        result = f"## Dependencies for `{os.path.basename(file_path)}`\n\n"
        
        if imports["stdlib"]:
            result += "### Standard Library\n"
            for m in sorted(set(imports["stdlib"])):
                result += f"- `{m}`\n"
            result += "\n"
        
        if imports["third_party"]:
            result += "### Third Party\n"
            for m in sorted(set(imports["third_party"])):
                result += f"- `{m}`\n"
            result += "\n"
        
        if imports["local"]:
            result += "### Local/Project\n"
            for m in sorted(set(imports["local"])):
                result += f"- `{m}`\n"
        
        total = len(set(imports["stdlib"])) + len(set(imports["third_party"])) + len(set(imports["local"]))
        result = f"**Total Dependencies:** {total}\n\n" + result
        
        return Response(message=result, break_loop=False)

    async def _analyze_directory(self, dir_path: str) -> Response:
        """Analyze dependencies across a directory."""
        all_imports = {"stdlib": set(), "third_party": set(), "local": set()}
        file_deps = {}
        
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r') as f:
                            code = f.read()
                        tree = ast.parse(code)
                        
                        file_imports = []
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    cat = self._categorize_import(alias.name)
                                    all_imports[cat].add(alias.name)
                                    file_imports.append(alias.name)
                            elif isinstance(node, ast.ImportFrom):
                                module = node.module or ""
                                cat = self._categorize_import(module)
                                all_imports[cat].add(module)
                                file_imports.append(module)
                        
                        rel_path = os.path.relpath(file_path, dir_path)
                        file_deps[rel_path] = file_imports
                    except:
                        pass
        
        result = f"## Project Dependency Analysis\n\n"
        result += f"**Files Analyzed:** {len(file_deps)}\n"
        result += f"**Standard Library:** {len(all_imports['stdlib'])}\n"
        result += f"**Third Party:** {len(all_imports['third_party'])}\n"
        result += f"**Local Modules:** {len(all_imports['local'])}\n\n"
        
        if all_imports["third_party"]:
            result += "### Third Party Dependencies\n"
            for m in sorted(all_imports["third_party"]):
                result += f"- `{m}`\n"
            result += "\n"
        
        # Most connected files
        result += "### Files with Most Dependencies\n"
        sorted_files = sorted(file_deps.items(), key=lambda x: -len(x[1]))[:10]
        for path, deps in sorted_files:
            result += f"- `{path}`: {len(deps)} imports\n"

        return Response(message=result, break_loop=False)

    def _categorize_import(self, module: str) -> str:
        """Categorize an import as stdlib, third_party, or local."""
        stdlib_modules = {
            'os', 'sys', 'json', 're', 'ast', 'typing', 'collections', 'functools',
            'itertools', 'pathlib', 'subprocess', 'threading', 'asyncio', 'datetime',
            'logging', 'unittest', 'dataclasses', 'abc', 'copy', 'io', 'time', 'random',
            'math', 'string', 'enum', 'contextlib', 'shutil', 'tempfile', 'pickle',
            'hashlib', 'base64', 'uuid', 'socket', 'http', 'urllib', 'email', 'html',
            'xml', 'csv', 'sqlite3', 'queue', 'multiprocessing', 'concurrent', 'traceback'
        }

        root = module.split('.')[0]
        if root in stdlib_modules:
            return "stdlib"
        elif module.startswith('.') or module.startswith('python.'):
            return "local"
        else:
            return "third_party"

    async def list_imports(self) -> Response:
        """List all imports in a file with details."""
        file_path = self.args.get("file_path", "") or self.args.get("path", "")

        if not file_path or not os.path.exists(file_path):
            return Response(message="Please provide valid 'file_path' argument.", break_loop=False)

        with open(file_path, 'r') as f:
            code = f.read()

        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return Response(message=f"Syntax error: {e}", break_loop=False)

        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        "module": alias.name,
                        "alias": alias.asname,
                        "type": "import",
                        "line": node.lineno
                    })
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imports.append({
                        "module": node.module or "",
                        "name": alias.name,
                        "alias": alias.asname,
                        "type": "from",
                        "line": node.lineno
                    })

        result = f"## Imports in `{os.path.basename(file_path)}`\n\n"
        result += f"**Total Import Statements:** {len(imports)}\n\n"
        result += "| Line | Type | Module | Name | Alias |\n"
        result += "|------|------|--------|------|-------|\n"

        for imp in sorted(imports, key=lambda x: x["line"]):
            alias = imp.get("alias") or "-"
            if imp["type"] == "import":
                result += f"| {imp['line']} | import | `{imp['module']}` | - | {alias} |\n"
            else:
                result += f"| {imp['line']} | from | `{imp['module']}` | `{imp.get('name', '')}` | {alias} |\n"

        return Response(message=result, break_loop=False)

    async def find_dependents(self) -> Response:
        """Find files that depend on a given module."""
        module_name = self.args.get("module", "")
        search_dir = self.args.get("directory", "") or self.args.get("path", ".")

        if not module_name:
            return Response(message="Please provide 'module' argument.", break_loop=False)

        dependents = []

        for root, _, files in os.walk(search_dir):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r') as f:
                            code = f.read()

                        # Check if module is imported
                        if re.search(rf'\b{re.escape(module_name)}\b', code):
                            tree = ast.parse(code)
                            for node in ast.walk(tree):
                                if isinstance(node, ast.Import):
                                    for alias in node.names:
                                        if module_name in alias.name:
                                            dependents.append({
                                                "file": os.path.relpath(file_path, search_dir),
                                                "line": node.lineno
                                            })
                                elif isinstance(node, ast.ImportFrom):
                                    if node.module and module_name in node.module:
                                        dependents.append({
                                            "file": os.path.relpath(file_path, search_dir),
                                            "line": node.lineno
                                        })
                    except:
                        pass

        if not dependents:
            return Response(message=f"No files found that import `{module_name}`.", break_loop=False)

        result = f"## Files Depending on `{module_name}`\n\n"
        result += f"**Found {len(dependents)} references:**\n\n"

        for dep in dependents:
            result += f"- `{dep['file']}` (line {dep['line']})\n"

        return Response(message=result, break_loop=False)

    async def generate_graph(self) -> Response:
        """Generate a text-based dependency graph."""
        path = self.args.get("path", "") or self.args.get("directory", "")

        if not path or not os.path.exists(path):
            return Response(message="Please provide valid 'path' argument.", break_loop=False)

        # Build dependency map
        deps = {}

        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, path)
                    module_name = rel_path.replace('/', '.').replace('\\', '.')[:-3]

                    try:
                        with open(file_path, 'r') as f:
                            code = f.read()
                        tree = ast.parse(code)

                        imports = []
                        for node in ast.walk(tree):
                            if isinstance(node, ast.ImportFrom):
                                if node.module and not node.module.startswith(('os', 'sys', 're', 'json')):
                                    imports.append(node.module)

                        deps[module_name] = imports
                    except:
                        pass

        result = "## Dependency Graph\n\n"
        result += "```\n"

        for module, imports in sorted(deps.items()):
            if imports:
                result += f"{module}\n"
                for imp in imports[:5]:
                    result += f"  └─> {imp}\n"
                if len(imports) > 5:
                    result += f"  └─> ... +{len(imports) - 5} more\n"

        result += "```\n"

        return Response(message=result, break_loop=False)
