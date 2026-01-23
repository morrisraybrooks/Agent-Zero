"""
Code Complexity Analyzer for Agent Zero
Measures cyclomatic complexity, detects code smells, and provides quality metrics.
"""
import ast
import re
import os
from python.helpers.tool import Tool, Response


class CodeComplexity(Tool):
    """
    Tool for analyzing code complexity and detecting code smells.
    
    Methods:
    - analyze: Full complexity analysis
    - cyclomatic: Calculate cyclomatic complexity
    - smells: Detect common code smells
    - metrics: Get code metrics (lines, functions, classes)
    """

    async def execute(self, **kwargs) -> Response:
        method = self.method or self.args.get("method", "analyze")
        
        if method == "analyze":
            return await self.full_analysis()
        elif method == "cyclomatic":
            return await self.cyclomatic_complexity()
        elif method == "smells":
            return await self.detect_smells()
        elif method == "metrics":
            return await self.code_metrics()
        else:
            return Response(
                message=f"Unknown method '{method}'. Available: analyze, cyclomatic, smells, metrics",
                break_loop=False
            )

    def _get_code(self) -> str:
        """Get code from args."""
        code = self.args.get("code", "")
        file_path = self.args.get("file_path", "")
        
        if file_path and os.path.exists(file_path):
            with open(file_path, 'r') as f:
                code = f.read()
        return code

    async def full_analysis(self) -> Response:
        """Perform full code complexity analysis."""
        code = self._get_code()
        if not code:
            return Response(message="Please provide 'code' or 'file_path' argument.", break_loop=False)
        
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return Response(message=f"Syntax error: {e}", break_loop=False)
        
        # Gather all metrics
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                complexity = self._calculate_complexity(node)
                lines = (node.end_lineno or node.lineno) - node.lineno + 1
                functions.append({
                    "name": node.name,
                    "complexity": complexity,
                    "lines": lines,
                    "args": len(node.args.args),
                    "line": node.lineno
                })
        
        # Code smells
        smells = self._find_smells(code, tree)
        
        # Build result
        result = "## Code Complexity Analysis\n\n"
        
        # Overall metrics
        lines = code.count('\n') + 1
        result += f"**Total Lines:** {lines}\n"
        result += f"**Functions/Methods:** {len(functions)}\n"
        
        if functions:
            avg_complexity = sum(f["complexity"] for f in functions) / len(functions)
            max_complexity = max(f["complexity"] for f in functions)
            result += f"**Average Complexity:** {avg_complexity:.1f}\n"
            result += f"**Max Complexity:** {max_complexity}\n\n"
            
            # Function details
            result += "### Function Complexity\n\n"
            result += "| Function | Complexity | Lines | Rating |\n"
            result += "|----------|------------|-------|--------|\n"
            for f in sorted(functions, key=lambda x: -x["complexity"]):
                rating = self._complexity_rating(f["complexity"])
                result += f"| `{f['name']}` | {f['complexity']} | {f['lines']} | {rating} |\n"
        
        # Code smells
        if smells:
            result += f"\n### Code Smells Detected ({len(smells)})\n\n"
            for smell in smells[:10]:
                result += f"- **{smell['type']}** (line {smell['line']}): {smell['message']}\n"
            if len(smells) > 10:
                result += f"- ... and {len(smells) - 10} more\n"
        
        return Response(message=result, break_loop=False)

    def _calculate_complexity(self, node) -> int:
        """Calculate cyclomatic complexity for a function."""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            # Decision points add complexity
            if isinstance(child, (ast.If, ast.While, ast.For)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, ast.Assert):
                complexity += 1
            elif isinstance(child, ast.comprehension):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                # Each 'and' or 'or' adds complexity
                complexity += len(child.values) - 1
            elif isinstance(child, ast.IfExp):  # Ternary
                complexity += 1
        
        return complexity

    def _complexity_rating(self, complexity: int) -> str:
        """Rate complexity level."""
        if complexity <= 5:
            return "✅ Simple"
        elif complexity <= 10:
            return "⚠️ Moderate"
        elif complexity <= 20:
            return "🔶 Complex"
        else:
            return "🔴 Very Complex"

    def _find_smells(self, code: str, tree) -> list:
        """Detect common code smells."""
        smells = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Long lines
            if len(line) > 120:
                smells.append({"type": "Long Line", "line": i, "message": f"Line has {len(line)} chars (>120)"})
            
            # TODO/FIXME comments
            if re.search(r'#\s*(TODO|FIXME|XXX|HACK)', line, re.I):
                smells.append({"type": "TODO Comment", "line": i, "message": "Unresolved TODO/FIXME"})
            
            # Magic numbers (not 0, 1, -1)
            if re.search(r'[^a-zA-Z0-9_]([2-9]|[1-9]\d+)[^a-zA-Z0-9_.]', line):
                if not re.search(r'(range|sleep|timeout|port|year|month|day|hour)', line, re.I):
                    smells.append({"type": "Magic Number", "line": i, "message": "Consider using named constant"})

        # AST-based smells
        for node in ast.walk(tree):
            # Long functions
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_lines = (node.end_lineno or node.lineno) - node.lineno + 1
                if func_lines > 50:
                    smells.append({"type": "Long Function", "line": node.lineno,
                                  "message": f"`{node.name}` has {func_lines} lines (>50)"})

                # Too many parameters
                if len(node.args.args) > 5:
                    smells.append({"type": "Too Many Parameters", "line": node.lineno,
                                  "message": f"`{node.name}` has {len(node.args.args)} params (>5)"})

            # Deeply nested code
            if isinstance(node, ast.If):
                depth = self._get_nesting_depth(node)
                if depth > 3:
                    smells.append({"type": "Deep Nesting", "line": node.lineno,
                                  "message": f"Nesting depth is {depth} (>3)"})

        return smells

    def _get_nesting_depth(self, node, depth=1) -> int:
        """Calculate nesting depth."""
        max_depth = depth
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
                child_depth = self._get_nesting_depth(child, depth + 1)
                max_depth = max(max_depth, child_depth)
        return max_depth

    async def cyclomatic_complexity(self) -> Response:
        """Calculate cyclomatic complexity for each function."""
        code = self._get_code()
        if not code:
            return Response(message="Please provide 'code' or 'file_path' argument.", break_loop=False)

        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return Response(message=f"Syntax error: {e}", break_loop=False)

        result = "## Cyclomatic Complexity Report\n\n"
        result += "| Function | Complexity | Rating |\n"
        result += "|----------|------------|--------|\n"

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                complexity = self._calculate_complexity(node)
                rating = self._complexity_rating(complexity)
                result += f"| `{node.name}` | {complexity} | {rating} |\n"

        result += "\n### Complexity Legend\n"
        result += "- **1-5**: Simple, easy to understand\n"
        result += "- **6-10**: Moderate, consider refactoring\n"
        result += "- **11-20**: Complex, should be refactored\n"
        result += "- **21+**: Very complex, must be refactored\n"

        return Response(message=result, break_loop=False)

    async def detect_smells(self) -> Response:
        """Detect code smells only."""
        code = self._get_code()
        if not code:
            return Response(message="Please provide 'code' or 'file_path' argument.", break_loop=False)

        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return Response(message=f"Syntax error: {e}", break_loop=False)

        smells = self._find_smells(code, tree)

        if not smells:
            return Response(message="✅ No code smells detected! Code looks clean.", break_loop=False)

        result = f"## Code Smells Report\n\n**Found {len(smells)} potential issues:**\n\n"

        # Group by type
        by_type = {}
        for smell in smells:
            t = smell["type"]
            if t not in by_type:
                by_type[t] = []
            by_type[t].append(smell)

        for smell_type, items in by_type.items():
            result += f"### {smell_type} ({len(items)})\n"
            for item in items[:5]:
                result += f"- Line {item['line']}: {item['message']}\n"
            if len(items) > 5:
                result += f"- ... and {len(items) - 5} more\n"
            result += "\n"

        return Response(message=result, break_loop=False)

    async def code_metrics(self) -> Response:
        """Get general code metrics."""
        code = self._get_code()
        if not code:
            return Response(message="Please provide 'code' or 'file_path' argument.", break_loop=False)

        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return Response(message=f"Syntax error: {e}", break_loop=False)

        lines = code.split('\n')
        total_lines = len(lines)
        blank_lines = sum(1 for line in lines if not line.strip())
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        code_lines = total_lines - blank_lines - comment_lines

        functions = classes = methods = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions += 1
            elif isinstance(node, ast.ClassDef):
                classes += 1

        result = "## Code Metrics\n\n"
        result += "### Line Counts\n"
        result += f"- **Total Lines:** {total_lines}\n"
        result += f"- **Code Lines:** {code_lines}\n"
        result += f"- **Blank Lines:** {blank_lines}\n"
        result += f"- **Comment Lines:** {comment_lines}\n\n"
        result += "### Structure\n"
        result += f"- **Classes:** {classes}\n"
        result += f"- **Functions/Methods:** {functions}\n"
        result += f"- **Avg Lines per Function:** {code_lines / functions:.1f}\n" if functions else ""

        return Response(message=result, break_loop=False)

