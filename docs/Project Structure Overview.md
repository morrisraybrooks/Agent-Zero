Version M v0.9.7-12 25-12-29 06:42
6:02:58 am
Jan 26, 2026
notifications

Stories
arrow_drop_down
A0: Welcome
minimize
expand
Hello! 👋, I'm Agent Zero, your AI assistant. How can I help you today?

User message person
what settings files control agent zero in bare metal
network_intelligence A0: Identifying Agent Zero bare metal configuration files
minimize
expand_all
Thoughts	
The user is asking about settings files that control Agent Zero in a bare metal (non-Docker) installation.
From the memories, I can see that Agent Zero has two main installation paths:
1. Full source installation in /home/morris/agent-zero
2. Minimal installation in /a0 directory
For bare metal, we should focus on the full source installation configuration files.
The memories mention several key configuration files and locations:
- .a0proj/config.json for project configuration
- .env file for API keys and sensitive settings
- settings.json (mentioned in warning about updates)
I should also check the standard Linux configuration locations for Agent Zero.
Since this is a development environment, I should look for both project-specific and global configuration files.
I'll provide a comprehensive list of the main configuration files and their purposes.
Headline	
Identifying Agent Zero bare metal configuration files
Tool Name	
response
Text	
## Agent Zero Bare Metal Configuration Files

Here are the main configuration files that control Agent Zero in a bare metal (non-Docker) installation:

### 1. **Project Configuration**
- **Location**: `/usr/projects/<project-name>/.a0proj/config.json`
- **Purpose**: Contains project-specific settings, paths, and Agent Zero configuration for the active project

### 2. **Environment Variables**
- **Location**: `.env` (in the installation root)
- **Purpose**: Stores API keys, secrets, and environment-specific variables
- **Important**: This file should never be committed to version control

### 3. **Global Settings**
- **Location**: `settings.json` (in the installation root)
- **Purpose**: Contains framework-wide configuration including:
  - Model providers and settings
  - Memory configuration
  - Embedding settings
  - Speech-to-text parameters

### 4. **Prompt Configuration**
- **Location**: `/prompts/<subdirectory>/` (configurable in settings)
- **Purpose**: Contains agent behavior prompts and system instructions
- **Key files**:
  - `default` directory: Standard prompts
  - Custom subdirectories: Specialized agent profiles

### 5. **Memory Configuration**
- **Location**: Configurable via settings (default subdirectory in `/memory/`)
- **Purpose**: Stores long-term memory settings and storage paths

### 6. **Knowledge Base**
- **Location**: Configurable via settings (default subdirectory in `/knowledge/`)
- **Purpose**: Contains custom knowledge files that enhance agent capabilities

### 7. **Development Environment**
- **Location**: `requirements.txt`
- **Purpose**: Lists Python dependencies for the framework
- **Note**: Must be updated when upgrading versions

### 8. **Project Instructions**
- **Location**: `/usr/projects/<project-name>/.a0proj/instructions.md`
- **Purpose**: Contains project-specific instructions that guide agent behavior

### Important Notes:
- The full source installation typically resides in `/home/morris/agent-zero/`
- Configuration files may be spread between the installation root and project directories
- Always back up `.env` and `settings.json` before updates
- Project-specific settings override global settings

Would you like me to examine any specific configuration file in more detail?
chat A0: Responding
minimize
expand
Agent Zero Bare Metal Configuration Files
Here are the main configuration files that control Agent Zero in a bare metal (non-Docker) installation:

1. Project Configuration
Location: /usr/projects/<project-name>/.a0proj/config.json
Purpose: Contains project-specific settings, paths, and Agent Zero configuration for the active project
2. Environment Variables
Location: .env (in the installation root)
Purpose: Stores API keys, secrets, and environment-specific variables
Important: This file should never be committed to version control
3. Global Settings
Location: settings.json (in the installation root)
Purpose: Contains framework-wide configuration including:
Model providers and settings
Memory configuration
Embedding settings
Speech-to-text parameters
4. Prompt Configuration
Location: /prompts/<subdirectory>/ (configurable in settings)
Purpose: Contains agent behavior prompts and system instructions
Key files:
default directory: Standard prompts
Custom subdirectories: Specialized agent profiles
5. Memory Configuration
Location: Configurable via settings (default subdirectory in /memory/)
Purpose: Stores long-term memory settings and storage paths
6. Knowledge Base
Location: Configurable via settings (default subdirectory in /knowledge/)
Purpose: Contains custom knowledge files that enhance agent capabilities
7. Development Environment
Location: requirements.txt
Purpose: Lists Python dependencies for the framework
Note: Must be updated when upgrading versions
8. Project Instructions
Location: /usr/projects/<project-name>/.a0proj/instructions.md
Purpose: Contains project-specific instructions that guide agent behavior
Important Notes:
The full source installation typically resides in /home/morris/agent-zero/
Configuration files may be spread between the installation root and project directories
Always back up .env and settings.json before updates
Project-specific settings override global settings
Would you like me to examine any specific configuration file in more detail?

User message person
lets work on the story project
network_intelligence A0: Initiating work session on the Stories project
minimize
expand_all
Thoughts	
The user wants to work on the 'stories' project. Based on the project file structure, this appears to be a creative writing project with character development, world-building, and story creation components.
I should first understand what specific aspect of the story project the user wants to work on. The project has several key directories:
- characters/ - Character profiles and templates
- stories/ - Story templates and drafts
- worlds/ - World-building templates
- media/ - Supporting images and reference materials
- output/ - Final outputs
- research/ - Background research
Since this is our first work session on this project, I should offer a structured approach to help the user get started or continue their work.
I'll provide an overview of the project structure and suggest some starting points based on common creative writing workflows.
The current time is early morning (5:56 AM), which might be a good time for creative work.
Headline	
Initiating work session on the Stories project
Tool Name	
response
Text	
## Stories Project Work Session 📖✨

Welcome to our creative writing workspace! The **Stories** project is well-organized for developing characters, worlds, and narratives. Here's how we can approach our work session:

### Project Structure Overview
```
/home/morris/agent-zero/usr/projects/stories/
├── characters/    # Character profiles and development
├── stories/       # Story drafts and templates
├── worlds/        # World-building documents
├── media/         # Images and reference materials
├── output/        # Final polished outputs
├── research/      # Background research
└── drafts/        # Work-in-progress materials
```

### Recommended Starting Points
1. **Character Development** - Work on character profiles in `/characters/`
2. **World Building** - Expand your setting in `/worlds/`
3. **Story Drafting** - Start a new story or continue existing ones in `/stories/`
4. **Research** - Gather background materials in `/research/`
5. **Media Collection** - Add reference images to `/media/images/`

### How would you like to begin?
- Should we create a new character?
- Would you like to develop your story world?
- Do you want to start writing a new story?
- Or would you prefer to review existing materials first?

*The early morning (5:56 AM) can be a wonderful time for creative work - let's make the most of this inspiration!*
chat A0: Responding
minimize
expand

content_copy

volume_up
Stories Project Work Session 📖✨
Welcome to our creative writing workspace! The Stories project is well-organized for developing characters, worlds, and narratives. Here's how we can approach our work session:

Project Structure Overview
/home/morris/agent-zero/usr/projects/stories/
├── characters/    # Character profiles and development
├── stories/       # Story drafts and templates
├── worlds/        # World-building documents
├── media/         # Images and reference materials
├── output/        # Final polished outputs
├── research/      # Background research
└── drafts/        # Work-in-progress materials
