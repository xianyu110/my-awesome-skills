# Video Tool Homepage Design System

## Layout

| Element         | Guideline                                                                |
| --------------- | ------------------------------------------------------------------------ |
| Header          | Sticky, 68px high, white/translucent surface, 1px bottom border          |
| Content width   | 1120px for sections; up to 1248px for header/footer                      |
| Hero            | Dark utility band with centered copy and the real tool directly below it |
| Tool surface    | Maximum 920px, white background, 8px radius, restrained shadow           |
| Section spacing | 72-96px desktop, 48-60px mobile                                          |
| Repeated cards  | 6-8px radius; never place a card inside another card                     |
| Upgrade         | Full-width band rather than a floating pricing card                      |

The hero should contain the product interaction, not a decorative preview. At common viewport heights, leave enough of the following tools section visible to indicate that the page continues.

## Section Rhythm

1. Core tool hero
2. Available tools
3. Result example
4. Feature explanation
5. Use cases
6. FAQ
7. Paid upgrade
8. Legal/product footer

Alternate white and very light neutral bands. Use borders and spacing for hierarchy; avoid wrapping every section in a card.

## Reference Tokens

```css
--vth-ink: #111827;
--vth-muted: #64748b;
--vth-border: #dbe4f0;
--vth-panel: #f6f8fb;
--vth-hero: #111827;
--vth-primary: #2563eb;
--vth-primary-hover: #1d4ed8;
--vth-cyan: #36c5f0;
--vth-member: #b45309;
--vth-member-bg: #fff7ed;
--vth-success: #047857;
--vth-success-bg: #ecfdf5;
```

Use solid colors. A small logo treatment may use the host brand style, but do not spread gradients across buttons, cards, or page backgrounds.

## Typography

- Use the host sans-serif family; Inter/system sans is a safe fallback.
- Hero H1: 52-60px desktop, 34-38px mobile, line-height 1.08-1.15.
- Section H2: 34-42px desktop, 28-32px mobile.
- Tool labels: 12-14px with strong weight.
- Body: 15-18px, line-height 1.6-1.75.
- Keep letter spacing at `0`; do not scale font size continuously with viewport width.

## Controls

- Inputs: 52-56px high, visible label, 7-8px radius, clear focus ring.
- Primary button: solid primary color, icon plus action label, stable height.
- Secondary action: outline or neutral surface, never equal visual weight to the main command.
- Modes: segmented control with icon, selected state, and clear Pro marker when locked.
- Locked controls remain understandable. Link the Pro cue to pricing and explain the entitlement in nearby text.
- Loading text and icons must not change control dimensions.

## Result Example

Use a realistic result frame with a clear "Example" label. Show only fields the real product returns, such as title, source platform, duration, output format, transcript excerpt, or export options. Never present sample data as a live user result.

## Conversion Pattern

- Keep the free action visually dominant in the hero.
- Mention paid value beside relevant advanced controls without opening a modal automatically.
- Explain benefits before pricing: faster workflows, exports, batch limits, quality, transcription, or API access.
- Place the full upgrade band after FAQ so objections are answered before the final command.
- Use concrete benefit labels rather than generic claims like "more power."

## Responsive Behavior

- At 720px and below, collapse header navigation, stack form actions, and use one-column section grids.
- At 390px, keep 18px page gutters and full-width primary actions.
- Allow platform/tool chips to scroll horizontally when wrapping would make them unreadable.
- Stack the membership cue text and CTA; do not shrink the CTA below a 40px tap target.
- Wrap long URLs with `overflow-wrap: anywhere`.

## Accessibility And QA

- Use semantic `header`, `nav`, `main`, `section`, `form`, `details`, and `footer` elements.
- Associate every input with a label and expose busy state with `aria-busy`.
- Use visible `:focus-visible` outlines and respect `prefers-reduced-motion`.
- Confirm one H1, ordered headings, sufficient contrast, and keyboard-operable FAQ rows.
- Capture 390px, 768px, and 1440px screenshots and compare `scrollWidth` with `clientWidth`.
