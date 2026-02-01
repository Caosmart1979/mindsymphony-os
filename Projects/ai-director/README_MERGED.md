# AI Director + MindSymphony = MindDirector 🎬🧠

> "The fusion of creative intelligence and cognitive architecture"

## 🎯 Project Overview

**MindDirector** is the merger of two powerful AI systems:
- **AI Director**: A ReAct agent-based creative director assistant
- **MindSymphony**: A comprehensive cognitive operating system with 90+ skills

This merger creates a unified platform that combines:
- Creative direction capabilities from AI Director
- Vast skill library from MindSymphony (90+ skills)
- Intent routing and task decomposition
- Persona consistency management
- Multi-modal tool integration

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MindDirector OS                          │
├─────────────────────────────────────────────────────────────┤
│  Layer 4: Creative Direction (ai-director)                  │
│  ReAct Agent | Persona Management | Creative Tools          │
├─────────────────────────────────────────────────────────────┤
│  Layer 3: Skill Library (mindsymphony - 90+ skills)        │
│  creative/ | research/ | strategy/ | engineering/ | ...    │
├─────────────────────────────────────────────────────────────┤
│  Layer 2: Cognitive Services                                │
│  Intent Router | Task Decomposer | Security Gate            │
├─────────────────────────────────────────────────────────────┤
│  Layer 1: Core Agent Engine                                 │
│  ReAct Loop | Tool Execution | Memory Management            │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Key Features

### From AI Director
✅ ReAct Agent Architecture (Reasoning + Acting)
✅ Persona Consistency Management
✅ Creative Tools (brainstorming, story structure, visual planning)
✅ Conversation Memory
✅ Anthropic Claude API Integration

### From MindSymphony
✅ 90+ Specialized Skills
✅ Intent Routing System
✅ Task Decomposition (Cognitive Architect)
✅ Security Gateway
✅ External Integrations (n8n, Feishu, Slack, Notion)

## 📁 Project Structure

```
ai-director/
├── agent_core.py              # ReAct agent implementation
├── persona_consistency.py     # Persona management
├── run.py                     # Main entry point
├── core/                      # Core cognitive skills (6 skills)
├── skills/                    # 90+ extension skills
├── router/                    # Intent routing system
├── gateway/                   # Security gateway
├── tools/                     # Tool implementations
├── tests/                     # Test suites
├── docs/                      # Documentation
└── *.md                       # Documentation files
```

## 💡 Quick Start

```python
from ai_director import AIDirector

# Initialize with default "Director Lin" persona
director = AIDirector()

# Start creating
response = director.chat("Help me brainstorm a short film about coffee")
print(response)
```

## 🎭 Core Capabilities

- Creative direction and brainstorming
- Task decomposition and planning
- Research and knowledge exploration
- Brand strategy and identity
- Technical architecture design
- Professional writing and editing

## 📚 Documentation

- SKILL.md - Skill definition
- USAGE.md - Usage guide
- PROJECT_SUMMARY.md - Project summary

---

**Version**: 1.0.0 (Merged)
**Status**: ✅ Production Ready
