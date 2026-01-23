## Programming Paradigms Guide

### Object-Oriented Programming (OOP)

#### Core Principles

**Encapsulation**: Bundle data and methods that operate on that data
```python
class BankAccount:
    def __init__(self, balance=0):
        self._balance = balance  # Private by convention
    
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
    
    def get_balance(self):
        return self._balance
```

**Inheritance**: Create new classes based on existing ones
```python
class SavingsAccount(BankAccount):
    def __init__(self, balance=0, interest_rate=0.02):
        super().__init__(balance)
        self.interest_rate = interest_rate
    
    def apply_interest(self):
        self._balance *= (1 + self.interest_rate)
```

**Polymorphism**: Objects of different types respond to same interface
```python
class PaymentProcessor:
    def process(self, payment):
        payment.execute()  # Works with any payment type

class CreditCardPayment:
    def execute(self): ...
    
class PayPalPayment:
    def execute(self): ...
```

**Abstraction**: Hide complex implementation details
```python
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def connect(self): pass
    
    @abstractmethod
    def query(self, sql): pass
```

#### SOLID Principles

| Principle | Description | Example |
|-----------|-------------|---------|
| **S**ingle Responsibility | One class, one reason to change | Separate User from UserValidator |
| **O**pen/Closed | Open for extension, closed for modification | Use interfaces for new behaviors |
| **L**iskov Substitution | Subtypes must be substitutable | Child classes honor parent contracts |
| **I**nterface Segregation | Small, specific interfaces | Split IWorker into IWorkable, IEatable |
| **D**ependency Inversion | Depend on abstractions | Inject interfaces, not concrete classes |

#### Common Design Patterns
- **Factory**: Create objects without specifying exact class
- **Singleton**: Ensure only one instance exists
- **Observer**: Notify dependents of state changes
- **Strategy**: Define family of interchangeable algorithms
- **Decorator**: Add behavior dynamically

### Functional Programming (FP)

#### Core Concepts

**Pure Functions**: Same input always produces same output, no side effects
```python
# Pure function
def add(a, b):
    return a + b

# Impure function (side effect)
total = 0
def add_to_total(n):
    global total
    total += n  # Modifies external state
```

**Immutability**: Data cannot be changed after creation
```python
# Mutable (avoid in FP)
items = [1, 2, 3]
items.append(4)

# Immutable approach
items = (1, 2, 3)
new_items = items + (4,)
```

**Higher-Order Functions**: Functions that take/return functions
```python
def apply_operation(func, data):
    return [func(x) for x in data]

doubled = apply_operation(lambda x: x * 2, [1, 2, 3])
```

**Function Composition**: Combine simple functions into complex ones
```python
def compose(*funcs):
    def composed(x):
        for f in reversed(funcs):
            x = f(x)
        return x
    return composed

add_one = lambda x: x + 1
double = lambda x: x * 2
add_one_then_double = compose(double, add_one)
```

#### Functional Patterns
```python
# Map: Transform each element
squares = list(map(lambda x: x**2, [1, 2, 3]))

# Filter: Select elements matching predicate
evens = list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4]))

# Reduce: Combine elements into single value
from functools import reduce
total = reduce(lambda a, b: a + b, [1, 2, 3, 4])
```

### Async/Concurrent Programming

#### Concurrency vs Parallelism
- **Concurrency**: Multiple tasks making progress (not necessarily simultaneously)
- **Parallelism**: Multiple tasks executing simultaneously on multiple cores

#### Async/Await Pattern (Python)
```python
import asyncio

async def fetch_data(url):
    # Simulate async I/O
    await asyncio.sleep(1)
    return f"Data from {url}"

async def main():
    # Concurrent execution
    results = await asyncio.gather(
        fetch_data("url1"),
        fetch_data("url2"),
        fetch_data("url3")
    )
    return results

asyncio.run(main())
```

#### Threading vs Multiprocessing

| Aspect | Threading | Multiprocessing |
|--------|-----------|-----------------|
| Use case | I/O-bound tasks | CPU-bound tasks |
| Memory | Shared memory | Separate memory |
| GIL impact | Affected by GIL | Bypasses GIL |
| Overhead | Lower | Higher |
| Communication | Direct sharing | IPC required |

#### Async Best Practices
- Use async for I/O-bound operations
- Avoid blocking calls in async code
- Use asyncio.gather for concurrent operations
- Handle exceptions in async tasks
- Use proper cancellation patterns

#### Common Concurrency Patterns
```python
# Producer-Consumer
import asyncio
from asyncio import Queue

async def producer(queue):
    for i in range(5):
        await queue.put(i)
        
async def consumer(queue):
    while True:
        item = await queue.get()
        process(item)
        queue.task_done()
```

#### Avoiding Common Pitfalls
- **Race Conditions**: Use locks/mutexes for shared resources
- **Deadlocks**: Acquire locks in consistent order
- **Starvation**: Use fair scheduling algorithms
- **Memory Leaks**: Cancel tasks and close resources properly

