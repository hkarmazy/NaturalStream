# Stream Analysis App - Architecture & Data Flow

## 📋 Application Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      STREAMLIT APP                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              LEFT SIDEBAR - USER INPUT                   │   │
│  ├──────────────────────────────────────────────────────────┤   │
│  │  ⚙️ Episode Parameters:                                  │   │
│  │    • Episode Length (10-500)                             │   │
│  │    • Options to Select (1-10)                            │   │
│  │    • Episode Options (5-100)                             │   │
│  │    • Selection Probability (0.0-1.0)                     │   │
│  │                                                           │   │
│  │  🏷️ The Options (Optional):                              │   │
│  │    • Dynamic label input fields                          │   │
│  │    • Order selection (Ranked/Random)                     │   │
│  │    • Label count indicator                               │   │
│  │                                                           │   │
│  │  🚀 Generate Analysis button                             │   │
│  └──────────────────────────────────────────────────────────┘   │
│                           │                                      │
│                           ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │          ANALYSIS ENGINE & COMPUTATION                   │   │
│  ├──────────────────────────────────────────────────────────┤   │
│  │  ModelTimeSeries → Generate stream data                  │   │
│  │       │                                                   │   │
│  │       ▼                                                   │   │
│  │  Ranking → Rank items by frequency                       │   │
│  │       │                                                   │   │
│  │       ▼                                                   │   │
│  │  Optional: The Options Label Mapping                     │   │
│  │    ├─ If Ranked: Sequential mapping                      │   │
│  │    └─ If Random: Shuffled mapping (seed=42)              │   │
│  │       │                                                   │   │
│  │       ▼                                                   │   │
│  │  Build Adjacency Matrix → Network analysis               │   │
│  │       │                                                   │   │
│  │       ├─ NetworkX DiGraph creation                       │   │
│  │       ├─ Clustering coefficient calculation              │   │
│  │       ├─ Average shortest path                           │   │
│  │       └─ Power law exponent (alpha)                      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                           │                                      │
└───────────────────────────┼──────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │      MAIN CONTENT AREA - TABS         │
        ├───────────────────────────────────────┤
        │                                       │
        │  ┌─────────────────────────────────┐ │
        │  │ 📊 Main Analysis Plots (Tab 1)  │ │
        │  │ ┌─────────────────────────────┐ │ │
        │  │ │ 📈 Key Metrics Cards        │ │ │
        │  │ │ • Edge Value                │ │ │
        │  │ │ • Clustering Coefficient    │ │ │
        │  │ │ • Avg Shortest Path         │ │ │
        │  │ │ • Alpha (Power Law)         │ │ │
        │  │ └─────────────────────────────┘ │ │
        │  │                                  │ │
        │  │ ┌─────────────────────────────┐ │ │
        │  │ │ Plots:                      │ │ │
        │  │ │ 1. Distribution Bar Graph   │ │ │
        │  │ │ 2. Spike Train              │ │ │
        │  │ │ 3. Network Graph (enhanced) │ │ │
        │  │ └─────────────────────────────┘ │ │
        │  └─────────────────────────────────┘ │
        │                                       │
        │  ┌─────────────────────────────────┐ │
        │  │ 📈 Power Law Analysis (Tab 2)   │ │
        │  │ • Linear plot (Rank vs Freq)    │ │
        │  │ • Log-log plot with fit curve   │ │
        │  └─────────────────────────────────┘ │
        │                                       │
        │  ┌─────────────────────────────────┐ │
        │  │ 📋 Frequency Table (Tab 3)      │ │
        │  │ • Interactive data display      │ │
        │  │ • Labels (if provided)          │ │
        │  └─────────────────────────────────┘ │
        │                                       │
        │  ┌─────────────────────────────────┐ │
        │  │ 📥 Downloads (Tab 4)            │ │
        │  │ • Frequency Table CSV           │ │
        │  │ • Stream Data CSV               │ │
        │  │ • Stream by Ranked Order CSV    │ │
        │  └─────────────────────────────────┘ │
        │                                       │
        └───────────────────────────────────────┘
```

---

## 🔄 Data Flow Diagram

```
USER INPUT
   │
   ├─ Episode Parameters ──────┐
   │                           │
   └─ The Options ──────┐      │
                        │      │
                        ▼      │
                   ┌────────────┘
                   ▼
        ┌──────────────────────┐
        │ Validate Parameters  │
        └──────────────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ Generate Stream      │
        │ ModelTimeSeries()    │
        └──────────────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ Rank Stream          │
        │ Ranking()            │
        └──────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
   [No Labels]          [With Labels]
        │                     │
        ▼                     ▼
   Use Numeric          Apply Mapping
   Values (1-n)         Ranked/Random
        │                     │
        └──────────┬──────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ Build Network        │
        │ Adjacency Matrix     │
        └──────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
        ▼          ▼          ▼
   Metrics    Network    Power Law
   Analysis   Analysis   Fitting
   Clustering Shortest   Alpha
   Coef.      Path       (MLE)
        │          │          │
        └──────────┼──────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ Create Visualizations│
        │ - Bar Graph          │
        │ - Spike Train        │
        │ - Network (w/ labels)│
        │ - Power Law Plots    │
        └──────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
    Display Results     Prepare Downloads
    (Tabs)             (CSV Files)
        │                     │
        │     ┌───────────────┘
        │     │
        └─────┴──────────────────────┐
                                     │
                                     ▼
                            ┌──────────────────┐
                            │  USER VIEW       │
                            │ Metrics/Plots/   │
                            │ Tables/Downloads │
                            └──────────────────┘
```

---

## 🏷️ The Options Feature Flow

```
                    USER PROVIDES LABELS?
                            │
                ┌───────────┴───────────┐
                │                       │
              NO                      YES
                │                       │
                ▼                       │
         Use Default           ┌────────┴─────────┐
         (1, 2, 3, ...)        │                  │
                │              ▼                  │
                │        Choose Order             │
                │              │                  │
                │        ┌─────┴────┐             │
                │        │          │             │
                │      RANKED    RANDOM           │
                │        │          │             │
                │        ▼          ▼             │
                │    Sequential  Shuffled         │
                │    Mapping     (seed=42)        │
                │        │          │             │
                │        └─────┬────┘             │
                │              │                  │
                │              │                  │
                ▼              ▼                  │
         ┌─────────────────────────────┐         │
         │  STATE TO LABEL MAPPING     │◄────────┘
         │  {1: "Label1", 2: ...}      │
         └─────────────────────────────┘
                      │
            ┌─────────┼─────────┐
            │         │         │
            ▼         ▼         ▼
         Update   Display in  Export in
         Freq     Network     Downloads
         Table    Graph
```

---

## 📊 Network Graph Enhancement

```
BEFORE (Version 1.0)          AFTER (Version 2.0)
─────────────────────         ──────────────────────

      [1]                           [Product A]
       / \                            /    \
     [2] [3]                      [Item1] [Item2]
      \ /                           \ /
      [4]                        [Service]
                        
Size: 400                    Size: 800
Labels: Numeric              Labels: Custom or Numeric
No text display              Text displayed at center
Limited visibility           Better readability
```

---

## 💾 Export Data Structure

```
CSV OPTION 1: Frequency Table
┌─────────────┬──────────┬──────┬───────┬────────────┐
│ State       │ Freq     │ Rank │ Prop  │ Cumulative │
├─────────────┼──────────┼──────┼───────┼────────────┤
│ Apple       │ 45       │ 1    │ 0.375 │ 0.375      │
│ Banana      │ 30       │ 2    │ 0.250 │ 0.625      │
│ Orange      │ 25       │ 3    │ 0.208 │ 0.833      │
└─────────────┴──────────┴──────┴───────┴────────────┘

CSV OPTION 2: Raw Stream
┌──────┬──────┐
│ 1    │ 3    │
│ 2    │ 2    │
│ 3    │ 1    │
│ 1    │ 2    │
└──────┴──────┘

CSV OPTION 3: Ranked Stream (with labels)
┌────────────────────┐
│ Apple, Orange      │
│ Banana, Banana     │
│ Orange, Apple      │
│ Apple, Banana      │
└────────────────────┘
```

---

## 🔐 Session State Management

```
┌─────────────────────────────────────────┐
│      STREAMLIT SESSION STATE            │
├─────────────────────────────────────────┤
│                                         │
│ • run_analysis (bool)                   │
│   Triggers computation on button click  │
│                                         │
│ • the_options_order (str)               │
│   Stores 'ranked' or 'random'          │
│                                         │
│ • episode_options (int)                 │
│   Number of items (from slider)         │
│                                         │
│ • Generated data (cached)               │
│   Stream, Rankings, Analysis results    │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🎯 Feature Decision Tree

```
START APP
│
├─ User enters parameters
│  ├─ Episode Length
│  ├─ Options to Select
│  ├─ Episode Options
│  └─ Selection Probability
│
├─ User clicks "Configure Options"?
│  │
│  ├─ YES
│  │  ├─ Enter labels (optional)
│  │  └─ Choose order (Ranked/Random)
│  │
│  └─ NO
│     └─ Use defaults (1, 2, 3, ...)
│
├─ Click "Generate Analysis"
│
├─ System generates stream
│
├─ System computes metrics
│
├─ System applies label mapping (if provided)
│
├─ System creates visualizations
│  ├─ Bar graph (with colors)
│  ├─ Spike train
│  └─ Network graph (with labels)
│
└─ Display results in tabs
   ├─ Main Analysis Plots
   ├─ Power Law Analysis
   ├─ Frequency Table
   └─ Downloads
```

---

## ⚙️ Technical Stack

```
Frontend:        Streamlit 1.28+
Backend:         Python 3.8+
Data:            NumPy, Pandas
Visualization:   Matplotlib
Network:         NetworkX
Statistics:      SciPy
File I/O:        CSV export

Deployment:      Streamlit Cloud
Repository:      GitHub
Environment:     Virtual Environment (.venv)
```

---

## 🔄 Reproducibility & Seeding

```
REPRODUCIBILITY SOURCES:

1. ModelTimeSeries()
   └─ Uses RandomState (seed-based)

2. Random Order Mapping
   └─ np.random.seed(42) → Fixed seed

3. Network Layout
   └─ spring_layout(iterations=50) → Deterministic with seed

RESULT: Same inputs → Same outputs (across sessions)
```

---

This architecture ensures:
✓ Clean separation of concerns  
✓ Scalable feature additions  
✓ Reproducible results  
✓ User-friendly interface  
✓ Robust data handling  
✓ Professional visualizations  

