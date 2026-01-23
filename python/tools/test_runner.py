"""
Test Runner Tool for Agent Zero
Run tests and report results with detailed analysis.
"""
import subprocess
import os
import re
from python.helpers.tool import Tool, Response


class TestRunner(Tool):
    """
    Tool for running tests and analyzing results.
    
    Methods:
    - run: Run tests (pytest, unittest, or npm test)
    - coverage: Run with coverage report
    - failed: Re-run only failed tests
    - watch: Suggest watch mode command
    """

    async def execute(self, **kwargs) -> Response:
        method = self.method or self.args.get("method", "run")
        
        if method == "run":
            return await self.run_tests()
        elif method == "coverage":
            return await self.run_coverage()
        elif method == "failed":
            return await self.run_failed()
        elif method == "watch":
            return await self.suggest_watch()
        elif method == "analyze":
            return await self.analyze_output()
        else:
            return Response(
                message=f"Unknown method '{method}'. Available: run, coverage, failed, watch, analyze",
                break_loop=False
            )

    def _run_command(self, cmd: list, cwd: str = None) -> tuple[bool, str, str]:
        """Run a command and return (success, stdout, stderr)."""
        try:
            cwd = cwd or self.args.get("path", "") or os.getcwd()
            result = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=120
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Test run timed out (120s limit)"
        except Exception as e:
            return False, "", str(e)

    def _detect_test_framework(self, path: str) -> str:
        """Detect which test framework to use."""
        # Check for package.json (npm/node)
        if os.path.exists(os.path.join(path, "package.json")):
            return "npm"
        # Check for pytest.ini or conftest.py
        if os.path.exists(os.path.join(path, "pytest.ini")) or \
           os.path.exists(os.path.join(path, "conftest.py")):
            return "pytest"
        # Check for setup.py or pyproject.toml
        if os.path.exists(os.path.join(path, "setup.py")) or \
           os.path.exists(os.path.join(path, "pyproject.toml")):
            return "pytest"
        # Default to pytest for Python projects
        return "pytest"

    async def run_tests(self) -> Response:
        """Run tests in the specified directory."""
        path = self.args.get("path", "") or os.getcwd()
        target = self.args.get("target", "")  # specific test file/function
        verbose = self.args.get("verbose", True)
        framework = self.args.get("framework", "") or self._detect_test_framework(path)
        
        if framework == "pytest":
            cmd = ["python", "-m", "pytest"]
            if verbose:
                cmd.append("-v")
            if target:
                cmd.append(target)
        elif framework == "npm":
            cmd = ["npm", "test"]
            if target:
                cmd.extend(["--", target])
        elif framework == "unittest":
            cmd = ["python", "-m", "unittest"]
            if target:
                cmd.append(target)
            else:
                cmd.append("discover")
        else:
            return Response(message=f"Unknown framework: {framework}", break_loop=False)
        
        success, stdout, stderr = self._run_command(cmd, path)
        
        result = f"## Test Results ({framework})\n\n"
        
        if success:
            result += "✅ **All tests passed!**\n\n"
        else:
            result += "❌ **Some tests failed**\n\n"
        
        # Parse output for summary
        output = stdout + stderr
        result += self._parse_test_output(output, framework)
        
        return Response(message=result, break_loop=False)

    def _parse_test_output(self, output: str, framework: str) -> str:
        """Parse test output into readable summary."""
        result = ""
        
        if framework == "pytest":
            # Find summary line
            summary = re.search(r'=+ ([\d\w\s,]+) in [\d.]+s =+', output)
            if summary:
                result += f"**Summary:** {summary.group(1)}\n\n"
            
            # Find failed tests
            failures = re.findall(r'FAILED (.+?) -', output)
            if failures:
                result += "### Failed Tests\n"
                for f in failures[:10]:
                    result += f"- `{f}`\n"
                result += "\n"
            
            # Find errors
            errors = re.findall(r'ERROR (.+?)$', output, re.MULTILINE)
            if errors:
                result += "### Errors\n"
                for e in errors[:5]:
                    result += f"- `{e}`\n"
        
        # Show truncated raw output
        result += "### Output\n\n```\n"
        result += output[:2000]
        if len(output) > 2000:
            result += "\n... (truncated)"
        result += "\n```"
        
        return result

    async def run_coverage(self) -> Response:
        """Run tests with coverage reporting."""
        path = self.args.get("path", "") or os.getcwd()
        target = self.args.get("target", "")
        
        cmd = ["python", "-m", "pytest", "--cov", "--cov-report=term-missing"]
        if target:
            cmd.append(target)
        
        success, stdout, stderr = self._run_command(cmd, path)
        
        result = "## Coverage Report\n\n"
        output = stdout + stderr
        
        # Parse coverage percentage
        coverage_match = re.search(r'TOTAL\s+\d+\s+\d+\s+(\d+)%', output)
        if coverage_match:
            pct = int(coverage_match.group(1))
            emoji = "✅" if pct >= 80 else "⚠️" if pct >= 60 else "❌"
            result += f"{emoji} **Total Coverage: {pct}%**\n\n"
        
        result += "```\n" + output[:3000] + "\n```"

        return Response(message=result, break_loop=False)

    async def run_failed(self) -> Response:
        """Re-run only failed tests from last run."""
        path = self.args.get("path", "") or os.getcwd()

        cmd = ["python", "-m", "pytest", "--lf", "-v"]
        success, stdout, stderr = self._run_command(cmd, path)

        result = "## Re-running Failed Tests\n\n"
        output = stdout + stderr

        if "no previously failed tests" in output.lower():
            result += "✅ **No previously failed tests to run!**\n"
        elif success:
            result += "✅ **All previously failed tests now pass!**\n\n"
        else:
            result += "❌ **Some tests still failing**\n\n"

        result += "```\n" + output[:2000] + "\n```"

        return Response(message=result, break_loop=False)

    async def suggest_watch(self) -> Response:
        """Suggest watch mode command for continuous testing."""
        path = self.args.get("path", "") or os.getcwd()
        framework = self.args.get("framework", "") or self._detect_test_framework(path)

        result = "## Watch Mode Commands\n\n"

        if framework == "pytest":
            result += "### pytest-watch\n"
            result += "Install: `pip install pytest-watch`\n\n"
            result += "```bash\n"
            result += "# Watch all tests\n"
            result += "ptw\n\n"
            result += "# Watch specific file\n"
            result += "ptw -- tests/test_specific.py\n\n"
            result += "# Watch with verbose output\n"
            result += "ptw --runner 'pytest -v'\n"
            result += "```\n"
        elif framework == "npm":
            result += "### npm watch mode\n"
            result += "```bash\n"
            result += "npm test -- --watch\n"
            result += "```\n"

        result += "\n### Alternative: entr\n"
        result += "```bash\n"
        result += "# Watch and re-run on file changes\n"
        result += "find . -name '*.py' | entr -c pytest\n"
        result += "```"

        return Response(message=result, break_loop=False)

    async def analyze_output(self) -> Response:
        """Analyze test output to identify issues."""
        output = self.args.get("output", "")

        if not output:
            return Response(message="Please provide 'output' from test run.", break_loop=False)

        analysis = {
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "skipped": 0,
            "failures": [],
            "error_types": []
        }

        # Parse pytest output
        passed = re.search(r'(\d+) passed', output)
        if passed:
            analysis["passed"] = int(passed.group(1))

        failed = re.search(r'(\d+) failed', output)
        if failed:
            analysis["failed"] = int(failed.group(1))

        errors = re.search(r'(\d+) error', output)
        if errors:
            analysis["errors"] = int(errors.group(1))

        skipped = re.search(r'(\d+) skipped', output)
        if skipped:
            analysis["skipped"] = int(skipped.group(1))

        # Find failure details
        failures = re.findall(r'FAILED (.+?)::', output)
        analysis["failures"] = failures[:10]

        # Find common error types
        error_types = re.findall(r'(\w+Error):', output)
        analysis["error_types"] = list(set(error_types))

        result = "## Test Output Analysis\n\n"

        total = analysis["passed"] + analysis["failed"] + analysis["errors"]
        if total > 0:
            pass_rate = (analysis["passed"] / total) * 100
            result += f"**Pass Rate:** {pass_rate:.1f}% ({analysis['passed']}/{total})\n\n"

        result += "| Status | Count |\n|--------|-------|\n"
        result += f"| ✅ Passed | {analysis['passed']} |\n"
        result += f"| ❌ Failed | {analysis['failed']} |\n"
        result += f"| 💥 Errors | {analysis['errors']} |\n"
        result += f"| ⏭️ Skipped | {analysis['skipped']} |\n\n"

        if analysis["failures"]:
            result += "### Failed Tests\n"
            for f in analysis["failures"]:
                result += f"- `{f}`\n"
            result += "\n"

        if analysis["error_types"]:
            result += "### Error Types\n"
            for e in analysis["error_types"]:
                result += f"- `{e}`\n"

        return Response(message=result, break_loop=False)
