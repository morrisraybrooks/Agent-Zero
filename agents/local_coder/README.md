# Local Coder - Elite Software Development Specialist

## Overview

The Local Coder is a comprehensive software development assistant combining deep technical expertise with **persistent memory across all sessions**. Specializes in full-stack development, system architecture, DevOps, and modern software engineering practices.

**🧠 Persistent Memory**: The agent remembers your entire project structure, architecture decisions, code patterns, and development context across all sessions.

## Quick Start

### Using the Local Coder

```bash
# Start Agent Zero with Local Coder profile
./start_local_coder.sh
```

Then open http://localhost:50001 and start coding!

### First-Time Project Setup

When starting with a new project, the Local Coder will:

1. **Scan your codebase** to understand structure and technology stack
2. **Save to memory** for instant recall in future sessions
3. **Learn your patterns** and coding conventions
4. **Remember architecture decisions** and their rationale

Example interaction:
```
You: "Index this codebase and remember it"

Local Coder:
✓ Scanned project structure
✓ Identified: React 18 + TypeScript + Vite frontend
✓ Identified: Node.js + Express + PostgreSQL backend
✓ Saved to persistent memory
✓ Ready to help with development!
```

## Core Capabilities

### 1. Full-Stack Development
- **Frontend**: React, Vue, Angular, Svelte, Next.js, Nuxt
- **Backend**: Node.js, Python, Go, Java, Rust, C#, Ruby, PHP
- **Databases**: PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch
- **APIs**: REST, GraphQL, gRPC, WebSockets

### 2. Software Architecture
- **Design Patterns**: Repository, Factory, Strategy, Observer, Singleton
- **Architectures**: Microservices, Event-Driven, Clean Architecture, DDD
- **Scalability**: Load balancing, caching, horizontal scaling
- **Performance**: Optimization, profiling, monitoring

### 3. DevOps & CI/CD
- **Containers**: Docker, Kubernetes, Docker Compose
- **CI/CD**: GitHub Actions, GitLab CI, Jenkins, CircleCI
- **Infrastructure**: Terraform, CloudFormation, Ansible
- **Cloud**: AWS, Azure, GCP, Vercel, Railway

### 4. Code Quality
- **Testing**: Unit, Integration, E2E (Jest, Vitest, Cypress, Playwright)
- **Linting**: ESLint, Pylint, golangci-lint
- **Type Safety**: TypeScript, Python type hints
- **Code Review**: Best practices, security, performance

### 5. Persistent Memory
- **Project Structure**: Remembers file organization and architecture
- **Architecture Decisions**: Recalls why choices were made
- **Code Patterns**: Remembers your conventions and patterns
- **Dependencies**: Tracks versions and compatibility
- **Build Config**: Remembers deployment and build settings

## Development Methodologies

The Local Coder is proficient in:

- ✅ **Agile/Scrum**: Sprint planning, user stories, iterative development
- ✅ **Test-Driven Development (TDD)**: Write tests first, then implementation
- ✅ **Domain-Driven Design (DDD)**: Model complex business domains
- ✅ **Clean Architecture**: Separation of concerns, SOLID principles
- ✅ **DevOps**: Infrastructure as Code, CI/CD, monitoring

## Persistent Memory System

### What Gets Remembered

The Local Coder maintains comprehensive knowledge across sessions:

✓ **Project Structure**
  - File organization and module hierarchy
  - Entry points and configuration files
  - Build and deployment scripts

✓ **Technology Stack**
  - Languages, frameworks, and libraries
  - Version numbers and compatibility notes
  - Package managers and dependencies

✓ **Architecture Decisions**
  - Design patterns and their rationale
  - Technology choices and trade-offs
  - Migration paths and future plans

✓ **Code Patterns**
  - Naming conventions and code style
  - Common implementations and utilities
  - API patterns and error handling

✓ **Testing Strategy**
  - Test locations and frameworks
  - Coverage goals and testing patterns
  - CI/CD configuration

✓ **Known Issues**
  - Bugs and workarounds
  - Technical debt items
  - Performance bottlenecks

### Memory Workflow Example

**First Session - Project Discovery**:
```
You: "Help me understand this codebase"

Local Coder:
1. Checks memory for existing knowledge (none found)
2. Scans directory structure
3. Identifies technology stack from package.json
4. Finds entry points and key files
5. Saves complete project map to memory
6. Provides overview of architecture
```

**Later Session - Feature Development**:
```
You: "Add a new API endpoint for user profiles"

Local Coder:
1. Loads project structure from memory
2. Recalls API pattern (Express + TypeScript)
3. Remembers controller/service/route pattern
4. Generates code following established conventions
5. Updates memory with new endpoint
```

**Future Session - Debugging**:
```
You: "Why is the build failing?"

Local Coder:
1. Recalls build configuration from memory
2. Remembers known issues with dependencies
3. Checks recent changes against saved patterns
4. Provides solution based on project context
```

### Benefits

- 🚀 **Faster Development**: No repeated discovery of project structure
- 🎯 **Consistency**: Follows your established patterns automatically
- 🔄 **Continuity**: Pick up exactly where you left off
- 📚 **Knowledge Base**: Builds expertise about your specific codebase
- 👥 **Onboarding**: Helps new team members understand the project

## Tool Proficiency (100+ Tools)

### Languages & Frameworks
JavaScript/TypeScript, Python, Go, Java, Rust, C#, Ruby, PHP, React, Vue, Angular, Node.js, Django, Flask, FastAPI, Spring Boot, .NET Core

### Databases & Storage
PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch, Cassandra, DynamoDB, Prisma, TypeORM, SQLAlchemy

### DevOps & Cloud
Docker, Kubernetes, AWS, Azure, GCP, Terraform, GitHub Actions, GitLab CI, Jenkins, Prometheus, Grafana

### Testing & Quality
Jest, Vitest, Cypress, Playwright, Selenium, ESLint, Prettier, SonarQube, Snyk

## File Structure

```
agents/local_coder/
├── _context.md                                    # Agent overview
├── README.md                                      # This file
└── prompts/
    ├── agent.system.main.role.md                 # Role definition (331 lines)
    └── agent.system.main.communication.md        # Communication style (579 lines)
```

## Example Use Cases

### 1. New Feature Development
```
You: "Implement user authentication with JWT"

Local Coder:
- Recalls project structure and patterns
- Generates auth service, middleware, routes
- Follows established TypeScript patterns
- Adds tests matching existing test structure
- Updates memory with new auth implementation
```

### 2. Code Review
```
You: "Review this component for issues"

Local Coder:
- Checks against project conventions
- Identifies performance issues
- Suggests security improvements
- Provides specific code fixes
- Explains rationale for each suggestion
```

### 3. Debugging
```
You: "API endpoint returning 500 error"

Local Coder:
- Recalls API error handling pattern
- Checks logs and stack trace
- Identifies root cause
- Provides fix with explanation
- Suggests prevention strategies
```

### 4. Architecture Planning
```
You: "How should we implement real-time notifications?"

Local Coder:
- Recalls current architecture
- Compares WebSockets vs SSE vs polling
- Considers scalability requirements
- Recommends solution with trade-offs
- Provides implementation plan
```

## Best Practices

The Local Coder follows industry best practices:

- ✅ **SOLID Principles**: Single responsibility, Open/closed, Liskov substitution, Interface segregation, Dependency inversion
- ✅ **DRY**: Don't Repeat Yourself - extract common code
- ✅ **KISS**: Keep It Simple, Stupid - avoid over-engineering
- ✅ **YAGNI**: You Aren't Gonna Need It - don't add unused features
- ✅ **Security First**: Input validation, parameterized queries, HTTPS
- ✅ **Test Coverage**: 80%+ unit test coverage target
- ✅ **Documentation**: Clear comments, README, API docs

## Getting Help

The Local Coder can help with:

- 🔧 **Implementation**: Write new features and components
- 🐛 **Debugging**: Find and fix bugs
- 📊 **Architecture**: Design scalable systems
- ⚡ **Performance**: Optimize slow code
- 🔒 **Security**: Identify and fix vulnerabilities
- 📝 **Documentation**: Write clear docs and comments
- 🧪 **Testing**: Create comprehensive test suites
- 🚀 **Deployment**: Set up CI/CD and infrastructure

## Comparison with Other Agents

| Feature | Local Coder | Hacker Agent | Writer Agent |
|---------|-------------|--------------|--------------|
| **Focus** | Software Development | Security Testing | Documentation |
| **Expertise** | Full-stack, DevOps, Architecture | Penetration Testing | Technical Writing |
| **Tools** | 100+ dev tools | 50+ security tools | Writing tools |
| **Memory** | Project structure, patterns | Vulnerabilities, credentials | Style, context |
| **Use Case** | Building software | Security assessments | Creating docs |

## License

Same as Agent Zero main project.

