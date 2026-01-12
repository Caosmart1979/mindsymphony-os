---
name: brand-guidelines
description: Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and-feel. Use it when brand colors or style guidelines, visual formatting, or company design standards apply.
license: Complete terms in LICENSE.txt
category: design
tags: [brand, design, style, colors, typography, visual-identity, branding]
provides: [brand-guidelines, design-tokens, color-palette, typography-system]
consumes: []
related: [frontend-design, canvas-design, pptx, docx, theme-factory]
interop_metadata:
  skill_id: skills.brand_guidelines
  api_version: v1
  authentication: none
  rate_limit:
    requests_per_minute: 30
---

# Anthropic Brand Styling

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

## Interoperability Support

This skill provides brand design tokens to other skills for consistent styling across all outputs.

### Provided Capabilities

This skill provides the following capabilities to other skills:

#### Brand Guidelines (brand-guidelines)

Provides complete Anthropic brand specifications including colors, typography, and usage guidelines.

**Format**: JSON
**Location**: `references/brand-tokens.json`

#### Design Tokens (design-tokens)

Provides standardized design tokens for consistent styling:
- Color palette (primary, secondary, accent colors)
- Typography system (heading and body fonts)
- Spacing scales

**Format**: JSON
**Usage**: Other skills read these tokens to apply brand styling

#### Color Palette (color-palette)

Provides Anthropic's official color specifications in RGB format.

**Format**: JSON
**Contains**:
- Main colors: Dark (#141413), Light (#faf9f5), Mid Gray (#b0aea5), Light Gray (#e8e6dc)
- Accent colors: Orange (#d97757), Blue (#6a9bcc), Green (#788c5d)

#### Typography System (typography-system)

Provides Anthropic's official font specifications.

**Format**: JSON
**Contains**:
- Heading font: Poppins (with Arial fallback)
- Body font: Lora (with Georgia fallback)

### Consumed Capabilities

This skill does not consume capabilities from other skills - it is a pure provider.

### Related Skills

Provides brand tokens to:
- **frontend-design**: For consistent UI styling
- **canvas-design**: For brand-consistent graphics
- **pptx**: For branded presentations
- **docx**: For branded documents
- **theme-factory**: For theme generation

### Integration Protocol

Other skills can integrate with `brand-guidelines` using the following protocol:

1. **Check for brand tokens**: Look for `brand-guidelines` skill in active context
2. **Read design tokens**: Load tokens from `references/brand-tokens.json`
3. **Apply styling**: Use the tokens to style output consistently
4. **Handle fallback**: If brand tokens not available, use default styling

For complete interoperability details, see [SKILL_INTEROPERABILITY_PROTOCOL.md](../../SKILL_INTEROPERABILITY_PROTOCOL.md).
