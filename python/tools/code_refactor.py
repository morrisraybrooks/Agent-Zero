"""
Code Refactoring Tool for Agent Zero
Provides automated code refactoring capabilities.
"""
import ast
import re
import os
from python.helpers.tool import Tool, Response


class CodeRefactor(Tool):
    """
    Tool for automated code refactoring.
    
    Methods:
    - rename: Rename a symbol throughout code
    - extract_function: Extract code block into a function
    - inline_variable: Inline a variable's value
    - add_docstring: Add or update docstrings
    - format_code: Format code according to standards
    """

    async def execute(self, **kwargs) -> Response:
        method = self.method or self.args.get("method", "rename")
        
        if method == "rename":
            return await self.rename_symbol()
        elif method == "extract_function":
            return await self.extract_function()
        elif method == "inline_variable":
            return await self.inline_variable()
        elif method == "add_docstring":
            return await self.add_docstring()
        elif method == "format_code":
            return await self.format_code()
        elif method == "remove_unused_imports":
            return await self.remove_unused_imports()
        else:
            return Response(
                message=f"Unknown method '{method}'. Available: rename, extract_function, inline_variable, add_docstring, format_code, remove_unused_imports",
                break_loop=False
            )

    async def rename_symbol(self) -> Response:
        """Rename a symbol throughout the code."""
        code = self.args.get("code", "")
        file_path = self.args.get("file_path", "")
        old_name = self.args.get("old_name", "")
        new_name = self.args.get("new_name", "")
        
        if not old_name or not new_name:
            return Response(message="Please provide 'old_name' and 'new_name' arguments.", break_loop=False)
        
        if file_path and os.path.exists(file_path):
            with open(file_path, 'r') as f:
                code = f.read()
        
        if not code:
            return Response(message="No code provided.", break_loop=False)
        
        # Use word boundary regex to avoid partial matches
        pattern = rf'\b{re.escape(old_name)}\b'
        new_code = re.sub(pattern, new_name, code)
        
        # Count replacements
        count = len(re.findall(pattern, code))
        
        result = f"## Rename Refactoring\n\n"
        result += f"**Renamed:** `{old_name}` → `{new_name}`\n"
        result += f"**Occurrences replaced:** {count}\n\n"
        result += "### Refactored Code\n\n```python\n"
        result += new_code[:2000]
        if len(new_code) > 2000:
            result += "\n... (truncated)"
        result += "\n```"
        
        return Response(message=result, break_loop=False)

    async def extract_function(self) -> Response:
        """Extract selected code into a new function."""
        code = self.args.get("code", "")
        start_line = int(self.args.get("start_line", 0))
        end_line = int(self.args.get("end_line", 0))
        function_name = self.args.get("function_name", "extracted_function")
        
        if not code or start_line <= 0 or end_line <= 0:
            return Response(
                message="Please provide 'code', 'start_line', 'end_line', and optionally 'function_name'.",
                break_loop=False
            )
        
        lines = code.split('\n')
        if end_line > len(lines):
            end_line = len(lines)
        
        # Extract the code block
        extracted_lines = lines[start_line-1:end_line]
        extracted_code = '\n'.join(extracted_lines)
        
        # Detect indentation
        indent = ""
        for line in extracted_lines:
            if line.strip():
                indent = line[:len(line) - len(line.lstrip())]
                break
        
        # Find variables used in the extracted code
        variables = set(re.findall(r'\b([a-z_][a-z0-9_]*)\b', extracted_code.lower()))
        
        # Create the new function
        new_function = f"def {function_name}():\n"
        new_function += f'    """Extracted from lines {start_line}-{end_line}."""\n'
        for line in extracted_lines:
            # Remove one level of indentation if possible
            if line.startswith(indent):
                new_function += "    " + line[len(indent):] + "\n"
            else:
                new_function += "    " + line + "\n"
        
        # Create the replacement call
        replacement = f"{indent}{function_name}()"
        
        result = f"## Extract Function Refactoring\n\n"
        result += f"**Function name:** `{function_name}`\n"
        result += f"**Lines extracted:** {start_line}-{end_line}\n\n"
        result += "### New Function\n\n```python\n"
        result += new_function
        result += "```\n\n"
        result += "### Replacement Call\n\n```python\n"
        result += replacement
        result += "\n```\n\n"
        result += "*Note: Review parameters and return values. Adjust as needed.*"
        
        return Response(message=result, break_loop=False)

    async def inline_variable(self) -> Response:
        """Inline a variable by replacing its uses with its value."""
        code = self.args.get("code", "")
        variable = self.args.get("variable", "")
        
        if not code or not variable:
            return Response(message="Please provide 'code' and 'variable' arguments.", break_loop=False)
        
        # Find the variable assignment
        pattern = rf'^(\s*){re.escape(variable)}\s*=\s*(.+)$'
        match = re.search(pattern, code, re.MULTILINE)
        
        if not match:
            return Response(message=f"Variable '{variable}' assignment not found.", break_loop=False)
        
        value = match.group(2).strip()
        assignment_line = match.group(0)
        
        # Replace all uses except the assignment
        new_code = code.replace(assignment_line, f"# Inlined: {assignment_line}")
        new_code = re.sub(rf'\b{re.escape(variable)}\b', f'({value})', new_code)
        
        result = f"## Inline Variable Refactoring\n\n"
        result += f"**Variable:** `{variable}`\n"
        result += f"**Value:** `{value}`\n\n"
        result += "### Refactored Code\n\n```python\n"
        result += new_code[:2000]
        result += "\n```"
        
        return Response(message=result, break_loop=False)

    async def add_docstring(self) -> Response:
        """Add or suggest docstrings for functions/classes."""
        code = self.args.get("code", "")
        
        if not code:
            return Response(message="Please provide 'code' argument.", break_loop=False)
        
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return Response(message=f"Syntax error: {e}", break_loop=False)
        
        suggestions = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not ast.get_docstring(node):
                    args = [arg.arg for arg in node.args.args if arg.arg != 'self']
                    docstring = f'"""\n    Description of {node.name}.\n\n'
                    if args:
                        docstring += "    Args:\n"
                        for arg in args:
                            docstring += f"        {arg}: Description\n"
                    docstring += "\n    Returns:\n        Description\n    \"\"\""
                    suggestions.append({
                        "name": node.name,
                        "kind": "function",
                        "line": node.lineno,
                        "docstring": docstring
                    })
            elif isinstance(node, ast.ClassDef):
                if not ast.get_docstring(node):
                    docstring = f'"""Description of {node.name} class."""'
                    suggestions.append({
                        "name": node.name,
                        "kind": "class",
                        "line": node.lineno,
                        "docstring": docstring
                    })

        if not suggestions:
            return Response(message="All functions and classes already have docstrings!", break_loop=False)

        result = f"## Docstring Suggestions\n\n**Found {len(suggestions)} items missing docstrings:**\n\n"
        for s in suggestions:
            result += f"### {s['kind'].title()}: `{s['name']}` (line {s['line']})\n\n```python\n{s['docstring']}\n```\n\n"

        return Response(message=result, break_loop=False)

    async def format_code(self) -> Response:
        """Format code according to PEP 8 standards."""
        code = self.args.get("code", "")

        if not code:
            return Response(message="Please provide 'code' argument.", break_loop=False)

        formatted = code

        # Basic formatting fixes
        # 1. Normalize line endings
        formatted = formatted.replace('\r\n', '\n')

        # 2. Remove trailing whitespace
        formatted = '\n'.join(line.rstrip() for line in formatted.split('\n'))

        # 3. Ensure single blank line at end of file
        formatted = formatted.rstrip() + '\n'

        # 4. Fix spacing around operators
        formatted = re.sub(r'(\w)\s*=\s*(\w)', r'\1 = \2', formatted)
        formatted = re.sub(r'(\w)\s*==\s*(\w)', r'\1 == \2', formatted)
        formatted = re.sub(r'(\w)\s*!=\s*(\w)', r'\1 != \2', formatted)

        # 5. Fix spacing after commas
        formatted = re.sub(r',(\S)', r', \1', formatted)

        # 6. Remove multiple blank lines (keep max 2)
        formatted = re.sub(r'\n{3,}', '\n\n', formatted)

        result = "## Code Formatting\n\n"
        result += "Applied formatting fixes:\n"
        result += "- Removed trailing whitespace\n"
        result += "- Normalized line endings\n"
        result += "- Fixed operator spacing\n"
        result += "- Fixed comma spacing\n"
        result += "- Reduced excessive blank lines\n\n"
        result += "### Formatted Code\n\n```python\n"
        result += formatted[:2000]
        if len(formatted) > 2000:
            result += "\n... (truncated)"
        result += "\n```\n\n"
        result += "*Note: For complete PEP 8 formatting, use `black` or `autopep8` tools.*"

        return Response(message=result, break_loop=False)

    async def remove_unused_imports(self) -> Response:
        """Detect and remove unused imports."""
        code = self.args.get("code", "")

        if not code:
            return Response(message="Please provide 'code' argument.", break_loop=False)

        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return Response(message=f"Syntax error: {e}", break_loop=False)

        # Collect all imports
        imports = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.asname if alias.asname else alias.name
                    imports[name] = {"module": alias.name, "line": node.lineno, "type": "import"}
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    name = alias.asname if alias.asname else alias.name
                    imports[name] = {"module": f"{node.module}.{alias.name}", "line": node.lineno, "type": "from"}

        # Find all name references in the code (excluding import lines)
        code_without_imports = '\n'.join(
            line for i, line in enumerate(code.split('\n'), 1)
            if not any(imp["line"] == i for imp in imports.values())
        )

        used_names = set(re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', code_without_imports))

        # Find unused imports
        unused = []
        for name, info in imports.items():
            # Check if the name or its root (for dotted imports) is used
            if name not in used_names and name.split('.')[0] not in used_names:
                unused.append({"name": name, **info})

        if not unused:
            return Response(message="No unused imports found! All imports are being used.", break_loop=False)

        result = f"## Unused Imports Detected\n\n**Found {len(unused)} unused imports:**\n\n"
        for u in unused:
            result += f"- Line {u['line']}: `{u['name']}` (from `{u['module']}`)\n"

        result += "\n### Suggested Removal\n\nRemove these import statements:\n\n```python\n"
        for u in unused:
            if u['type'] == 'import':
                result += f"# Remove: import {u['module']}\n"
            else:
                result += f"# Remove: from ... import {u['name']}\n"
        result += "```"

        return Response(message=result, break_loop=False)
