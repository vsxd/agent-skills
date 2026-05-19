---
name: editorial-diagram
description: Generate warm editorial technical diagrams as editable .drawio files. Use for flowcharts, architecture diagrams, comparison charts, swimlanes, feedback loops, process visuals, and article-ready technical explainers. Trigger on requests like "draw a diagram", "create a flowchart", "visualize this process", "make an architecture diagram", "画流程图", "画架构图", or "帮我画". Do not use for dense UML/BPMN notation, UI mockups, decorative illustrations, or dashboards unless the user explicitly asks for an editorial diagram.
license: MIT
compatibility: Best in agents that can write local files and generate structured XML. Optional PNG/SVG export requires draw.io Desktop or diagrams.net import.
metadata:
  author: vsxd
  version: "1.0.0"
---

# Editorial Diagram Skill

Generate draw.io diagrams in a warm, minimalist editorial style suitable for technical articles and architecture explainers.

## Use This Skill When

- The user wants an explanatory diagram, flowchart, architecture visual, comparison, swimlane, loop, or process map.
- The output should be an editable `.drawio` file rather than a static illustration.
- A calm, article-ready visual style is more useful than formal notation or dashboard UI.

## Do Not Use

- The user needs strict UML, BPMN, ERD, network topology notation, or another formal diagramming standard.
- The user wants a UI mockup, dashboard, logo, icon set, decorative illustration, or generated bitmap image.
- The user only needs a Mermaid snippet or text-only outline unless they explicitly ask to convert it to draw.io.

## Workflow

```
User text -> DiagramSpec -> Styled draw.io XML -> validate -> .drawio file
```

---

## Step 1: Analyze the Request

Determine:
- **Main claim**: What is the one thing this diagram should make obvious?
- **Pattern**: Which visual pattern best serves that claim? (See Step 2 and `references/pattern-library.md`)
- **Reading direction**: left-to-right for workflows/comparisons; top-to-bottom for stacks/hierarchies

When uncertain about pattern, default rules:
- Sequential steps → Linear Workflow
- System components/containment → Grouped Architecture
- Before/after or two approaches → Split Comparison
- Multiple actors over time → Swimlane
- Overlap/shared ownership → Venn
- Numerical contrast → Editorial Chart

---

## Step 2: Build the DiagramSpec

Before writing XML, draft a concise diagram plan to catch structural mistakes before committing to coordinates. Use this format in working notes; include it in the user-visible response only when the user asks for planning detail or when the structure is unusually ambiguous.

```
**DiagramSpec**

main_claim: [one sentence - what is the diagram making obvious?]
pattern: [primary pattern]
secondary_pattern: [optional, or none]
reading_direction: [left-to-right / top-to-bottom]
title: "Diagram Title"

nodes:
  - id: n1
    label: "Short label"
    semantic_type: [primary | secondary | tertiary | start | end | warning | decision | ai_llm | inactive | error]
    shape: [rect | pill | diamond | cylinder]
    group: [container_id if inside a container, else none]

connections:
  - from: n1
    to: n2
    label: ""          # keep short or empty
    style: [primary | optional | feedback | human | context | error]

groups:
  - id: g1
    label: "Panel title"
    type: [outer_panel | inner_panel | swimlane | soft_region]
    children: [n1, n2, ...]
```

After drafting the DiagramSpec, **proceed immediately to Step 3** without waiting for user confirmation unless the request is missing essential facts. Read `references/pattern-library.md` for layout rules per pattern type.

**Language consistency**: Write the DiagramSpec and all node labels, titles, and edge labels in the final XML in the same language the user used. If the user wrote in Chinese, the diagram text should be Chinese too.

---

## Step 3: Generate draw.io XML

### Canvas setup

```xml
<mxGraphModel background="#F2EFE8" grid="0" tooltips="0" connect="0" arrows="0" fold="0" page="0" pageScale="1" pageWidth="1654" pageHeight="1169" math="0" shadow="0">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <!-- all cells go here with parent="1" (or parent="container_id" if nested) -->
  </root>
</mxGraphModel>
```

Use `background="#F2EFE8"` (warm canvas) for most diagrams. Use `background="#FFFFFF"` only for very minimal, sparse diagrams with few elements.

### Title

```xml
<mxCell id="title" value="Your Diagram Title" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;overflow=hidden;fontStyle=1;fontSize=32;fontColor=#1F1F1C;" vertex="1" parent="1">
  <mxGeometry x="80" y="40" width="1200" height="50" as="geometry"/>
</mxCell>
```

### Node style strings by semantic type

Apply these styles based on the semantic role, not just aesthetics. The color encodes meaning.

| Semantic type | draw.io style |
|---|---|
| **Primary / Neutral** | `rounded=1;whiteSpace=wrap;arcSize=10;fillColor=#E6E2DA;strokeColor=#8C867F;strokeWidth=1.8;fontColor=#2D2B28;fontSize=20;` |
| **Secondary / Context** | `rounded=1;whiteSpace=wrap;arcSize=10;fillColor=#EAF4FB;strokeColor=#6FA8D6;strokeWidth=1.8;fontColor=#2D2B28;fontSize=20;` |
| **Tertiary / Control** | `rounded=1;whiteSpace=wrap;arcSize=10;fillColor=#EEEAF9;strokeColor=#9A90D6;strokeWidth=1.8;fontColor=#2D2B28;fontSize=20;` |
| **Start / Trigger** | `rounded=1;whiteSpace=wrap;arcSize=50;fillColor=#F8E9E1;strokeColor=#D88966;strokeWidth=1.8;fontColor=#D88966;fontSize=20;fontStyle=1;` |
| **End / Success** | `rounded=1;whiteSpace=wrap;arcSize=10;fillColor=#CFE8D7;strokeColor=#71AE88;strokeWidth=1.8;fontColor=#2D2B28;fontSize=20;` |
| **Warning / Reset** | `rounded=1;whiteSpace=wrap;arcSize=10;fillColor=#F3E4DA;strokeColor=#C88E6A;strokeWidth=1.8;fontColor=#2D2B28;fontSize=20;` |
| **Decision** | `rhombus;whiteSpace=wrap;fillColor=#E6D7B4;strokeColor=#BFA777;strokeWidth=1.8;fontColor=#2D2B28;fontSize=20;` |
| **AI / LLM** | `rounded=1;whiteSpace=wrap;arcSize=10;fillColor=#D7E6DC;strokeColor=#7FB08F;strokeWidth=1.8;fontColor=#2D2B28;fontSize=20;` |
| **Inactive / Disabled** | `rounded=1;whiteSpace=wrap;arcSize=10;fillColor=#EFECE6;strokeColor=#B4AEA6;strokeWidth=1.8;fontColor=#7A756E;fontSize=20;` |
| **Error** | `rounded=1;whiteSpace=wrap;arcSize=10;fillColor=#F8DFDA;strokeColor=#D96B63;strokeWidth=1.8;fontColor=#2D2B28;fontSize=20;` |
| **Pill label** | `rounded=1;whiteSpace=wrap;arcSize=50;fillColor=#FAF8F4;strokeColor=#8C867F;strokeWidth=1.8;fontColor=#2D2B28;fontSize=20;` |
| **Code/evidence block** | `rounded=1;whiteSpace=wrap;arcSize=6;fillColor=#EEF3F7;strokeColor=#B7C9D8;strokeWidth=1.5;fontColor=#44515C;fontSize=20;align=left;` |

For semantic meaning of each type, read `references/color-palette.md` → Semantic Mapping Rules section.

### Container / panel styles

All container styles include `html=1;` so that the `value` attribute can contain HTML. Use a `<font>` tag in the `value` to control the label font size (typically 2–4px larger than the `fontSize` in the style string, for visual hierarchy).

**Outer panel** (large system boundary):
```
rounded=1;whiteSpace=wrap;arcSize=4;fillColor=#FAF8F4;strokeColor=#8C867F;strokeWidth=2;fontSize=18;fontStyle=1;fontColor=#5F5A54;swimlane;startSize=63;horizontal=1;html=1;
```
value: `<font style="font-size: 22px;">Panel Title</font>`

**Inner panel** (subsystem or grouping):
```
rounded=1;whiteSpace=wrap;arcSize=6;fillColor=#FAF8F4;strokeColor=#8C867F;strokeWidth=1.8;fontSize=16;fontStyle=1;fontColor=#5F5A54;swimlane;startSize=50;horizontal=1;html=1;
```
value: `<font style="font-size: 20px;">Panel Title</font>`

**Soft region** (dashed grouping, no strong boundary):
```
rounded=1;fillColor=#F6F4EE;strokeColor=#B9B3AB;strokeWidth=1.5;dashed=1;dashPattern=6 6;fontSize=16;fontColor=#7A756E;html=1;
```
value: `<font style="font-size: 18px;">Region Label</font>`

Example XML for an outer panel:
```xml
<mxCell id="panel_server" parent="1" style="rounded=1;whiteSpace=wrap;arcSize=4;fillColor=#FAF8F4;strokeColor=#8C867F;strokeWidth=2;fontSize=18;fontStyle=1;fontColor=#5F5A54;swimlane;startSize=63;horizontal=1;html=1;" value="&lt;font style=&quot;font-size: 22px;&quot;&gt;Panel Title&lt;/font&gt;" vertex="1">
  <mxGeometry x="580" y="110" width="480" height="920" as="geometry"/>
</mxCell>
```

Children of containers use `parent="container_id"` and coordinates relative to the container.

### Connector styles

**The single most important style rule**: all arrows use open chevron arrowheads.

```
endArrow=open;endSize=14;
```

This is what gives the diagrams their clean, editorial look. Never use filled/block arrowheads.

All connectors also use `edgeStyle=orthogonalEdgeStyle` — this makes lines route with right-angle bends and gives the diagram a clean, structured feel. Combined with `rounded=1`, the corners are softened into smooth curves rather than hard turns.

| Connector type | Full style |
|---|---|
| **Primary flow** | `endArrow=open;endSize=14;edgeStyle=orthogonalEdgeStyle;strokeColor=#7A756E;strokeWidth=1.8;rounded=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;` |
| **Optional / inferred** | `endArrow=open;endSize=14;edgeStyle=orthogonalEdgeStyle;strokeColor=#9A948C;strokeWidth=1.6;rounded=1;dashed=1;dashPattern=6 6;` |
| **Feedback loop** | `endArrow=open;endSize=14;edgeStyle=orthogonalEdgeStyle;strokeColor=#8E8982;strokeWidth=1.8;rounded=1;curved=1;` |
| **Human override** | `endArrow=open;endSize=14;edgeStyle=orthogonalEdgeStyle;strokeColor=#D88966;strokeWidth=1.8;rounded=1;dashed=1;dashPattern=6 6;` |
| **Context / support** | `endArrow=open;endSize=14;edgeStyle=orthogonalEdgeStyle;strokeColor=#7FB08F;strokeWidth=1.8;rounded=1;` |
| **Error path** | `endArrow=open;endSize=14;edgeStyle=orthogonalEdgeStyle;strokeColor=#D96B63;strokeWidth=1.8;rounded=1;` |

Every edge cell must have a child geometry element — never self-close:
```xml
<mxCell id="e1" edge="1" source="n1" target="n2" style="endArrow=open;endSize=14;edgeStyle=orthogonalEdgeStyle;strokeColor=#7A756E;strokeWidth=1.8;rounded=1;" parent="1">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

---

## Step 4: Layout rules

These rules keep diagrams feeling calm and well-composed:

- **Node spacing**: minimum 80px horizontal gap between adjacent nodes; 60px vertical gap
- **Recommended horizontal pitch**: 200px center-to-center for workflow steps
- **Recommended vertical pitch**: 120px center-to-center for parallel elements
- **Canvas padding**: 60px around the outermost content
- **Grid alignment**: snap all positions to multiples of 10
- **Node size**: standard nodes 140×60 to 180×70; wide containers 300–600+; title bar height 40
- **Keep layout flat**: max 3 nesting levels; prefer whitespace over extra containers

For pattern-specific layout rules (swimlane lane widths, comparison panel sizing, fan-out spacing, etc.), read `references/pattern-library.md` → the relevant pattern section.

### Outer border

Every diagram gets a single outer border — a thin rounded rectangle that frames the entire composition (title + all content). This gives the diagram a poster-like finish and makes the whitespace feel intentional rather than accidental.

- Place this cell **first** in the XML, before all other nodes, so it renders behind everything
- `x=20, y=20`; width = pageWidth − 40 (→ **1614** for the standard 1654px canvas)
- Height: extend ~40px below the lowest node — snug enough to feel cohesive, loose enough to breathe
- Style: subtle warm stroke, no fill (the canvas background shows through)

```xml
<mxCell id="border" value="" style="rounded=1;arcSize=3;fillColor=none;strokeColor=#B9B3AB;strokeWidth=1.5;pointerEvents=0;" vertex="1" parent="1">
  <mxGeometry x="20" y="20" width="1614" height="1000" as="geometry"/>
</mxCell>
```

Adjust `height` so it ends roughly 40px below the bottom-most element. `pointerEvents=0` keeps it non-interactive so users can click through it in draw.io.

---

## Step 5: Write, validate, optionally open

1. Write the complete XML to a descriptive `.drawio` file in the current working directory unless the user requested another output path.
   - Filename: lowercase with hyphens, e.g., `agent-loop.drawio`, `context-engineering.drawio`
   - Prefer raw `<mxGraphModel>` XML for portability and easy validation. Uncompressed `<mxfile>` wrappers are acceptable; compressed draw.io payloads are not ideal for generated output because they are harder to inspect.
2. Validate the file when this skill's script is available:
   - `python3 scripts/validate_drawio.py <filename>.drawio`
   - If running from outside the skill directory, use the full path to `scripts/validate_drawio.py`.
3. Do not make desktop opening a hard requirement. Open only when the user asks, a GUI desktop is available, or the local workflow clearly supports it:
   - macOS: `open <filename>.drawio`
   - Linux: `xdg-open <filename>.drawio`
   - Windows PowerShell: `Start-Process <filename>.drawio`
   - Windows cmd: `start "" <filename>.drawio`
4. If opening fails, keep the generated file and report the path. Opening failure is not generation failure.

If the user asks for PNG/SVG export:
```bash
# macOS
"/Applications/draw.io.app/Contents/MacOS/draw.io" -x -f png -e -b 20 -o output.png input.drawio

# Linux
drawio -x -f png -e -b 20 -o output.png input.drawio
# or, depending on installation:
draw.io -x -f png -e -b 20 -o output.png input.drawio

# Windows PowerShell
& "C:\Program Files\draw.io\draw.io.exe" -x -f png -e -b 20 -o output.png input.drawio
```
For SVG export, replace `-f png` with `-f svg` and use an `.svg` output path. If draw.io Desktop is unavailable, deliver the `.drawio` file and explain that export requires draw.io Desktop or diagrams.net import.

---

## Quality checklist

Before finalizing the XML, verify:

- [ ] Outer border present (`id="border"`, first cell in XML, x=20 y=20, width=1614, height covers all content + 40px)
- [ ] Title is large (fontSize >= 28), bold, dark (#1F1F1C), horizontally centered
- [ ] Canvas background set (`background="#F2EFE8"` in mxGraphModel)
- [ ] Every arrow uses `endArrow=open;endSize=14`
- [ ] Node colors follow semantic meaning, not decoration
- [ ] Main flow path is visually dominant within 3 seconds
- [ ] No more than 4 semantic accent colors in one diagram
- [ ] Every edge has `<mxGeometry relative="1" as="geometry"/>`
- [ ] All coordinates are multiples of 10
- [ ] No `--` inside XML comments (invalid XML)
- [ ] Special characters escaped: `&amp;` `&lt;` `&gt;`
- [ ] `scripts/validate_drawio.py` passes when available
- [ ] File delivery does not depend on a platform-specific opener succeeding

---

## Reference files

- `references/color-palette.md` — Full semantic color rules, text hierarchy, container specs, background values, geometry tokens. Read when you need to choose colors or verify a semantic mapping.
- `references/pattern-library.md` — 12 diagram patterns with layout rules, anti-patterns, and combination rules. Read when the pattern choice is ambiguous or the layout needs fine-tuning.
- `scripts/validate_drawio.py` — Lightweight structural validator for generated `.drawio` XML.
