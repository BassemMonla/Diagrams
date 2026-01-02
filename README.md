# Diagrams as Code & Architecture Demo

This repository demonstrates a modern approach to software architecture using "Diagrams as Code", covering both high-level system views and low-level code generation.

## Features

### 1. Interactive Architecture Diagram (`app.py`)
A Streamlit application that allows you to dynamically configure and generate an **Enterprise Medallion Architecture** diagram using the Python `diagrams` library.
- **Toggle Layers**: control visibility of Bronze, Silver, and Gold layers.
- **Layout Controls**: Adjust edge style (splines), spacing, and orientation.

### 2. Full Architecture Demo (`full_demo/`)
A complete "Zoom-In" demonstration showing the different levels of abstraction:

*   **System Level (C4 Model)**: `c4_system.puml`
    *   high-level container diagram (Web App, API, Database) using Structurizr/C4 standard.
*   **Code Level (UML)**: `domain_model.puml`
    *   Detailed class diagram of the API logic (Customer, Account, Transactions).
*   **Source Code Generation**: `generate_src.py`
    *   A script that parses the UML model and **auto-generates** the Python class files in `src/`.
*   **Viewer Dashboard**: `viewer.py`
    *   A consolidated dashboard to view the System Diagram, Class Diagram, and Generated Code side-by-side.

## Getting Started

### Prerequisites

```bash
pip install streamlit diagrams plantuml
```

### Running the Interactive Diagram

```bash
streamlit run app.py
```

### Running the Full Architecture Demo

```bash
streamlit run full_demo/viewer.py
```

## Structure

```
.
├── app.py                  # Main Streamlit Architecture App
├── Diagram.py              # Original static script
├── model.puml              # Basic Banking Class Diagram
├── full_demo/
│   ├── c4_system.puml      # C4 Container Diagram
│   ├── domain_model.puml   # Detailed Domain UML
│   ├── generate_src.py     # Code Generator Script
│   ├── viewer.py           # Demo Dashboard
│   └── src/                # Auto-generated Python code
└── generated/              # Output from basic model demo
```
