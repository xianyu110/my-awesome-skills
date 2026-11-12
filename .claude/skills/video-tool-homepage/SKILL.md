---
name: video-tool-homepage
description: Build or restyle conversion-focused homepages for public-link video utilities, downloaders, transcription tools, media converters, and similar SaaS products. Use when a user wants a homepage organized around an immediately usable tool, supported tools, result examples, feature explanations, use cases, FAQ, and a paid upgrade section. Supports React, TanStack, Next.js, Vite, and adaptation to other frontend stacks.
---

# Video Tool Homepage

Build a product-first homepage for a video utility. Put the working tool in the first viewport, explain value through concrete outputs, and introduce paid features without blocking the free workflow.

## Required Page Order

Use this sequence unless the existing product has a stronger information architecture:

1. **Core tool hero** - URL input, paste action, primary command, supported-platform signal, and a compact member-feature cue.
2. **Available tools** - Show the downloader, transcription, audio, batch, quality, or API tools that actually exist.
3. **Result example** - Demonstrate a real or clearly labeled sample output. Call this "Result example" or "Parse example," not "Generated example," unless the product generates media.
4. **Feature explanation** - Explain reliability, output choices, privacy, retries, export formats, or workflow details.
5. **Use cases** - Map the tool to creators, social teams, researchers, editors, or other real audiences.
6. **FAQ** - Resolve platform support, failures, copyright, privacy, credits, and membership questions.
7. **Paid upgrade** - End with the complete membership value proposition and a clear upgrade command.

Keep a light member cue next to locked controls earlier in the page. Do not wait until the final pricing section to explain why a control is locked.

## Workflow

1. Inspect the existing frontend stack, routes, design system, icon library, data-fetching layer, auth state, and billing model.
2. Read [references/design-system.md](references/design-system.md) before implementing the visual direction.
3. Inventory only real capabilities. Separate free, signed-in, and paid-member features before writing copy.
4. Reuse the existing component primitives and icons. For React projects, start from [assets/VideoToolHomepage.tsx](assets/VideoToolHomepage.tsx) and [assets/video-tool-homepage.css](assets/video-tool-homepage.css), then adapt them to local conventions.
5. Wire every visible command to real behavior. Pass callbacks into the template or connect it through the host application's established API client.
6. Replace all example brand text, links, result data, pricing claims, and legal links with product-specific values.
7. Verify responsive layout, keyboard access, loading/error states, membership states, and SEO metadata.

## Framework Guidance

- **Existing React application:** Copy the template assets into the application's block/component boundary. Replace plain anchors with the local navigation component and move copy into the existing i18n system.
- **TanStack or ShipAny:** Keep page composition in routes/blocks, use the existing API client and TanStack Query for network state, and do not import server modules into components.
- **Next.js:** Add a client boundary only around interactive controls. Keep static sections server-rendered when practical.
- **Other frameworks:** Port the semantic section structure and CSS tokens. Preserve behavior and hierarchy rather than React-specific syntax.
- **Established design system:** Prefer local buttons, inputs, icons, spacing tokens, and focus states over duplicating the asset CSS.

## Product Rules

- Make the actual tool the first-screen experience. Do not replace it with a marketing-only hero.
- Keep the brand and literal product category visible in the first viewport.
- Show a hint of the next section on common desktop and mobile viewports.
- Use icons for recognizable actions. Prefer the host application's Lucide integration when available.
- Keep cards at 8px radius or less. Do not nest cards or turn every section into a floating panel.
- Use quiet neutral surfaces, one primary action color, cyan for utility signals, amber for locked membership cues, and green for successful states.
- Do not use decorative gradient blobs, oversized display type inside tools, or viewport-scaled font sizes.
- Do not publish fake download counts, ratings, platform support, testimonials, or result examples.
- Do not claim watermark removal, private-content access, or platform bypassing unless the implementation and legal position support the claim.
- Include copyright, privacy, terms, and deletion/takedown links when the product processes third-party media.

## Paid Feature Pattern

Use two levels of paid messaging:

1. **Contextual cue:** Put a small crown/Pro label beside member-only controls such as transcription, batch jobs, audio-only output, best quality, or API access. Clicking it should open pricing or the relevant upgrade flow.
2. **Full upgrade band:** After FAQ, summarize the membership outcome, list 4-6 concrete benefits, show honest pricing or a neutral "View plans" command, and provide a secondary link to compare plans.

Enforce entitlements on the server. A disabled or hidden frontend control is not access control. Do not describe one-time credit packs as memberships unless they really unlock the same entitlements.

## Content And SEO

- Write copy in the user's requested languages and use the host i18n system when one exists.
- Give each public page a unique title, description, canonical URL, and social metadata.
- Add `WebSite` and `SoftwareApplication` structured data where accurate. Add `FAQPage` only when the FAQ is visible on the page.
- Use one H1, descriptive H2 headings, real labels, and explicit button text.
- Create platform-specific pages only when they contain useful, platform-specific content and working internal links.

## Verification

Check at 390px, 768px, and 1440px:

- No horizontal overflow, clipped text, overlapping controls, or layout shifts.
- Tap targets are at least 40px and keyboard focus is visible.
- Long URLs and translated copy wrap safely.
- Paste, submit, FAQ, tool links, and upgrade actions work.
- Loading, empty, error, free-user, signed-in, and paid-member states are coherent.
- The next section remains discoverable below the hero.
- Light and dark modes remain readable if the host application supports both.

Run the host project's fastest type/lint check, then its production build. Use browser screenshots for desktop and mobile before handing off.

## Resources

- [references/design-system.md](references/design-system.md): Required layout, visual, responsive, and conversion guidance.
- [assets/VideoToolHomepage.tsx](assets/VideoToolHomepage.tsx): Controlled React template with no API or brand coupling.
- [assets/video-tool-homepage.css](assets/video-tool-homepage.css): Responsive reference styling using the `vth-` class prefix.
