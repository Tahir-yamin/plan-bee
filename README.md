# 🚀 OpenPlanCo - Open-Source Primavera P6 & Project Controls Suite

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-15.0-black.svg)](https://nextjs.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**OpenPlanCo** is a modern, open-source reproduction and modernization of enterprise project planning tools (such as PlanCo Tool). It provides an all-in-one suite for **Primavera P6 XER parsing, DCMA 14-Point schedule health auditing, S-Curve generation, Schedule Comparison (Claim Digger), CPM Transitive Reduction, and Forensic Time Impact Analysis (TIA)**.

---

## 📦 What's Inside (3 Delivery Options)

OpenPlanCo provides complete support across three platforms:

| Component | Technology | Description |
| :--- | :--- | :--- |
| **1. Standalone Core & CLI** | `Python 3.9+`, `openpyxl`, `pydantic` | Fast local XER parser, DCMA auditor, CPM network optimizer, TIA generator, and command-line tool. |
| **2. Native Excel Add-in** | `VBA`, `CustomUI XML`, `xlwings` | Custom Excel Ribbon for WBS level coloring, multi-level outline grouping, bottom-up cost rollups, and dynamic EVM formulas. |
| **3. Full-Stack Web Platform** | `FastAPI`, `Next.js 15`, `Tailwind CSS` | Drag-and-drop web application with interactive Gantt, S-Curves, pass/fail DCMA scorecards, and visual schedule comparison. |

---

## 🏛️ Monorepo Structure

```
open-planco-tool/
├── packages/
│   └── openplanco-core/              # Python Core Library & CLI
│       ├── openplanco/
│       │   ├── parser/               # XER Parser & Writer (%T, %F, %R, %E)
│       │   ├── analyzer/             # DCMA 14-Point Assessment
│       │   ├── comparison/           # Schedule Comparison (Claim Digger)
│       │   ├── network/              # Transitive Reduction & Dangling Logic
│       │   ├── tia/                  # Forensic Half-Step & Zero-Step TIA
│       │   ├── database/             # Primavera SQLite Recovery Tools
│       │   └── converter/            # Excel <-> XER Bi-directional Mapping
│       ├── cli.py                    # OpenPlanCo CLI interface
│       └── tests/                    # Pytest test suite
│
├── apps/
│   ├── excel-addin/                  # Native Microsoft Excel Add-in
│   │   ├── src/                      # Custom Ribbon XML & VBA Modules
│   │   │   ├── RibbonCallbacks.bas
│   │   │   ├── WbsActions.bas
│   │   │   ├── DynamicProgress.bas
│   │   │   └── customUI.xml
│   │   └── xlwings_bridge.py
│   │
│   └── web-dashboard/                # Modern Full-Stack Web App
│       ├── backend/                  # FastAPI REST Service (Port 8000)
│       │   └── main.py
│       └── frontend/                 # Next.js 15 Dashboard (Port 3000)
│           └── src/app/page.tsx
│
├── LICENSE                           # MIT Open Source License
└── README.md                         # Documentation
```

---

## ⚡ Quickstart

### 1. Python Core Library & CLI

```bash
# Clone the repository
git clone https://github.com/your-username/open-planco-tool.git
cd open-planco-tool/packages/openplanco-core

# Install in editable mode
pip install -e .

# Run DCMA 14-Point Audit
openplanco audit sample_schedule.xer

# Compare Baseline vs Update (Claim Digger)
openplanco compare baseline.xer update.xer

# Eliminate redundant logic ties using CPM transitive reduction
openplanco clean input.xer cleaned.xer

# Zero out actuals to create a baseline from an update
openplanco zero update.xer zeroed_baseline.xer

# Generate Forensic TIA Half-Step and Zero-Step schedules
openplanco tia --prev update_month1.xer --curr update_month2.xer --out-half half_step.xer --out-zero zero_step.xer
```

---

### 2. Native Excel Add-in

1. Navigate to `apps/excel-addin/src/`.
2. Import `customUI.xml` into your Excel Add-in workbook (`.xlam`).
3. Import `WbsActions.bas`, `DynamicProgress.bas`, and `RibbonCallbacks.bas` into the VBA Project.
4. Enjoy automated **WBS Coloring**, **Hierarchy Grouping**, **EVM Dynamic Formula Rollups**, and **XER Export** directly from the Excel ribbon!

---

### 3. Full-Stack Web Dashboard

#### Start the FastAPI Backend:
```bash
cd apps/web-dashboard/backend
pip install fastapi uvicorn python-multipart
python main.py
```

#### Start the Next.js Frontend:
```bash
cd apps/web-dashboard/frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to access the drag-and-drop XER analytics workspace.

---

## 🛡️ DCMA 14-Point Assessment Specification

OpenPlanCo implements the complete 14-point audit framework:

1. **Logic**: Identifies activities missing predecessors or successors ($\le 5\%$).
2. **Leads**: Flags negative lags ($0\%$).
3. **Lags**: Identifies positive lags ($\le 5\%$).
4. **Relationship Types**: Enforces Finish-to-Start predominance ($\ge 90\%$).
5. **Hard Constraints**: Flags mandatory start/finish constraints ($\le 5\%$).
6. **High Float**: Identifies activities with total float $> 44$ working days ($\le 5\%$).
7. **Negative Float**: Flags critical path violations ($0\%$).
8. **High Duration**: Highlights remaining durations $> 44$ working days ($\le 5\%$).
9. **Invalid Dates**: Verifies actual vs forecast dates relative to the data date ($0\%$).
10. **Resource Loading**: Assesses resource/cost loading across activities.
11. **Missed Tasks**: Calculates actual finish dates vs. baseline finish dates ($\le 5\%$).
12. **Critical Path Test**: Validates continuity of the critical path to project completion.
13. **Critical Path Float Consumption Index (CAPI)**: Measures critical path float variation.
14. **Baseline Execution Index (BEI)**: Assesses progress velocity against the baseline plan ($\ge 0.95$).

---

## 🤝 Contributing & License

Contributions are welcome! Please feel free to submit a Pull Request.

Licensed under the **MIT License**.
