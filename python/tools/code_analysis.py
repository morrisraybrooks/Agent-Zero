"""
Code Analysis Tool for Agent Zero
Provides AST parsing, code navigation, and analysis capabilities.
"""
import ast
import os
import re
from dataclasses import dataclass
from typing import Any
from python.helpers.tool import Tool, Response


@dataclass
class CodeSymbol:
    name: str
    kind: str  # function, class, variable, import
    line: int
    end_line: int
    docstring: str | None = None
    parent: str | None = None


class CodeAnalysis(Tool):
    """
    Tool for analyzing source code structure and content.
    
    Methods:
    - parse: Parse code and extract structure (functions, classes, imports)
    - find_definition: Find where a symbol is defined
    - find_references: Find all references to a symbol
    - get_docstring: Extract docstring for a function/class
    - analyze_imports: List all imports and dependencies
    - get_call_graph: Get function call relationships
    """

    async def execute(self, **kwargs) -> Response:
        method = self.method or self.args.get("method", "parse")
        
        if method == "parse":
            return await self.parse_code()
        elif method == "find_definition":
            return await self.find_definition()
        elif method == "find_references":
            return await self.find_references()
        elif method == "analyze_imports":
            return await self.analyze_imports()
        elif method == "get_call_graph":
            return await self.get_call_graph()
        elif method == "get_structure":
            return await self.get_structure()
        else:
            return Response(
                message=f"Unknown method '{method}'. Available: parse, find_definition, find_references, analyze_imports, get_call_graph, get_structure",
                break_loop=False
            )

    async def parse_code(self) -> Response:
        """Parse source code and return its structure."""
        code = self.args.get("code", "")
        file_path = self.args.get("file_path", "")
        language = self.args.get("language", "python")
        
        if file_path and os.path.exists(file_path):
            with open(file_path, 'r') as f:
                code = f.read()
            if not language:
                language = self._detect_language(file_path)
        
        if not code:
            return Response(message="No code provided. Use 'code' or 'file_path' argument.", break_loop=False)
        
        if language == "python":
            return self._parse_python(code)
        elif language in ["javascript", "js", "typescript", "ts"]:
            return self._parse_javascript(code)
        else:
            return Response(message=f"Language '{language}' parsing not yet supported. Supported: python, javascript", break_loop=False)

    def _detect_language(self, file_path: str) -> str:
        ext = os.path.splitext(file_path)[1].lower()
        lang_map = {
            '.py': 'python',
            '.js': 'javascript', '.jsx': 'javascript',
            '.ts': 'typescript', '.tsx': 'typescript',
            '.java': 'java',
            '.rb': 'ruby',
            '.go': 'go',
            '.rs': 'rust',
        }
        return lang_map.get(ext, 'unknown')

    def _parse_python(self, code: str) -> Response:
        """Parse Python code using AST."""
        try:
            tree = ast.parse(code)
            symbols = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    symbols.append({
                        "name": node.name,
                        "kind": "function",
                        "line": node.lineno,
                        "end_line": node.end_lineno or node.lineno,
                        "docstring": ast.get_docstring(node),
                        "args": [arg.arg for arg in node.args.args],
                        "decorators": [self._get_decorator_name(d) for d in node.decorator_list]
                    })
                elif isinstance(node, ast.AsyncFunctionDef):
                    symbols.append({
                        "name": node.name,
                        "kind": "async_function",
                        "line": node.lineno,
                        "end_line": node.end_lineno or node.lineno,
                        "docstring": ast.get_docstring(node),
                        "args": [arg.arg for arg in node.args.args]
                    })
                elif isinstance(node, ast.ClassDef):
                    symbols.append({
                        "name": node.name,
                        "kind": "class",
                        "line": node.lineno,
                        "end_line": node.end_lineno or node.lineno,
                        "docstring": ast.get_docstring(node),
                        "bases": [self._get_name(base) for base in node.bases]
                    })
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        symbols.append({
                            "name": alias.name,
                            "kind": "import",
                            "line": node.lineno,
                            "alias": alias.asname
                        })
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        symbols.append({
                            "name": f"{module}.{alias.name}",
                            "kind": "import_from",
                            "line": node.lineno,
                            "alias": alias.asname
                        })
            
            result = f"## Code Structure Analysis\n\n"
            result += f"**Total symbols found:** {len(symbols)}\n\n"
            
            # Group by kind
            funcs = [s for s in symbols if s["kind"] in ("function", "async_function")]
            classes = [s for s in symbols if s["kind"] == "class"]
            imports = [s for s in symbols if s["kind"] in ("import", "import_from")]
            
            if classes:
                result += "### Classes\n"
                for c in classes:
                    bases = f" (extends {', '.join(c.get('bases', []))})" if c.get('bases') else ""
                    result += f"- `{c['name']}`{bases} (line {c['line']})\n"
            
            if funcs:
                result += "\n### Functions\n"
                for f in funcs:
                    args = ', '.join(f.get('args', []))
                    result += f"- `{f['name']}({args})` (line {f['line']})\n"
            
            if imports:
                result += "\n### Imports\n"
                for i in imports[:20]:  # Limit imports shown
                    result += f"- `{i['name']}`\n"
                if len(imports) > 20:
                    result += f"- ... and {len(imports) - 20} more\n"
            
            return Response(message=result, break_loop=False)
            
        except SyntaxError as e:
            return Response(message=f"Syntax error in code: {e}", break_loop=False)

    def _parse_javascript(self, code: str) -> Response:
        """Parse JavaScript using regex patterns (basic parsing)."""
        symbols = []

        # Function declarations
        for match in re.finditer(r'(?:async\s+)?function\s+(\w+)\s*\([^)]*\)', code):
            line = code[:match.start()].count('\n') + 1
            symbols.append({"name": match.group(1), "kind": "function", "line": line})

        # Arrow functions assigned to const/let
        for match in re.finditer(r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>', code):
            line = code[:match.start()].count('\n') + 1
            symbols.append({"name": match.group(1), "kind": "arrow_function", "line": line})

        # Class declarations
        for match in re.finditer(r'class\s+(\w+)(?:\s+extends\s+(\w+))?\s*\{', code):
            line = code[:match.start()].count('\n') + 1
            symbols.append({"name": match.group(1), "kind": "class", "line": line, "extends": match.group(2)})

        # Imports
        for match in re.finditer(r'import\s+(?:{[^}]+}|\w+)\s+from\s+[\'"]([^\'"]+)[\'"]', code):
            line = code[:match.start()].count('\n') + 1
            symbols.append({"name": match.group(1), "kind": "import", "line": line})

        result = f"## JavaScript Code Structure\n\n**Symbols found:** {len(symbols)}\n\n"
        for s in symbols:
            result += f"- `{s['name']}` ({s['kind']}) line {s['line']}\n"

        return Response(message=result, break_loop=False)

    def _get_decorator_name(self, node) -> str:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Call):
            return self._get_name(node.func)
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return "unknown"

    def _get_name(self, node) -> str:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Subscript):
            return self._get_name(node.value)
        return "unknown"

    async def find_definition(self) -> Response:
        """Find where a symbol is defined in code."""
        code = self.args.get("code", "")
        file_path = self.args.get("file_path", "")
        symbol = self.args.get("symbol", "")

        if not symbol:
            return Response(message="Please provide 'symbol' argument.", break_loop=False)

        if file_path and os.path.exists(file_path):
            with open(file_path, 'r') as f:
                code = f.read()

        if not code:
            return Response(message="No code provided.", break_loop=False)

        try:
            tree = ast.parse(code)
            definitions = []

            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == symbol:
                    definitions.append({"kind": "function", "line": node.lineno, "end_line": node.end_lineno})
                elif isinstance(node, ast.ClassDef) and node.name == symbol:
                    definitions.append({"kind": "class", "line": node.lineno, "end_line": node.end_lineno})
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == symbol:
                            definitions.append({"kind": "variable", "line": node.lineno})

            if not definitions:
                return Response(message=f"Symbol '{symbol}' not found.", break_loop=False)

            result = f"## Definition of `{symbol}`\n\n"
            for d in definitions:
                result += f"- {d['kind']} at line {d['line']}"
                if 'end_line' in d:
                    result += f"-{d['end_line']}"
                result += "\n"

            return Response(message=result, break_loop=False)
        except Exception as e:
            return Response(message=f"Error: {e}", break_loop=False)

    async def find_references(self) -> Response:
        """Find all references to a symbol in code."""
        code = self.args.get("code", "")
        file_path = self.args.get("file_path", "")
        symbol = self.args.get("symbol", "")

        if not symbol:
            return Response(message="Please provide 'symbol' argument.", break_loop=False)

        if file_path and os.path.exists(file_path):
            with open(file_path, 'r') as f:
                code = f.read()

        references = []
        for i, line in enumerate(code.split('\n'), 1):
            if re.search(rf'\b{re.escape(symbol)}\b', line):
                references.append({"line": i, "content": line.strip()})

        result = f"## References to `{symbol}`\n\n**Found {len(references)} references:**\n\n"
        for ref in references[:30]:
            result += f"- Line {ref['line']}: `{ref['content'][:60]}...`\n" if len(ref['content']) > 60 else f"- Line {ref['line']}: `{ref['content']}`\n"

        return Response(message=result, break_loop=False)

    async def analyze_imports(self) -> Response:
        """Analyze all imports in a Python file."""
        code = self.args.get("code", "")
        file_path = self.args.get("file_path", "")

        if file_path and os.path.exists(file_path):
            with open(file_path, 'r') as f:
                code = f.read()

        try:
            tree = ast.parse(code)
            stdlib = []
            third_party = []
            local = []

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self._categorize_import(alias.name, stdlib, third_party, local)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        self._categorize_import(node.module, stdlib, third_party, local)

            result = "## Import Analysis\n\n"
            if stdlib:
                result += "### Standard Library\n" + "\n".join(f"- `{m}`" for m in set(stdlib)) + "\n\n"
            if third_party:
                result += "### Third Party\n" + "\n".join(f"- `{m}`" for m in set(third_party)) + "\n\n"
            if local:
                result += "### Local Modules\n" + "\n".join(f"- `{m}`" for m in set(local)) + "\n"

            return Response(message=result, break_loop=False)
        except Exception as e:
            return Response(message=f"Error: {e}", break_loop=False)

    def _categorize_import(self, module: str, stdlib: list, third_party: list, local: list):
        stdlib_modules = {'os', 'sys', 'json', 're', 'ast', 'typing', 'collections', 'functools',
                         'itertools', 'pathlib', 'subprocess', 'threading', 'asyncio', 'datetime',
                         'logging', 'unittest', 'dataclasses', 'abc', 'copy', 'io', 'time', 'random'}
        root = module.split('.')[0]
        if root in stdlib_modules:
            stdlib.append(module)
        elif module.startswith('.') or module.startswith('python.'):
            local.append(module)
        else:
            third_party.append(module)

    async def get_call_graph(self) -> Response:
        """Get function call relationships."""
        code = self.args.get("code", "")
        file_path = self.args.get("file_path", "")

        if file_path and os.path.exists(file_path):
            with open(file_path, 'r') as f:
                code = f.read()

        try:
            tree = ast.parse(code)
            calls = {}

            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    func_name = node.name
                    calls[func_name] = []
                    for child in ast.walk(node):
                        if isinstance(child, ast.Call):
                            called = self._get_name(child.func)
                            if called != "unknown":
                                calls[func_name].append(called)

            result = "## Call Graph\n\n"
            for func, called_funcs in calls.items():
                if called_funcs:
                    result += f"**{func}** calls:\n"
                    for c in set(called_funcs):
                        result += f"  - `{c}`\n"

            return Response(message=result, break_loop=False)
        except Exception as e:
            return Response(message=f"Error: {e}", break_loop=False)

    async def get_structure(self) -> Response:
        """Get high-level code structure overview."""
        return await self.parse_code()

