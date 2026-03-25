# FINDEC-RS Figures Directory

This directory contains all figures and diagrams referenced in the FINDEC-RS proposal.

## Figure Naming Convention

All figures should follow this naming pattern:
```
[figure_type]_[component]_[version].png
```

Example:
- `system_architecture_v1.png`
- `methodology_pipeline_v2.png`
- `data_flow_diagram_v1.png`

## Required Figures

### 1. **system_architecture.png**
- **Location in document:** Section 1.6 → Proposed Solution → System Architecture
- **LaTeX Label:** `\label{fig:system_architecture}`
- **Dimensions:** 1600 x 1200 px (9.5" × 7.1" at 169 DPI)
- **Description:** 
  - Shows three main layers: Multi-Agent Pipeline, Knowledge Graph, and Inference Layer
  - Display the Bias Detector, Intent Modeler, and Recommender agents
  - Show data flow from user interactions through KG to recommendations
- **Tools to create:**
  - PowerPoint / Lucidchart / Draw.io
  - Adobe Illustrator
  - Python (matplotlib/graphviz)

### 2. **methodology_pipeline.png** (Alternative to TikZ)
- **Location in document:** Section 1.6 → Methodology
- **LaTeX Label:** `\label{fig:methodology_pipeline}`
- **Dimensions:** 1400 x 900 px
- **Description:**
  - Pipeline showing 5 stages: Data Collection → Preprocessing → Multi-Agent Profiling → GNN Inference → Recommendations
  - Color-code each stage (light gray boxes, connected by black arrows)
  - Include icons or labels for each component
- **Note:** This is already implemented as a TikZ diagram in the LaTeX file, so a PNG is optional

### 3. **data_flow_diagram.png**
- **Location in document:** Section 1.6 → Data Flow Diagram
- **LaTeX Label:** `\label{fig:data_flow}`
- **Dimensions:** 1600 x 1000 px
- **Description:**
  - Multiple data sources entering from left (Behavioral Log, Market Data, Sentiment Feeds, User Input)
  - Central processing (Agents, KG, GNN)
  - Outputs on right (Recommendations, Bias Report, Explanations)
- **Tools to create:**
  - Lucidchart / Draw.io (free online)
  - Graphviz
  - Python plotly

### 4. **knowledge_graph_schema.png** (Optional - already has TikZ)
- **Location in document:** Section 1.6 → Knowledge Graph Schema
- **LaTeX Label:** `\label{fig:kg}`
- **Dimensions:** 1200 x 900 px
- **Description:**
  - Already defined as TikZ diagram showing node connections
  - Generate PNG from TikZ if external diagram preferred
- **Note:** Currently uses TikZ code embedded in .tex file

---

## File Format Requirements

- **Format:** PNG (preferred) or PDF
- **Resolution:** 300 DPI for print quality
- **Margins:** Include 10-15px padding around diagram
- **Colors:** Black/white/grayscale for professional appearance
- **Fonts:** Use sans-serif (Arial, Helvetica) for clarity
- **File Size:** Keep under 2MB per image

---

## How to Place Figures in LaTeX

### Step 1: Save PNG file
Place your PNG file in this directory:
```
c:\Users\mansi\FINDEC-RS\figures\system_architecture.png
```

### Step 2: Reference in .tex file
The reference is already in the document:
```latex
\includegraphics[width=0.95\textwidth]{figures/system_architecture.png}
```

### Step 3: Build PDF
Compile LaTeX from the project root:
```bash
pdflatex FINDEC-RS_Proposal.tex
```

---

## Recommended Tools

### Online (Free)
- **Draw.io** (https://www.draw.io) - Best for architecture diagrams
- **Lucidchart** (free tier) - Professional flowcharts
- **Excalidraw** (https://excalidraw.com) - Hand-drawn style diagrams

### Desktop
- **Microsoft PowerPoint** - Export as PNG at high resolution
- **LibreOffice Draw** - Free alternative
- **Inkscape** - Vector graphics (free)

### Programmatic
- **Python + Graphviz** - For data flow and network diagrams
- **Python + matplotlib** - For charts and workflow diagrams
- **Python + networkx** - For knowledge graphs

---

## Export Settings for Each Tool

### From PowerPoint:
1. Right-click slide → Save as Picture → PNG
2. Set Quality: 300 DPI
3. Dimensions: 1600 x 1200 px

### From Draw.io:
1. File → Export as → PNG
2. Zoom: 150%
3. Background: White
4. Transparent: Unchecked

### From Graphviz (Python):
```python
import graphviz

dot = graphviz.Digraph()
# ... add nodes and edges
dot.render('system_architecture', format='png', cleanup=True)
```

---

## Quick Checklist

- [ ] All 3 required PNG files created and placed in `figures/` folder
- [ ] File names follow convention: `[name].png`
- [ ] Resolution is at least 300 DPI
- [ ] Diagrams use black/white/gray colors only
- [ ] File sizes are under 2MB each
- [ ] Diagrams are labeled and include captions
- [ ] LaTeX references match figure location in document

---

## Current Figure References in Document

```
Figure 1: \ref{fig:system_architecture} - System Architecture
Figure 2: \ref{fig:methodology_pipeline} - Methodology Pipeline (TikZ embedded)
Figure 3: \ref{fig:kg} - Knowledge Graph Schema (TikZ embedded)
Figure 4: \ref{fig:data_flow} - Data Flow Diagram
Figure 5: \ref{fig:evaluation_metrics} - Evaluation Dashboard (optional)
```

---

## Troubleshooting

### Figure not displaying?
- Check file path: `figures/filename.png` (relative path)
- Verify PNG exists in `c:\Users\mansi\FINDEC-RS\figures\`
- Run: `pdflatex -interaction=nonstopmode FINDEC-RS_Proposal.tex`

### Image quality is poor?
- Increase DPI to 300+
- Use vector formats (PDF) if possible
- Resize to at least 1600px width

### Large file size?
- Compress PNG using TinyPNG or similar
- Reduce color palette (use grayscale)
- Optimize before placement

---

**Last Updated:** March 25, 2026
