"""
Code Review Tool for Agent Zero
Automated code review with quality, security, and style checks.
"""
import ast
import os
import re
from python.helpers.tool import Tool, Response


class CodeReview(Tool):
    """
    Tool for automated code review.
    
    Methods:
    - review: Full code review
    - security: Security vulnerability scan
    - style: Style and convention check
    - quality: Quality checklist review
    - checklist: Generate review checklist
    """

    async def execute(self, **kwargs) -> Response:
        method = self.method or self.args.get("method", "review")
        
        if method == "review":
            return await self.full_review()
        elif method == "security":
            return await self.security_scan()
        elif method == "style":
            return await self.style_check()
        elif method == "quality":
            return await self.quality_check()
        elif method == "checklist":
            return await self.generate_checklist()
        else:
            return Response(
                message=f"Unknown method '{method}'. Available: review, security, style, quality, checklist",
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

    async def full_review(self) -> Response:
        """Comprehensive code review."""
        code = self._get_code()
        if not code:
            return Response(message="Please provide 'code' or 'file_path'.", break_loop=False)
        
        issues = []
        
        # Security issues
        security_issues = self._check_security(code)
        issues.extend([("🔐 Security", i) for i in security_issues])
        
        # Style issues
        style_issues = self._check_style(code)
        issues.extend([("📝 Style", i) for i in style_issues])
        
        # Quality issues
        quality_issues = self._check_quality(code)
        issues.extend([("⚡ Quality", i) for i in quality_issues])
        
        result = "## Code Review Report\n\n"
        
        if not issues:
            result += "✅ **No issues found!** Code looks good.\n"
        else:
            result += f"**Found {len(issues)} issues:**\n\n"
            
            # Group by category
            for category in ["🔐 Security", "📝 Style", "⚡ Quality"]:
                cat_issues = [i for c, i in issues if c == category]
                if cat_issues:
                    result += f"### {category}\n"
                    for issue in cat_issues:
                        result += f"- {issue}\n"
                    result += "\n"
        
        # Summary metrics
        lines = code.count('\n') + 1
        result += f"\n---\n**Lines:** {lines} | **Issues:** {len(issues)}"
        
        return Response(message=result, break_loop=False)

    def _check_security(self, code: str) -> list:
        """Check for security vulnerabilities."""
        issues = []
        
        patterns = [
            (r'eval\s*\(', 'Use of `eval()` - potential code injection'),
            (r'exec\s*\(', 'Use of `exec()` - potential code injection'),
            (r'subprocess\..*shell\s*=\s*True', 'Shell=True in subprocess - command injection risk'),
            (r'os\.system\s*\(', 'Use of `os.system()` - prefer subprocess'),
            (r'password\s*=\s*["\'][^"\']+["\']', 'Hardcoded password detected'),
            (r'api_key\s*=\s*["\'][^"\']+["\']', 'Hardcoded API key detected'),
            (r'secret\s*=\s*["\'][^"\']+["\']', 'Hardcoded secret detected'),
            (r'pickle\.loads?\s*\(', 'Pickle usage - deserialization vulnerability'),
            (r'yaml\.load\s*\([^)]*\)', 'Unsafe yaml.load - use safe_load'),
            (r'__import__\s*\(', 'Dynamic import - potential security risk'),
            (r'input\s*\(\s*\)', 'Raw input() without validation'),
            (r'sql\s*=\s*[f"\'][^"\']*%|\.format\(', 'Potential SQL injection - use parameterized queries'),
        ]
        
        for pattern, message in patterns:
            if re.search(pattern, code, re.IGNORECASE):
                issues.append(message)
        
        return issues

    def _check_style(self, code: str) -> list:
        """Check style and conventions."""
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Line too long
            if len(line) > 120:
                issues.append(f"Line {i}: exceeds 120 characters ({len(line)})")
            
            # Trailing whitespace
            if line.endswith(' ') or line.endswith('\t'):
                issues.append(f"Line {i}: trailing whitespace")
            
            # TODO/FIXME/HACK comments
            if re.search(r'#\s*(TODO|FIXME|HACK|XXX)', line, re.IGNORECASE):
                issues.append(f"Line {i}: unresolved {re.search(r'(TODO|FIXME|HACK|XXX)', line, re.IGNORECASE).group()}")
        
        # Check for consistent indentation
        spaces = sum(1 for l in lines if l.startswith('    '))
        tabs = sum(1 for l in lines if l.startswith('\t'))
        if spaces > 0 and tabs > 0:
            issues.append("Mixed tabs and spaces for indentation")
        
        return issues[:10]  # Limit issues

    def _check_quality(self, code: str) -> list:
        """Check code quality."""
        issues = []
        
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return [f"Syntax error: {e}"]
        
        for node in ast.walk(tree):
            # Long functions
            if isinstance(node, ast.FunctionDef):
                func_lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0
                if func_lines > 50:
                    issues.append(f"Function `{node.name}` is {func_lines} lines - consider splitting")
                
                # Too many arguments
                if len(node.args.args) > 6:
                    issues.append(f"Function `{node.name}` has {len(node.args.args)} args - consider refactoring")
                
                # Missing docstring
                if not ast.get_docstring(node):
                    issues.append(f"Function `{node.name}` missing docstring")
            
            # Bare except
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                issues.append("Bare `except:` clause - catch specific exceptions")

        return issues[:10]

    async def security_scan(self) -> Response:
        """Focused security vulnerability scan."""
        code = self._get_code()
        if not code:
            return Response(message="Please provide 'code' or 'file_path'.", break_loop=False)

        issues = self._check_security(code)

        result = "## 🔐 Security Scan Report\n\n"

        if not issues:
            result += "✅ **No security issues detected!**\n\n"
            result += "*Note: This is a basic scan. Consider using specialized security tools for comprehensive analysis.*"
        else:
            result += f"⚠️ **Found {len(issues)} potential security issues:**\n\n"
            for issue in issues:
                result += f"- 🚨 {issue}\n"

            result += "\n### Recommendations\n"
            result += "- Review each finding and assess actual risk\n"
            result += "- Use parameterized queries for database operations\n"
            result += "- Store secrets in environment variables\n"
            result += "- Sanitize all user input\n"

        return Response(message=result, break_loop=False)

    async def style_check(self) -> Response:
        """Check style and coding conventions."""
        code = self._get_code()
        if not code:
            return Response(message="Please provide 'code' or 'file_path'.", break_loop=False)

        issues = self._check_style(code)

        result = "## 📝 Style Check Report\n\n"

        if not issues:
            result += "✅ **Code follows style conventions!**\n"
        else:
            result += f"Found {len(issues)} style issues:\n\n"
            for issue in issues:
                result += f"- {issue}\n"

        result += "\n### Style Guidelines\n"
        result += "- Keep lines under 120 characters\n"
        result += "- Use consistent indentation (4 spaces for Python)\n"
        result += "- Remove trailing whitespace\n"
        result += "- Resolve all TODO/FIXME comments before merge\n"

        return Response(message=result, break_loop=False)

    async def quality_check(self) -> Response:
        """Check code quality metrics."""
        code = self._get_code()
        if not code:
            return Response(message="Please provide 'code' or 'file_path'.", break_loop=False)

        issues = self._check_quality(code)

        result = "## ⚡ Quality Check Report\n\n"

        if not issues:
            result += "✅ **Code quality looks good!**\n"
        else:
            result += f"Found {len(issues)} quality concerns:\n\n"
            for issue in issues:
                result += f"- {issue}\n"

        result += "\n### Quality Guidelines\n"
        result += "- Keep functions under 50 lines\n"
        result += "- Limit function arguments to 5-6\n"
        result += "- Add docstrings to all public functions\n"
        result += "- Catch specific exceptions\n"
        result += "- Follow single responsibility principle\n"

        return Response(message=result, break_loop=False)

    async def generate_checklist(self) -> Response:
        """Generate a code review checklist."""
        category = self.args.get("category", "general")

        checklists = {
            "general": """## General Code Review Checklist

### Functionality
- [ ] Code accomplishes the intended task
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] No obvious bugs

### Readability
- [ ] Code is self-documenting
- [ ] Variable/function names are descriptive
- [ ] Comments explain "why" not "what"
- [ ] Consistent formatting

### Security
- [ ] No hardcoded secrets
- [ ] Input is validated
- [ ] No SQL injection risks
- [ ] Authentication/authorization checked

### Performance
- [ ] No unnecessary loops/iterations
- [ ] Database queries are optimized
- [ ] No memory leaks
- [ ] Caching used where appropriate

### Testing
- [ ] Unit tests added/updated
- [ ] Tests cover edge cases
- [ ] Tests are passing
""",
            "security": """## Security Review Checklist

### Authentication & Authorization
- [ ] Auth tokens properly validated
- [ ] Session management secure
- [ ] Password hashing (bcrypt/argon2)
- [ ] Rate limiting implemented

### Input Validation
- [ ] All user input sanitized
- [ ] SQL injection prevented
- [ ] XSS protection in place
- [ ] File upload restrictions

### Data Protection
- [ ] Sensitive data encrypted
- [ ] Secrets in environment variables
- [ ] HTTPS enforced
- [ ] PII properly handled

### Dependencies
- [ ] Dependencies up to date
- [ ] No known vulnerabilities
- [ ] Minimal dependency footprint
""",
            "pr": """## Pull Request Review Checklist

### Before Review
- [ ] PR description is clear
- [ ] Linked to issue/ticket
- [ ] Branch is up to date with main

### Code Review
- [ ] Logic is correct
- [ ] No duplicate code
- [ ] Error handling complete
- [ ] Tests included

### After Approval
- [ ] CI/CD passes
- [ ] Documentation updated
- [ ] Ready to merge
"""
        }

        checklist = checklists.get(category, checklists["general"])

        return Response(message=checklist, break_loop=False)

