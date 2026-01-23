"""
Debug Tool for Agent Zero
Error parsing, stack trace analysis, and fix suggestions.
"""
import re
from python.helpers.tool import Tool, Response


class DebugTool(Tool):
    """
    Tool for debugging errors and suggesting fixes.
    
    Methods:
    - parse: Parse error message
    - analyze: Analyze stack trace
    - suggest: Suggest fixes for error
    - explain: Explain error type
    - patterns: Show common error patterns
    """

    async def execute(self, **kwargs) -> Response:
        method = self.method or self.args.get("method", "parse")
        
        if method == "parse":
            return await self.parse_error()
        elif method == "analyze":
            return await self.analyze_stacktrace()
        elif method == "suggest":
            return await self.suggest_fix()
        elif method == "explain":
            return await self.explain_error()
        elif method == "patterns":
            return await self.common_patterns()
        else:
            return Response(
                message=f"Unknown method '{method}'. Available: parse, analyze, suggest, explain, patterns",
                break_loop=False
            )

    # Common error patterns and fixes
    ERROR_PATTERNS = {
        "NameError": {
            "pattern": r"NameError: name '(\w+)' is not defined",
            "cause": "Variable or function used before being defined",
            "fixes": [
                "Check spelling of the variable/function name",
                "Make sure the variable is defined before use",
                "Check if import is missing",
                "Verify scope - variable may be defined in different scope"
            ]
        },
        "TypeError": {
            "pattern": r"TypeError: (.+)",
            "cause": "Operation applied to wrong type",
            "fixes": [
                "Check argument types match function signature",
                "Add type conversion (int(), str(), etc.)",
                "Check if None is being passed unexpectedly",
                "Verify number of arguments matches"
            ]
        },
        "AttributeError": {
            "pattern": r"AttributeError: '(\w+)' object has no attribute '(\w+)'",
            "cause": "Accessing attribute that doesn't exist",
            "fixes": [
                "Check spelling of attribute name",
                "Verify object type is what you expect",
                "Check if attribute exists with hasattr()",
                "Object might be None - add null check"
            ]
        },
        "KeyError": {
            "pattern": r"KeyError: ['\"]?(\w+)['\"]?",
            "cause": "Dictionary key doesn't exist",
            "fixes": [
                "Use dict.get('key', default) instead of dict['key']",
                "Check if key exists with 'key' in dict",
                "Verify key spelling",
                "Initialize key if it should exist"
            ]
        },
        "IndexError": {
            "pattern": r"IndexError: (list|tuple|string) index out of range",
            "cause": "Accessing index beyond sequence length",
            "fixes": [
                "Check sequence length before accessing",
                "Use try/except for safe access",
                "Verify loop bounds are correct",
                "Check for off-by-one errors"
            ]
        },
        "ImportError": {
            "pattern": r"(Import|Module)Error: .*['\"](\w+)['\"]",
            "cause": "Cannot import module or name",
            "fixes": [
                "Install missing package: pip install <package>",
                "Check spelling of module name",
                "Verify package is in PYTHONPATH",
                "Check for circular imports"
            ]
        },
        "ValueError": {
            "pattern": r"ValueError: (.+)",
            "cause": "Correct type but invalid value",
            "fixes": [
                "Validate input before processing",
                "Add input sanitization",
                "Check for empty strings/collections",
                "Verify data format matches expected"
            ]
        },
        "FileNotFoundError": {
            "pattern": r"FileNotFoundError: .* '(.+)'",
            "cause": "File or directory doesn't exist",
            "fixes": [
                "Check file path is correct",
                "Use absolute paths instead of relative",
                "Create directory if needed: os.makedirs()",
                "Check working directory: os.getcwd()"
            ]
        },
        "SyntaxError": {
            "pattern": r"SyntaxError: (.+)",
            "cause": "Invalid Python syntax",
            "fixes": [
                "Check for missing colons, brackets, quotes",
                "Verify indentation is consistent",
                "Look for invalid characters",
                "Check for Python version compatibility"
            ]
        },
        "IndentationError": {
            "pattern": r"IndentationError: (.+)",
            "cause": "Incorrect indentation",
            "fixes": [
                "Use consistent indentation (4 spaces recommended)",
                "Don't mix tabs and spaces",
                "Check IDE settings for tab width",
                "Use editor's 'fix indentation' feature"
            ]
        }
    }

    async def parse_error(self) -> Response:
        """Parse error message and identify type."""
        error = self.args.get("error", "")
        if not error:
            return Response(message="Please provide 'error' message.", break_loop=False)
        
        result = "## Error Analysis\n\n"
        
        # Identify error type
        error_type = None
        matched_info = None
        
        for err_name, info in self.ERROR_PATTERNS.items():
            if err_name in error:
                error_type = err_name
                matched_info = info
                break
        
        if error_type:
            result += f"**Error Type:** `{error_type}`\n\n"
            result += f"**Cause:** {matched_info['cause']}\n\n"
            result += "### Quick Fixes\n"
            for fix in matched_info['fixes'][:3]:
                result += f"- {fix}\n"
        else:
            result += "**Error Type:** Unknown\n\n"
            result += "*Could not identify error pattern. Provide full traceback for better analysis.*"

        return Response(message=result, break_loop=False)

    async def analyze_stacktrace(self) -> Response:
        """Analyze full stack trace."""
        traceback = self.args.get("traceback", "") or self.args.get("error", "")
        if not traceback:
            return Response(message="Please provide 'traceback' text.", break_loop=False)

        result = "## Stack Trace Analysis\n\n"

        # Extract frames
        frames = re.findall(r'File "([^"]+)", line (\d+), in (\w+)', traceback)

        if frames:
            result += "### Call Stack (most recent last)\n\n"
            result += "| # | File | Line | Function |\n"
            result += "|---|------|------|----------|\n"

            for i, (file, line, func) in enumerate(frames, 1):
                short_file = file.split('/')[-1] if '/' in file else file.split('\\')[-1]
                result += f"| {i} | `{short_file}` | {line} | `{func}` |\n"

            # Identify likely error location
            if frames:
                last_frame = frames[-1]
                result += f"\n**Most likely error location:** `{last_frame[0]}` line {last_frame[1]} in `{last_frame[2]}`\n"

        # Extract error message
        error_match = re.search(r'(\w+Error): (.+)$', traceback, re.MULTILINE)
        if error_match:
            result += f"\n### Error\n**{error_match.group(1)}:** {error_match.group(2)}\n"

            # Get fixes for this error type
            error_type = error_match.group(1)
            if error_type in self.ERROR_PATTERNS:
                result += "\n### Suggested Fixes\n"
                for fix in self.ERROR_PATTERNS[error_type]['fixes']:
                    result += f"- {fix}\n"

        return Response(message=result, break_loop=False)

    async def suggest_fix(self) -> Response:
        """Suggest specific fixes for an error."""
        error = self.args.get("error", "")
        context = self.args.get("context", "")

        if not error:
            return Response(message="Please provide 'error' message.", break_loop=False)

        result = "## Fix Suggestions\n\n"

        # Match error pattern
        for err_name, info in self.ERROR_PATTERNS.items():
            match = re.search(info['pattern'], error)
            if match:
                result += f"**Detected:** `{err_name}`\n\n"

                result += "### Possible Fixes\n\n"
                for i, fix in enumerate(info['fixes'], 1):
                    result += f"{i}. {fix}\n"

                # Add code example based on error type
                result += "\n### Code Example\n\n"
                result += self._get_fix_example(err_name)
                break
        else:
            result += "Could not match error pattern.\n\n"
            result += "### General Debugging Steps\n"
            result += "1. Read the full error message carefully\n"
            result += "2. Check the line number indicated\n"
            result += "3. Add print statements before the error\n"
            result += "4. Check variable types with type()\n"
            result += "5. Use a debugger for step-by-step execution\n"

        return Response(message=result, break_loop=False)

    def _get_fix_example(self, error_type: str) -> str:
        """Get code example for fixing error type."""
        examples = {
            "KeyError": """```python
# Instead of:
value = my_dict['key']

# Use safe access:
value = my_dict.get('key', 'default')

# Or check first:
if 'key' in my_dict:
    value = my_dict['key']
```""",
            "AttributeError": """```python
# Check attribute exists:
if hasattr(obj, 'attribute'):
    value = obj.attribute

# Or handle None:
if obj is not None:
    value = obj.attribute
```""",
            "TypeError": """```python
# Check and convert types:
if isinstance(value, str):
    value = int(value)

# Handle None:
if value is not None:
    result = process(value)
```""",
            "IndexError": """```python
# Check length first:
if index < len(my_list):
    value = my_list[index]

# Or use try/except:
try:
    value = my_list[index]
except IndexError:
    value = None
```""",
            "FileNotFoundError": """```python
from pathlib import Path

# Check file exists:
path = Path('file.txt')
if path.exists():
    content = path.read_text()

# Create directories:
path.parent.mkdir(parents=True, exist_ok=True)
```"""
        }
        return examples.get(error_type, "```python\n# Add error handling\ntry:\n    # your code\nexcept Exception as e:\n    print(f'Error: {e}')\n```")

    async def explain_error(self) -> Response:
        """Explain what an error type means."""
        error_type = self.args.get("type", "")

        if not error_type:
            return Response(message="Please provide 'type' of error to explain.", break_loop=False)

        explanations = {
            "NameError": "Raised when a variable or function name is not found in local or global scope.",
            "TypeError": "Raised when an operation is applied to an object of inappropriate type.",
            "ValueError": "Raised when a function receives an argument of correct type but inappropriate value.",
            "AttributeError": "Raised when an attribute reference or assignment fails.",
            "KeyError": "Raised when a dictionary key is not found.",
            "IndexError": "Raised when a sequence index is out of range.",
            "ImportError": "Raised when an import statement fails to find a module.",
            "ModuleNotFoundError": "Raised when a module cannot be located (subclass of ImportError).",
            "FileNotFoundError": "Raised when trying to open a file that doesn't exist.",
            "SyntaxError": "Raised when the parser encounters a syntax error.",
            "IndentationError": "Raised when indentation is not correct.",
            "RuntimeError": "Raised when an error doesn't fit any other category.",
            "RecursionError": "Raised when maximum recursion depth is exceeded.",
            "MemoryError": "Raised when an operation runs out of memory.",
            "ZeroDivisionError": "Raised when dividing by zero.",
            "StopIteration": "Raised by next() when iterator is exhausted.",
            "AssertionError": "Raised when an assert statement fails.",
            "ConnectionError": "Raised for connection-related issues.",
            "TimeoutError": "Raised when an operation times out.",
        }

        result = f"## {error_type} Explained\n\n"

        if error_type in explanations:
            result += f"**Definition:** {explanations[error_type]}\n\n"

            if error_type in self.ERROR_PATTERNS:
                result += f"**Common Cause:** {self.ERROR_PATTERNS[error_type]['cause']}\n\n"
                result += "### How to Fix\n"
                for fix in self.ERROR_PATTERNS[error_type]['fixes']:
                    result += f"- {fix}\n"
        else:
            result += f"*{error_type} is not in the knowledge base.*\n"

        return Response(message=result, break_loop=False)

    async def common_patterns(self) -> Response:
        """Show common error patterns and solutions."""
        language = self.args.get("language", "python")

        result = "## Common Error Patterns\n\n"

        if language == "python":
            result += "### Python Errors\n\n"
            result += "| Error | Quick Fix |\n"
            result += "|-------|-----------|\n"
            result += "| `NameError` | Check spelling, imports, scope |\n"
            result += "| `TypeError` | Check types, add conversion |\n"
            result += "| `KeyError` | Use `.get()`, check key exists |\n"
            result += "| `AttributeError` | Check for None, use hasattr() |\n"
            result += "| `IndexError` | Check length before access |\n"
            result += "| `ValueError` | Validate input data |\n"
            result += "| `FileNotFoundError` | Check path, use absolute paths |\n"
            result += "| `ImportError` | pip install, check spelling |\n\n"

            result += "### Debugging Tips\n"
            result += "1. **Print debugging:** Add `print(type(x), x)` before error\n"
            result += "2. **Use pdb:** `import pdb; pdb.set_trace()`\n"
            result += "3. **Check types:** `isinstance(x, expected_type)`\n"
            result += "4. **Try/except:** Wrap risky code in try block\n"

        return Response(message=result, break_loop=False)
