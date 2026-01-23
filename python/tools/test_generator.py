"""
Test Generator Tool for Agent Zero
Auto-generates unit tests from code analysis.
"""
import ast
import os
import re
from python.helpers.tool import Tool, Response


class TestGenerator(Tool):
    """
    Tool for generating unit tests from source code.
    
    Methods:
    - generate: Generate tests for a file or function
    - template: Get test template for a function
    - fixtures: Suggest pytest fixtures
    - coverage: Suggest tests to improve coverage
    """

    async def execute(self, **kwargs) -> Response:
        method = self.method or self.args.get("method", "generate")
        
        if method == "generate":
            return await self.generate_tests()
        elif method == "template":
            return await self.get_template()
        elif method == "fixtures":
            return await self.suggest_fixtures()
        elif method == "coverage":
            return await self.suggest_coverage()
        else:
            return Response(
                message=f"Unknown method '{method}'. Available: generate, template, fixtures, coverage",
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

    async def generate_tests(self) -> Response:
        """Generate unit tests for functions/classes in code."""
        code = self._get_code()
        if not code:
            return Response(message="Please provide 'code' or 'file_path'.", break_loop=False)
        
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return Response(message=f"Syntax error: {e}", break_loop=False)
        
        file_path = self.args.get("file_path", "module")
        module_name = os.path.basename(file_path).replace('.py', '') if file_path else "module"
        
        tests = []
        tests.append(f'"""Tests for {module_name} module."""')
        tests.append('import pytest')
        tests.append(f'from {module_name} import *')
        tests.append('')
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name.startswith('_'):
                    continue
                test = self._generate_function_test(node)
                tests.append(test)
            elif isinstance(node, ast.ClassDef):
                class_tests = self._generate_class_tests(node)
                tests.append(class_tests)
        
        result = "## Generated Unit Tests\n\n```python\n"
        result += '\n'.join(tests)
        result += "\n```\n\n"
        result += "*Note: Review and customize these tests. Add specific assertions for your use case.*"
        
        return Response(message=result, break_loop=False)

    def _generate_function_test(self, node: ast.FunctionDef) -> str:
        """Generate test for a single function."""
        func_name = node.name
        args = [arg.arg for arg in node.args.args if arg.arg != 'self']
        
        test = f'\ndef test_{func_name}():\n'
        test += f'    """Test {func_name} function."""\n'
        
        # Generate sample arguments
        if args:
            for i, arg in enumerate(args):
                test += f'    {arg} = None  # TODO: provide test value\n'
            
            call_args = ', '.join(args)
            test += f'\n    result = {func_name}({call_args})\n'
        else:
            test += f'\n    result = {func_name}()\n'
        
        test += f'\n    # TODO: Add assertions\n'
        test += f'    assert result is not None\n'
        
        return test

    def _generate_class_tests(self, node: ast.ClassDef) -> str:
        """Generate tests for a class."""
        class_name = node.name
        
        test = f'\n\nclass Test{class_name}:\n'
        test += f'    """Tests for {class_name} class."""\n\n'
        
        # Find __init__ to get constructor args
        init_args = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name == '__init__':
                init_args = [arg.arg for arg in item.args.args if arg.arg != 'self']
                break
        
        # Fixture for class instance
        test += '    @pytest.fixture\n'
        test += f'    def instance(self):\n'
        test += f'        """Create {class_name} instance for testing."""\n'
        if init_args:
            for arg in init_args:
                test += f'        {arg} = None  # TODO: provide value\n'
            args_str = ', '.join(init_args)
            test += f'        return {class_name}({args_str})\n'
        else:
            test += f'        return {class_name}()\n'
        
        # Generate test for each public method
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and not item.name.startswith('_'):
                method_name = item.name
                method_args = [a.arg for a in item.args.args if a.arg != 'self']
                
                test += f'\n    def test_{method_name}(self, instance):\n'
                test += f'        """Test {method_name} method."""\n'
                
                if method_args:
                    for arg in method_args:
                        test += f'        {arg} = None  # TODO\n'
                    args_str = ', '.join(method_args)
                    test += f'        result = instance.{method_name}({args_str})\n'
                else:
                    test += f'        result = instance.{method_name}()\n'
                
                test += f'        assert result is not None  # TODO: proper assertion\n'
        
        return test

    async def get_template(self) -> Response:
        """Get test template for a specific function."""
        func_name = self.args.get("function", "")
        if not func_name:
            return Response(message="Please provide 'function' name.", break_loop=False)
        
        template = f'''
def test_{func_name}_success():
    """Test {func_name} with valid input."""
    # Arrange
    input_value = ...  # TODO: setup
    
    # Act
    result = {func_name}(input_value)
    
    # Assert
    assert result == expected_value


def test_{func_name}_edge_case():
    """Test {func_name} with edge case."""
    result = {func_name}(None)  # or empty, zero, etc.
    assert result is not None


def test_{func_name}_error():
    """Test {func_name} raises error on invalid input."""
    with pytest.raises(ValueError):
        {func_name}(invalid_input)
'''
        
        return Response(message=f"## Test Template for `{func_name}`\n\n```python\n{template}\n```", break_loop=False)

    async def suggest_fixtures(self) -> Response:
        """Suggest pytest fixtures based on code analysis."""
        code = self._get_code()
        if not code:
            return Response(message="Please provide 'code' or 'file_path'.", break_loop=False)

        fixtures = []

        # Common patterns that suggest fixtures
        patterns = [
            (r'open\s*\([\'"]', 'tmp_file', 'Temporary file fixture'),
            (r'requests\.(get|post|put|delete)', 'mock_requests', 'Mock HTTP requests'),
            (r'sqlite3|psycopg2|pymysql', 'mock_db', 'Database mock fixture'),
            (r'os\.(environ|getenv)', 'mock_env', 'Environment variable fixture'),
            (r'datetime\.(now|today|utcnow)', 'mock_datetime', 'Mock datetime fixture'),
            (r'logging\.(info|debug|error|warning)', 'caplog', 'Capture log fixture'),
        ]

        for pattern, fixture_name, description in patterns:
            if re.search(pattern, code):
                fixtures.append((fixture_name, description))

        result = "## Suggested Pytest Fixtures\n\n"

        if not fixtures:
            result += "*No specific fixtures suggested. Consider these common ones:*\n\n"
            fixtures = [
                ('tmp_path', 'Temporary directory for file operations'),
                ('monkeypatch', 'Mock/patch objects and environment'),
                ('capsys', 'Capture stdout/stderr'),
            ]

        for name, desc in fixtures:
            result += f"### `{name}`\n{desc}\n\n"

        result += "### Example Fixtures\n\n```python\n"
        result += '''@pytest.fixture
def sample_data():
    """Provide sample test data."""
    return {"key": "value", "count": 42}


@pytest.fixture
def mock_api(monkeypatch):
    """Mock external API calls."""
    def mock_get(*args, **kwargs):
        return MockResponse({"result": "success"})
    monkeypatch.setattr("requests.get", mock_get)


@pytest.fixture
def temp_config(tmp_path):
    """Create temporary config file."""
    config_file = tmp_path / "config.json"
    config_file.write_text('{"debug": true}')
    return config_file
'''
        result += "```"

        return Response(message=result, break_loop=False)

    async def suggest_coverage(self) -> Response:
        """Suggest additional tests to improve coverage."""
        code = self._get_code()
        if not code:
            return Response(message="Please provide 'code' or 'file_path'.", break_loop=False)

        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return Response(message=f"Syntax error: {e}", break_loop=False)

        suggestions = []

        for node in ast.walk(tree):
            # Find if statements - suggest branch coverage
            if isinstance(node, ast.If):
                if isinstance(node.test, ast.Compare):
                    suggestions.append({
                        "type": "Branch Coverage",
                        "line": node.lineno,
                        "suggestion": "Test both True and False branches"
                    })

            # Find try/except - suggest error path testing
            elif isinstance(node, ast.Try):
                for handler in node.handlers:
                    exc_type = handler.type.id if isinstance(handler.type, ast.Name) else "Exception"
                    suggestions.append({
                        "type": "Error Path",
                        "line": node.lineno,
                        "suggestion": f"Test that {exc_type} is properly handled"
                    })

            # Find loops - suggest empty and single item cases
            elif isinstance(node, (ast.For, ast.While)):
                suggestions.append({
                    "type": "Loop Coverage",
                    "line": node.lineno,
                    "suggestion": "Test with empty, single item, and multiple items"
                })

            # Find functions with default args
            elif isinstance(node, ast.FunctionDef):
                defaults = node.args.defaults
                if defaults:
                    suggestions.append({
                        "type": "Default Arguments",
                        "line": node.lineno,
                        "suggestion": f"`{node.name}`: Test with and without default args"
                    })

        result = "## Coverage Improvement Suggestions\n\n"
        result += f"**Found {len(suggestions)} areas to improve coverage:**\n\n"

        for s in suggestions[:15]:
            result += f"- **{s['type']}** (line {s['line']}): {s['suggestion']}\n"

        if len(suggestions) > 15:
            result += f"\n... and {len(suggestions) - 15} more\n"

        result += "\n### General Coverage Tips\n"
        result += "- Test boundary values (0, 1, max, min)\n"
        result += "- Test null/None inputs\n"
        result += "- Test empty collections\n"
        result += "- Test error conditions\n"
        result += "- Test async edge cases\n"

        return Response(message=result, break_loop=False)
