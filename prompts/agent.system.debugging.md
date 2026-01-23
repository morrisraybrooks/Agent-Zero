## Debugging Workflow & Troubleshooting Guide

### Debugging Philosophy

Effective debugging is systematic investigation, not random guessing. Follow these principles:
- **Reproduce First**: Always reproduce the issue before attempting fixes
- **Understand Before Fixing**: Know WHY it's broken, not just WHERE
- **One Change at a Time**: Isolate variables to identify root causes
- **Verify Fixes**: Confirm the fix works and doesn't introduce new issues

### Step-by-Step Debugging Protocol

#### Phase 1: Information Gathering
1. **Collect Error Details**
   - Exact error message and stack trace
   - When does it occur? (always, sometimes, specific conditions)
   - Recent changes that might have caused it
   - Environment details (OS, language version, dependencies)

2. **Reproduce the Issue**
   ```
   - Create minimal reproduction case
   - Document exact steps to trigger
   - Note if intermittent or consistent
   ```

#### Phase 2: Error Analysis

**For Python Errors**:
```python
# Read traceback bottom-to-top
# Last line = actual error
# Work up to find your code vs library code
# Focus on the transition point
```

**For JavaScript Errors**:
```javascript
// Check console for full stack trace
// Look for 'at' lines pointing to your code
// Check async boundaries (Promise rejections)
```

**Common Error Categories**:
| Category | Symptoms | First Steps |
|----------|----------|-------------|
| Syntax | Won't parse/run | Check line numbers, brackets, quotes |
| Type | Type mismatch | Log variable types, check conversions |
| Reference | Undefined/null | Check variable scope, initialization |
| Logic | Wrong output | Add logging, trace data flow |
| Runtime | Crashes during execution | Check resource limits, inputs |
| Async | Race conditions | Add await, check Promise chains |

#### Phase 3: Hypothesis Formation

1. **Form a Theory**: Based on error analysis, hypothesize the cause
2. **Predict Behavior**: If your theory is correct, what else should happen?
3. **Test Prediction**: Verify your prediction before fixing

#### Phase 4: Debugging Techniques

**Print/Log Debugging**:
```python
# Strategic logging points
print(f"[DEBUG] Variable x = {x}, type = {type(x)}")
print(f"[DEBUG] Entering function with args: {args}")
print(f"[DEBUG] Loop iteration {i}, state = {state}")
```

**Binary Search Debugging**:
- Comment out half the code
- Does error persist?
- Narrow down by halves until isolated

**Rubber Duck Debugging**:
- Explain the code line-by-line
- The act of explanation often reveals bugs

**Diff Debugging**:
- Compare working vs broken versions
- What changed? Focus investigation there

#### Phase 5: Fix Implementation

1. **Minimal Fix**: Apply smallest change that fixes the issue
2. **Understand Impact**: Consider side effects of your fix
3. **Add Guards**: Prevent similar issues with validation/checks
4. **Document**: Comment on why the fix was needed

#### Phase 6: Verification

1. **Test the Fix**: Confirm original issue is resolved
2. **Regression Test**: Ensure nothing else broke
3. **Edge Cases**: Test boundary conditions
4. **Clean Up**: Remove debug statements, temporary code

### Error-Specific Strategies

#### Stack Overflow / Recursion
- Check base case conditions
- Verify recursion is progressing toward base case
- Consider iterative alternative

#### Memory Issues
- Look for memory leaks (unclosed resources)
- Check for accumulating data structures
- Profile memory usage over time

#### Performance Problems
- Profile to find hotspots
- Check algorithm complexity
- Look for N+1 queries, unnecessary loops

#### Async/Concurrency Bugs
- Add synchronization/locks
- Check for race conditions
- Verify async/await usage

#### Import/Module Errors
- Check file paths and names
- Verify package installation
- Check circular imports

### Debugging Commands Reference

**Python**:
```bash
python -m pdb script.py          # Start debugger
python -c "import sys; print(sys.path)"  # Check module path
pip show package_name            # Package info
```

**Node.js**:
```bash
node --inspect script.js         # Enable debugger
npm ls                           # List dependencies
node -e "console.log(process.env)"  # Check environment
```

**System**:
```bash
strace -f command                # Trace system calls
lsof -p PID                      # Open files
netstat -tlnp                    # Network connections
```

### When to Escalate

Consider asking for help or searching when:
- Same error after 3 different fix attempts
- Error message is completely unfamiliar
- Issue involves unfamiliar technology
- Time spent exceeds value of manual solution

