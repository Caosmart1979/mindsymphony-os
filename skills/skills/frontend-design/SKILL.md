---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Generates creative, polished code and UI design that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
category: design
tags: [frontend, ui, web, react, vue, html, css]
provides: [design-tokens, component-templates, html-css-code]
consumes: [brand-guidelines, design-tokens, user-assets]
related: [brand-guidelines, canvas-design, theme-factory, artifacts-builder]
interop_metadata:
  skill_id: skills.frontend_design
  api_version: v1
  authentication: none
  rate_limit:
    requests_per_minute: 30
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.

---

## Interoperability Support

This skill supports collaboration with other skills through a flexible interoperability protocol.

### Provided Capabilities

This skill provides the following capabilities to other skills:

#### Design Tokens (design-tokens)

Provides adaptive design tokens including:
- Color specifications
- Typography systems
- Spacing scales

**Format**: JSON
**Usage**: Other skills can read these tokens for consistent styling

#### Component Templates (component-templates)

Provides reusable React/Vue component templates.

**Format**: TSX/VUE
**Usage**: Other skills can use or modify these templates

### Consumed Capabilities

This skill can use the following capabilities from other skills (all optional):

#### Brand Guidelines (brand-guidelines)

- **Source**: `brand-guidelines` skill
- **Purpose**: Apply brand colors and typography
- **Behavior**: If `brand-guidelines` has been applied, automatically use its design tokens
- **Fallback**: Use adaptive design system if no brand guidelines available

#### Design Tokens (design-tokens)

- **Source**: Any skill providing design tokens
- **Purpose**: Maintain consistency across multiple skills
- **Behavior**: Read and apply external design tokens
- **Fallback**: Generate adaptive design tokens

#### User Assets (user-assets)

- **Source**: User-provided `assets/` directory
- **Purpose**: Use custom images, icons, and resources
- **Behavior**: Read and use files from `assets/`
- **Fallback**: Use placeholders or generative content

### Style Inheritance Protocol

This skill uses a flexible styling system:

1. **Check for other skills**: First check if `brand-guidelines` or other skills providing design tokens are active
2. **Apply tokens**: If available, read and apply their design tokens
3. **User overrides**: User can explicitly override any style value
4. **Default behavior**: If no other skills provide tokens, use this skill's default adaptive styling

### Related Skills

Collaborative relationships with:
- **brand-guidelines**: Provides brand specifications
- **canvas-design**: Canvas and graphic design
- **theme-factory**: Theme generation
- **artifacts-builder**: Build deployable artifacts

For complete interoperability details, see [SKILL_INTEROPERABILITY_PROTOCOL.md](../../SKILL_INTEROPERABILITY_PROTOCOL.md).
