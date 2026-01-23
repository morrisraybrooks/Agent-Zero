"""
Code Generator Tool for Agent Zero
Templates, scaffolding, and pattern generators.
"""
import os
from python.helpers.tool import Tool, Response


class CodeGenerator(Tool):
    """
    Tool for generating code from templates and patterns.
    
    Methods:
    - scaffold: Generate project scaffolding
    - template: Get code template
    - pattern: Generate design pattern implementation
    - boilerplate: Generate boilerplate code
    - api: Generate API endpoint code
    """

    async def execute(self, **kwargs) -> Response:
        method = self.method or self.args.get("method", "template")
        
        if method == "scaffold":
            return await self.scaffold_project()
        elif method == "template":
            return await self.get_template()
        elif method == "pattern":
            return await self.generate_pattern()
        elif method == "boilerplate":
            return await self.generate_boilerplate()
        elif method == "api":
            return await self.generate_api()
        else:
            return Response(
                message=f"Unknown method '{method}'. Available: scaffold, template, pattern, boilerplate, api",
                break_loop=False
            )

    async def scaffold_project(self) -> Response:
        """Generate project scaffolding."""
        project_type = self.args.get("type", "python")
        name = self.args.get("name", "my_project")
        
        scaffolds = {
            "python": f"""## Python Project Scaffold: `{name}`

```
{name}/
├── {name}/
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── requirements.txt
├── setup.py
├── README.md
├── .gitignore
└── pyproject.toml
```

### setup.py
```python
from setuptools import setup, find_packages

setup(
    name="{name}",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.8",
)
```

### pyproject.toml
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.black]
line-length = 88
```

### .gitignore
```
__pycache__/
*.pyc
.env
venv/
dist/
*.egg-info/
```
""",
            "fastapi": f"""## FastAPI Project Scaffold: `{name}`

```
{name}/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routers/
│   │   └── __init__.py
│   ├── models/
│   │   └── __init__.py
│   └── schemas/
│       └── __init__.py
├── tests/
├── requirements.txt
└── README.md
```

### app/main.py
```python
from fastapi import FastAPI

app = FastAPI(title="{name}")

@app.get("/")
async def root():
    return {{"message": "Hello World"}}

@app.get("/health")
async def health():
    return {{"status": "healthy"}}
```

### requirements.txt
```
fastapi>=0.100.0
uvicorn[standard]>=0.22.0
pydantic>=2.0.0
```
""",
            "express": f"""## Express.js Project Scaffold: `{name}`

```
{name}/
├── src/
│   ├── index.js
│   ├── routes/
│   │   └── index.js
│   ├── controllers/
│   └── middleware/
├── tests/
├── package.json
└── README.md
```

### src/index.js
```javascript
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/', (req, res) => {{
    res.json({{ message: 'Hello World' }});
}});

app.listen(PORT, () => {{
    console.log(`Server running on port ${{PORT}}`);
}});
```

### package.json
```json
{{
    "name": "{name}",
    "version": "1.0.0",
    "main": "src/index.js",
    "scripts": {{
        "start": "node src/index.js",
        "dev": "nodemon src/index.js",
        "test": "jest"
    }}
}}
```
"""
        }
        
        result = scaffolds.get(project_type, scaffolds["python"])
        return Response(message=result, break_loop=False)

    async def get_template(self) -> Response:
        """Get code template."""
        template_type = self.args.get("type", "function")
        language = self.args.get("language", "python")
        name = self.args.get("name", "my_function")
        
        templates = self._get_templates(language, name)
        template = templates.get(template_type, templates.get("function", ""))

        result = f"## {template_type.title()} Template ({language})\n\n```{language}\n{template}\n```"
        return Response(message=result, break_loop=False)

    def _get_templates(self, language: str, name: str) -> dict:
        """Get templates for a language."""
        if language == "python":
            return {
                "function": f'''def {name}(param1: str, param2: int = 0) -> str:
    """
    Description of {name}.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When invalid input
    """
    if not param1:
        raise ValueError("param1 cannot be empty")

    result = f"{{param1}}: {{param2}}"
    return result
''',
                "class": f'''class {name.title()}:
    """Description of {name.title()} class."""

    def __init__(self, value: str):
        """Initialize {name.title()}.

        Args:
            value: Initial value
        """
        self.value = value

    def process(self) -> str:
        """Process the value.

        Returns:
            Processed value
        """
        return self.value.upper()

    def __repr__(self) -> str:
        return f"{name.title()}(value={{self.value!r}})"
''',
                "async": f'''async def {name}(param: str) -> dict:
    """
    Async function {name}.

    Args:
        param: Input parameter

    Returns:
        Result dictionary
    """
    import asyncio

    # Simulate async operation
    await asyncio.sleep(0.1)

    return {{"status": "success", "param": param}}
'''
            }
        elif language in ("javascript", "js"):
            return {
                "function": f'''/**
 * Description of {name}
 * @param {{string}} param1 - First parameter
 * @param {{number}} param2 - Second parameter
 * @returns {{string}} Result
 */
function {name}(param1, param2 = 0) {{
    if (!param1) {{
        throw new Error('param1 is required');
    }}
    return `${{param1}}: ${{param2}}`;
}}
''',
                "class": f'''class {name.title()} {{
    /**
     * Create a {name.title()}
     * @param {{string}} value - Initial value
     */
    constructor(value) {{
        this.value = value;
    }}

    /**
     * Process the value
     * @returns {{string}} Processed value
     */
    process() {{
        return this.value.toUpperCase();
    }}
}}
''',
                "async": f'''/**
 * Async function {name}
 * @param {{string}} param - Input parameter
 * @returns {{Promise<Object>}} Result
 */
async function {name}(param) {{
    // Simulate async operation
    await new Promise(resolve => setTimeout(resolve, 100));

    return {{ status: 'success', param }};
}}
'''
            }
        return {"function": f"// Template for {name}"}

    async def generate_pattern(self) -> Response:
        """Generate design pattern implementation."""
        pattern = self.args.get("pattern", "singleton")
        language = self.args.get("language", "python")

        patterns = self._get_patterns(language)
        code = patterns.get(pattern.lower(), f"Pattern '{pattern}' not found.")

        result = f"## {pattern.title()} Pattern ({language})\n\n```{language}\n{code}\n```"
        return Response(message=result, break_loop=False)

    def _get_patterns(self, language: str) -> dict:
        """Get design patterns for a language."""
        if language == "python":
            return {
                "singleton": '''class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
''',
                "factory": '''from abc import ABC, abstractmethod

class Product(ABC):
    @abstractmethod
    def operation(self) -> str:
        pass

class ConcreteProductA(Product):
    def operation(self) -> str:
        return "Product A"

class ConcreteProductB(Product):
    def operation(self) -> str:
        return "Product B"

class Factory:
    @staticmethod
    def create(product_type: str) -> Product:
        if product_type == "A":
            return ConcreteProductA()
        elif product_type == "B":
            return ConcreteProductB()
        raise ValueError(f"Unknown product type: {product_type}")
''',
                "observer": '''from abc import ABC, abstractmethod
from typing import List

class Observer(ABC):
    @abstractmethod
    def update(self, message: str) -> None:
        pass

class Subject:
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, message: str) -> None:
        for observer in self._observers:
            observer.update(message)
''',
                "decorator": '''from functools import wraps
import time

def timing_decorator(func):
    """Decorator to measure execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f}s")
        return result
    return wrapper

# Usage
@timing_decorator
def slow_function():
    time.sleep(1)
    return "done"
'''
            }
        return {}

    async def generate_boilerplate(self) -> Response:
        """Generate boilerplate code."""
        boilerplate_type = self.args.get("type", "cli")

        boilerplates = {
            "cli": '''#!/usr/bin/env python3
"""Command-line interface."""
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="My CLI tool")
    parser.add_argument("input", help="Input file")
    parser.add_argument("-o", "--output", default="output.txt")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()

    if args.verbose:
        print(f"Processing {args.input}...")

    # Your logic here
    print(f"Output written to {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
''',
            "config": '''"""Configuration management."""
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    debug: bool = False
    database_url: str = ""
    api_key: Optional[str] = None

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            debug=os.getenv("DEBUG", "false").lower() == "true",
            database_url=os.getenv("DATABASE_URL", ""),
            api_key=os.getenv("API_KEY"),
        )

config = Config.from_env()
''',
            "logging": '''"""Logging configuration."""
import logging
import sys

def setup_logging(level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(getattr(logging, level.upper()))

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))
    logger.addHandler(handler)

    return logger

logger = setup_logging()
'''
        }

        code = boilerplates.get(boilerplate_type, boilerplates["cli"])
        result = f"## {boilerplate_type.title()} Boilerplate\n\n```python\n{code}\n```"
        return Response(message=result, break_loop=False)

    async def generate_api(self) -> Response:
        """Generate API endpoint code."""
        framework = self.args.get("framework", "fastapi")
        resource = self.args.get("resource", "item")

        if framework == "fastapi":
            code = f'''from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/{resource}s", tags=["{resource}s"])

class {resource.title()}(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None

# In-memory storage
{resource}s_db: List[{resource.title()}] = []

@router.get("/", response_model=List[{resource.title()}])
async def list_{resource}s():
    return {resource}s_db

@router.get("/{{id}}", response_model={resource.title()})
async def get_{resource}(id: int):
    for item in {resource}s_db:
        if item.id == id:
            return item
    raise HTTPException(status_code=404, detail="{resource.title()} not found")

@router.post("/", response_model={resource.title()})
async def create_{resource}({resource}: {resource.title()}):
    {resource}.id = len({resource}s_db) + 1
    {resource}s_db.append({resource})
    return {resource}

@router.delete("/{{id}}")
async def delete_{resource}(id: int):
    for i, item in enumerate({resource}s_db):
        if item.id == id:
            {resource}s_db.pop(i)
            return {{"message": "{resource.title()} deleted"}}
    raise HTTPException(status_code=404, detail="{resource.title()} not found")
'''
        else:
            code = f"// API template for {resource} ({framework})"

        result = f"## {resource.title()} API ({framework})\n\n```python\n{code}\n```"
        return Response(message=result, break_loop=False)
