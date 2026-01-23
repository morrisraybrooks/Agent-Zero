## Language-Specific Guidelines

### Python Best Practices

#### Style & Conventions
```python
# Use type hints for clarity
def process_data(items: list[str], max_count: int = 10) -> dict[str, int]:
    return {item: len(item) for item in items[:max_count]}

# Use dataclasses for data containers
from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: str
    active: bool = True

# Context managers for resource handling
with open('file.txt', 'r') as f:
    content = f.read()

# List comprehensions over map/filter
squares = [x**2 for x in range(10) if x % 2 == 0]

# F-strings for formatting
name = "Alice"
message = f"Hello, {name}!"
```

#### Common Patterns
- Use `pathlib.Path` instead of `os.path`
- Use `logging` module instead of print for production
- Use virtual environments (`venv`, `conda`)
- Follow PEP 8 style guide
- Use `pytest` for testing

### JavaScript/TypeScript Best Practices

#### Modern JS Patterns
```javascript
// Use const/let, never var
const API_URL = 'https://api.example.com';
let counter = 0;

// Arrow functions for callbacks
const doubled = numbers.map(n => n * 2);

// Destructuring
const { name, email } = user;
const [first, ...rest] = items;

// Async/await over callbacks
async function fetchUser(id) {
    try {
        const response = await fetch(`/api/users/${id}`);
        return await response.json();
    } catch (error) {
        console.error('Failed to fetch:', error);
        throw error;
    }
}

// Optional chaining and nullish coalescing
const city = user?.address?.city ?? 'Unknown';
```

#### TypeScript Specifics
```typescript
// Interface for object shapes
interface User {
    id: number;
    name: string;
    email: string;
    role?: 'admin' | 'user';
}

// Generics for reusable code
function first<T>(arr: T[]): T | undefined {
    return arr[0];
}

// Type guards
function isString(value: unknown): value is string {
    return typeof value === 'string';
}
```

### Java Best Practices

#### Modern Java Patterns
```java
// Use var for local type inference (Java 10+)
var users = new ArrayList<User>();

// Records for data classes (Java 16+)
public record User(String name, String email) {}

// Stream API for collections
List<String> names = users.stream()
    .filter(u -> u.isActive())
    .map(User::getName)
    .collect(Collectors.toList());

// Optional for nullable values
Optional<User> user = findById(id);
String name = user.map(User::getName).orElse("Unknown");

// Try-with-resources
try (var reader = new BufferedReader(new FileReader(path))) {
    return reader.readLine();
}
```

#### Java Conventions
- Use `final` for immutable fields
- Prefer composition over inheritance
- Use interfaces for abstraction
- Follow package naming conventions
- Use Maven/Gradle for dependency management

### Shell/Bash Best Practices

```bash
#!/bin/bash
set -euo pipefail  # Fail fast, undefined vars error, pipe failures

# Quote variables to prevent word splitting
filename="my file.txt"
cat "$filename"

# Use arrays for multiple values
files=("file1.txt" "file2.txt" "file3.txt")
for f in "${files[@]}"; do
    echo "$f"
done

# Check command success
if command -v python3 &> /dev/null; then
    echo "Python3 is installed"
fi

# Use functions for reusable logic
log_error() {
    echo "[ERROR] $1" >&2
}

# Default values
NAME="${1:-default_name}"
```

### SQL Best Practices

```sql
-- Use meaningful aliases
SELECT u.name, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.active = TRUE
GROUP BY u.id, u.name
HAVING COUNT(o.id) > 5
ORDER BY order_count DESC;

-- Use parameterized queries (never string concat)
-- Correct: SELECT * FROM users WHERE id = ?
-- Wrong:  SELECT * FROM users WHERE id = ' + userId

-- Index frequently queried columns
CREATE INDEX idx_users_email ON users(email);

-- Use transactions for multiple operations
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

### Language Selection Guide

| Use Case | Recommended | Why |
|----------|-------------|-----|
| Quick scripts | Python, Bash | Easy syntax, fast to write |
| Web backend | Python, Node.js, Java | Strong ecosystems |
| Web frontend | JavaScript/TypeScript | Browser native |
| Data science | Python | NumPy, Pandas, ML libs |
| System programming | Rust, C, Go | Performance, control |
| Enterprise apps | Java, C# | Mature tooling, stability |
| CLI tools | Go, Rust, Python | Easy distribution |

