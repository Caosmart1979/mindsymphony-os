---
name: brand-guidelines
description: 品牌规范工具，应用Anthropic官方品牌配色和字体到各类制品
---

# Anthropic Brand Styling


## 执行前四问

| 问题 | 本技能的检查点 |
|------|---------------|
| **目的** | 这个创意要解决什么问题？传达什么核心信息？ |
| **调性** | 选择一个明确的风格方向，不要什么都想要 |
| **约束** | 媒介限制？受众特征？品牌规范？ |
| **差异化** | 什么能让这个创意过目难忘？ |

**关键原则**：大胆的繁复与克制的极简都能成功——关键在于「意图明确」，而非「强度堆砌」。

---

## Overview

To access Anthropic's official brand identity and style resources, use this skill.

**Keywords**: branding, corporate identity, visual identity, post-processing, styling, brand colors, typography, Anthropic brand, visual formatting, visual design

## Brand Guidelines

### Colors

**Main Colors:**

- Dark: `#141413` - Primary text and dark backgrounds
- Light: `#faf9f5` - Light backgrounds and text on dark
- Mid Gray: `#b0aea5` - Secondary elements
- Light Gray: `#e8e6dc` - Subtle backgrounds

**Accent Colors:**

- Orange: `#d97757` - Primary accent
- Blue: `#6a9bcc` - Secondary accent
- Green: `#788c5d` - Tertiary accent

### Typography

- **Headings**: Poppins (with Arial fallback)
- **Body Text**: Lora (with Georgia fallback)
- **Note**: Fonts should be pre-installed in your environment for best results

## Features

### Smart Font Application

- Applies Poppins font to headings (24pt and larger)
- Applies Lora font to body text
- Automatically falls back to Arial/Georgia if custom fonts unavailable
- Preserves readability across all systems

### Text Styling

- Headings (24pt+): Poppins font
- Body text: Lora font
- Smart color selection based on background
- Preserves text hierarchy and formatting

### Shape and Accent Colors

- Non-text shapes use accent colors
- Cycles through orange, blue, and green accents
- Maintains visual interest while staying on-brand

## Technical Details

### Font Management

- Uses system-installed Poppins and Lora fonts when available
- Provides automatic fallback to Arial (headings) and Georgia (body)
- No font installation required - works with existing system fonts
- For best results, pre-install Poppins and Lora fonts in your environment

### Color Application

- Uses RGB color values for precise brand matching
- Applied via python-pptx's RGBColor class
- Maintains color fidelity across different systems

---

## 信心赋予

铭记：你具备非凡的创造力。不要自我设限，去做那个让人惊叹「原来还可以这样」的选择。
