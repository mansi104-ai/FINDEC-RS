# Python Scripts to Generate Diagram Figures

This file contains Python code to programmatically generate the required diagrams.
These scripts use Graphviz and can be run to auto-generate PNG files.

## Prerequisites

```bash
# Install graphviz package
pip install graphviz

# Install graphviz system package (Windows)
choco install graphviz
# Or download from: https://graphviz.org/download/

# Install matplotlib
pip install matplotlib networkx
```

---

## 1. System Architecture Diagram

Save this as: `c:\Users\mansi\FINDEC-RS\generate_system_architecture.py`

```python
import graphviz

# Create graph
dot = graphviz.Digraph(comment='System Architecture', format='png')
dot.attr(rankdir='TB', bgcolor='white', splines='ortho')
dot.attr('node', shape='box', style='filled', fillcolor='lightgray', 
         color='black', penwidth='1.5', fontname='Arial')
dot.attr('edge', color='black', penwidth='1.5')

# Input Layer
dot.node('input', 'User\nInteractions')
dot.node('market', 'Market Data\n(yfinance)')
dot.node('sentiment', 'Sentiment\n(NewsAPI)')
dot.node('explicit', 'User Explicit\nPreferences')

# Processing Layer
dot.node('collect', 'Data\nCollection')
dot.node('preprocess', 'Data\nPreprocessing')

# Multi-Agent Layer
dot.node('bias', 'Bias Detector\nAgent', fillcolor='#FFE4E1')
dot.node('intent', 'Intent Modeler\nAgent', fillcolor='#E6E6FA')
dot.node('kg', 'Knowledge Graph\nAgent', fillcolor='#E0F4F7')

# Inference Layer
dot.node('gnn', 'GNN Encoder\n(GraphSAGE/GAT)')
dot.node('bias_correct', 'Bias Correction\nWeighting')

# Output Layer
dot.node('rank', 'Asset Ranking\nand Scoring')
dot.node('explain', 'Explanation\nGeneration')
dot.node('output', 'Recommendations\nwith Bias Alerts')

# Edges - Input to Processing
dot.edge('input', 'collect')
dot.edge('market', 'collect')
dot.edge('sentiment', 'collect')
dot.edge('explicit', 'collect')
dot.edge('collect', 'preprocess')

# Edges - Processing to Multi-Agent
dot.edge('preprocess', 'bias')
dot.edge('preprocess', 'intent')
dot.edge('preprocess', 'kg')

# Edges - Multi-Agent to Inference
dot.edge('bias', 'gnn')
dot.edge('intent', 'gnn')
dot.edge('kg', 'gnn')
dot.edge('gnn', 'bias_correct')

# Edges - Inference to Output
dot.edge('bias_correct', 'rank')
dot.edge('rank', 'explain')
dot.edge('explain', 'output')

# Save as PNG
dot.render('figures/system_architecture', cleanup=True)
print("✓ Generated: figures/system_architecture.png")
```

**Run with:**
```bash
cd c:\Users\mansi\FINDEC-RS
python generate_system_architecture.py
```

---

## 2. Methodology Pipeline Diagram

Save as: `c:\Users\mansi\FINDEC-RS\generate_methodology_pipeline.py`

```python
import graphviz

dot = graphviz.Digraph(comment='Methodology Pipeline', format='png')
dot.attr(rankdir='TB', bgcolor='white', splines='ortho')
dot.attr('node', shape='box', style='filled', fillcolor='#F0F0F0', 
         color='black', penwidth='1.5', fontname='Arial', fontsize='10')
dot.attr('edge', color='black', penwidth='1.5', arrowsize='1.5')

# Stage 1
dot.node('s1', 'Stage 1:\nData Collection\n& Preprocessing', 
         fillcolor='#FFE4E1')

# Stage 2
dot.node('s2a', 'Bias\nDetection', fillcolor='#FFE4E1')
dot.node('s2b', 'Intent\nModeling', fillcolor='#E6E6FA')
dot.node('s2c', 'KG\nConstruction', fillcolor='#E0F4F7')

# Stage 3
dot.node('s3', 'Stage 3:\nGNN Encoding\n& Bias Correction', fillcolor='#F5DEB3')

# Stage 4
dot.node('s4', 'Stage 4:\nRanking &\nScoring', fillcolor='#E6D2B5')

# Stage 5
dot.node('s5', 'Stage 5:\nExplanation\nGeneration', fillcolor='#D4E6E6')

# Output
dot.node('out', 'Personalized\nRecommendations', fillcolor='#E0FFE0', 
         shape='ellipse')

# Edges
dot.edge('s1', 's2a')
dot.edge('s1', 's2b')
dot.edge('s1', 's2c')

dot.edge('s2a', 's3')
dot.edge('s2b', 's3')
dot.edge('s2c', 's3')

dot.edge('s3', 's4')
dot.edge('s4', 's5')
dot.edge('s5', 'out')

dot.render('figures/methodology_pipeline', cleanup=True)
print("✓ Generated: figures/methodology_pipeline.png")
```

**Run with:**
```bash
cd c:\Users\mansi\FINDEC-RS
python generate_methodology_pipeline.py
```

---

## 3. Data Flow Diagram

Save as: `c:\Users\mansi\FINDEC-RS\generate_data_flow_diagram.py`

```python
import graphviz

dot = graphviz.Digraph(comment='Data Flow Diagram', format='png')
dot.attr(rankdir='LR', bgcolor='white', splines='smooth')
dot.attr('node', shape='box', style='filled', fillcolor='lightblue', 
         color='black', penwidth='1.5', fontname='Arial')
dot.attr('edge', color='black', penwidth='1.5')

# Data Sources
dot.node('behavioral', 'Behavioral\nInteraction\nLogs', fillcolor='#FFE4E1')
dot.node('market', 'Market Data\n(yfinance/\nAlpha Vantage)', fillcolor='#FFE4E1')
dot.node('sentiment', 'Sentiment Feeds\n(NewsAPI/\nSEBI)', fillcolor='#FFE4E1')
dot.node('explicit', 'User Explicit\nPreferences', fillcolor='#FFE4E1')

# Processing
dot.node('agents', 'Multi-Agent\nProfiling\n(3 parallel)', fillcolor='#E6E6FA')
dot.node('kg', 'Knowledge\nGraph\n(Neo4j)', fillcolor='#E0F4F7')

# Inference
dot.node('gnn', 'GNN Inference\n(PyTorch)', fillcolor='#F5DEB3')

# Outputs
dot.node('rec', 'Recommendations\n& Badges', fillcolor='#E0FFE0')
dot.node('exp', 'Explanations\nand Reports', fillcolor='#E0FFE0')
dot.node('bias_report', 'Bias Profile\nReports', fillcolor='#E0FFE0')

# Dashboard
dot.node('dashboard', 'User Dashboard\n(Next.js)', fillcolor='#FFE6E6')

# Connections
dot.edge('behavioral', 'agents')
dot.edge('market', 'agents')
dot.edge('sentiment', 'agents')
dot.edge('explicit', 'agents')

dot.edge('agents', 'kg')
dot.edge('kg', 'gnn')

dot.edge('gnn', 'rec')
dot.edge('gnn', 'exp')
dot.edge('gnn', 'bias_report')

dot.edge('rec', 'dashboard')
dot.edge('exp', 'dashboard')
dot.edge('bias_report', 'dashboard')

dot.render('figures/data_flow_diagram', cleanup=True)
print("✓ Generated: figures/data_flow_diagram.png")
```

**Run with:**
```bash
cd c:\Users\mansi\FINDEC-RS
python generate_data_flow_diagram.py
```

---

## 4. Knowledge Graph Schema Visualization

Save as: `c:\Users\mansi\FINDEC-RS\generate_kg_schema.py`

```python
import graphviz

dot = graphviz.Digraph(comment='Knowledge Graph Schema', format='png')
dot.attr(rankdir='TB', bgcolor='white')
dot.attr('node', shape='circle', style='filled', fillcolor='lightblue', 
         color='black', penwidth='1.5', fontname='Arial', fontsize='9')
dot.attr('edge', color='black', penwidth='1.5', arrowsize='1.2')

# Nodes
dot.node('user', 'User', fillcolor='#FFB6C1')
dot.node('bias', 'Bias\nType', fillcolor='#FFE4E1')
dot.node('intent', 'Intent\nVector', fillcolor='#E6E6FA')
dot.node('asset', 'Asset/\nFund', fillcolor='#E0F4F7')
dot.node('sector', 'Sector', fillcolor='#D4E6D4')
dot.node('fund', 'Fund\nManager', fillcolor='#F5DEB3')

# Edges with labels
dot.edge('user', 'bias', label='exhibits')
dot.edge('user', 'intent', label='has_intent')
dot.edge('user', 'asset', label='has_interest')
dot.edge('user', 'fund', label='trusts')

dot.edge('asset', 'sector', label='belongs_to')
dot.edge('bias', 'asset', label='corrects_toward')
dot.edge('intent', 'asset', label='weights')

dot.render('figures/knowledge_graph_schema', cleanup=True)
print("✓ Generated: figures/knowledge_graph_schema.png")
```

**Run with:**
```bash
cd c:\Users\mansi\FINDEC-RS
python generate_kg_schema.py
```

---

## Running All Scripts at Once

Save as: `c:\Users\mansi\FINDEC-RS\generate_all_figures.py`

```python
#!/usr/bin/env python3
"""
Generate all FINDEC-RS figures automatically
"""

import os
import subprocess
import sys

scripts = [
    'generate_system_architecture.py',
    'generate_methodology_pipeline.py',
    'generate_data_flow_diagram.py',
    'generate_kg_schema.py'
]

print("=" * 60)
print("FINDEC-RS Figure Generation")
print("=" * 60)

# Create figures directory if it doesn't exist
os.makedirs('figures', exist_ok=True)

success_count = 0
for script in scripts:
    if os.path.exists(script):
        print(f"\n▶ Running {script}...")
        try:
            exec(open(script).read())
            success_count += 1
        except Exception as e:
            print(f"✗ Error running {script}: {e}")
    else:
        print(f"✗ File not found: {script}")

print("\n" + "=" * 60)
print(f"✓ Successfully generated {success_count}/{len(scripts)} figures")
print("=" * 60)
print("\nGenerated files in: c:\\Users\\mansi\\FINDEC-RS\\figures\\")
print("  - system_architecture.png")
print("  - methodology_pipeline.png")
print("  - data_flow_diagram.png")
print("  - knowledge_graph_schema.png")
```

**Run with:**
```bash
cd c:\Users\mansi\FINDEC-RS
python generate_all_figures.py
```

---

## Manual LaTeX Compilation After Generating Figures

```bash
cd c:\Users\mansi\FINDEC-RS

# Generate all figures
python generate_all_figures.py

# Compile PDF (requires all .png files present)
pdflatex FINDEC-RS_Proposal.tex
pdflatex FINDEC-RS_Proposal.tex  # Run twice for TOC/references

# View result
start FINDEC-RS_Proposal.pdf
```

---

## Troubleshooting Python Scripts

### Error: `FileNotFoundError: Cannot find dot executable`
**Solution:** Install Graphviz system package
```bash
# Windows (using Chocolatey)
choco install graphviz

# Or download from:
https://graphviz.org/download/
# Add to PATH: C:\Program Files\Graphviz\bin
```

### Error: `Module graphviz not found`
**Solution:** Install Python package
```bash
pip install graphviz
```

### PNG files not generated
**Solution:** Check permissions
```bash
# Ensure figures directory is writable
icacls c:\Users\mansi\FINDEC-RS\figures /grant Users:F
```

---

**Tip:** Use these scripts for quick updates. If you need to edit and re-release the PDF, simply update the diagram logic and re-run!
