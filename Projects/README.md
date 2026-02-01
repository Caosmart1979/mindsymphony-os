# AI Director - Intelligent Video Script Creation System

> Let AI be your video director and generate professional video scripts with one click

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![AI](https://img.shields.io/badge/AI-GLM%20%7C%20Gemini-green.svg)](https://open.bigmodel.cn/)

## Features

- 🎯 **Smart Script Generation** - AI automatically creates video scripts
- 🎨 **Storyboard Description** - Detailed shot and scene descriptions
- 🎤 **Voiceover Lines** - Automatically generate narration and dialogue
- 🎵 **Music Suggestions** - Intelligently recommend background music
- 🎭 **Multiple Styles** - Support for various video styles
- ⚡ **Fast Response** - Based on free AI APIs, generates in seconds

## Quick Start

### 1. Install Dependencies

```bash
pip install requests
```

### 2. Configure AI API

Choose either option:

**Option A: GLM-4-Flash (Recommended)**
- Free 2.58M tokens/day
- Register: https://open.bigmodel.cn/
- Setup: `export GLM_API_KEY="your_key"`

**Option B: Gemini Flash**
- Free 15 requests/minute
- Register: https://aistudio.google.com/
- Setup: `export GEMINI_API_KEY="your_key"`

For detailed setup, see: [API_SETUP_GUIDE.md](API_SETUP_GUIDE.md)

### 3. Test Connection

```bash
python test_api.py
```

### 4. Start Using

```python
from ai_director import AIDirector

# Create AI director
director = AIDirector()

# Generate video script
script = director.generate_script(
    topic="How to make perfect pour-over coffee",
    duration=30,
    style="warm and healing"
)

# View results
print(script.title)
for scene in script.scenes:
    print(f"{scene.time}: {scene.description}")
```

## Demo Examples

### Generated Script Example

**Topic**: The Slow Time of Hand-pour Coffee

```json
{
  "title": "The Slow Time of Hand-pour Coffee",
  "style": "warm and healing",
  "music": "soft jazz",
  "scenes": [
    {
      "time": "0-5s",
      "shot": "close-up",
      "description": "Coffee beans slowly poured into hand grinder",
      "voiceover": "Good coffee starts with a single bean"
    },
    {
      "time": "5-10s",
      "shot": "medium shot",
      "description": "Hand-cranking the grinder, powder falling",
      "voiceover": "Every grind is a沉淀 of patience"
    }
  ]
}
```

## Use Cases

- 📱 **Short Video Creation** - TikTok,快手,小红书
- 🎬 **Video Planning** - Professional video production pre-production
- 📺 **Content Marketing** - Product promotion, brand stories
- 🎓 **Educational Videos** - Knowledge sharing, tutorials
- 🎪 **Creative Inspiration** - Break through creative blocks

## Tech Stack

- **Python 3.8+** - Core development language
- **GLM-4-Flash** - Zhipu AI free large model
- **Gemini Flash** - Google free AI service
- **Requests** - HTTP request library

## Project Structure

```
ai-director/
├── ai_director/           # Core module
│   ├── __init__.py
│   └── director.py        # AI director class
├── api_clients/           # API clients
│   ├── gemini_client.py
│   └── glm_client.py
├── examples/              # Example code
│   └── demo.py
├── tests/                 # Test files
├── API_SETUP_GUIDE.md    # Setup guide
├── test_api.py           # Test script
└── README.md
```

## API Comparison

| Feature | GLM-4-Flash | Gemini Flash |
|---------|-------------|--------------|
| Free Quota | 2.58M tokens/day | 15 requests/min |
| Response Speed | ⚡⚡⚡ | ⚡⚡⚡ |
| Chinese Support | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Recommended | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## Documentation

- [API Setup Guide](API_SETUP_GUIDE.md)
- [Usage Examples](examples/demo.py)
- [Test Script](test_api.py)

## Contributing

Issues and Pull Requests are welcome!

## License

MIT License

## Acknowledgments

- [Zhipu AI](https://open.bigmodel.cn/) - For providing GLM-4-Flash free API
- [Google AI](https://ai.google.dev/) - For providing Gemini Flash free API

---

**Start your AI creation journey!** 🎬✨
