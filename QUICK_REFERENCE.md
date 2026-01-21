# Stream Analysis App - Quick Reference Card

## 🎯 Basic Workflow

### Step 1: Set Episode Parameters (Required)
1. **Episode Length** (10-500): How long is your stream?
2. **Options to Select** (1-10): How many items per time step?
3. **Episode Options** (5-100): How many total items exist?
4. **Selection Probability** (0.0-1.0): How biased toward popular items?

### Step 2: Configure Custom Labels (Optional)
1. Click "Configure Options" to expand
2. Enter labels for each item (or leave blank for numbers)
3. Choose order: Ranked (sequential) or Random (default)
4. Confirm number of labels provided

### Step 3: Generate Analysis
1. Click "🚀 Generate Analysis" button
2. Wait for computation (takes a few seconds)
3. View results in tabs below

### Step 4: Explore Results
1. **Main Analysis Plots**: Three visualizations
2. **Power Law Analysis**: Statistical distributions
3. **Frequency Table**: Complete data table
4. **Downloads**: Export results as CSV

---

## 🎨 Visualization Guide

### Distribution Bar Graph
- **Dark Blue Bars**: High-ranking items (rank ≤ edge)
- **Light Blue Bars**: Low-ranking items (rank > edge)
- **Edge Value**: Separates head (frequent) from tail (rare)
- **Height**: Relative frequency of each item

### Spike Train
- **Vertical Lines**: When an item appears
- **Color Gradient**: Dark (frequent) to Light (rare)
- **X-axis**: Time steps
- **Y-axis**: Individual items

### Network Graph
- **Nodes**: Represent items
- **Node Colors**: Same as bar graph (dark/light blue)
- **Node Size**: 800 (larger for visibility)
- **Edges**: Transition relationships
- **Edge Thickness**: How often transitions occur

---

## 📊 Key Metrics Explained

| Metric | Range | Meaning |
|--------|-------|---------|
| **Edge** | 1 - n | Rank where 50% frequency threshold is crossed |
| **Clustering Coef** | 0 - 1 | How clustered items form groups (higher = more clustered) |
| **Avg Shortest Path** | 1+ | Average distance between items in network |
| **Alpha** | 0.5+ | Power law exponent (measures distribution skewness) |

---

## 🏷️ The Options Feature

### Default (No Custom Labels)
```
Episode Options: 3
Nodes display as: [1] [2] [3]
Downloads show: 1, 2, 3
```

### With Custom Labels (Ranked)
```
Episode Options: 3
Labels: ["Apple", "Banana", "Cherry"]
Order: Ranked (sequential)
Result: State 1 → Apple, State 2 → Banana, State 3 → Cherry
Nodes display as: [Apple] [Banana] [Cherry]
Downloads show: Apple, Banana, Cherry
```

### With Custom Labels (Random)
```
Episode Options: 3
Labels: ["Apple", "Banana", "Cherry"]
Order: Random
Result: States randomly mapped to labels
Example: State 1 → Banana, State 2 → Apple, State 3 → Cherry
Nodes display as: [Banana] [Apple] [Cherry]
Downloads show: Random assignment
```

---

## 📥 Download Options

### 1. Frequency Table (CSV)
**Contains**: State, Frequency, Rank, Proportion, Cumulative
**Use For**: Statistical analysis, reporting

### 2. Stream Data (CSV)
**Contains**: Raw stream (numeric 1 to n)
**Use For**: Custom analysis, simulation reproducibility

### 3. Stream by Ranked Order (CSV)
**Contains**: Selected items per time step
**Use For**: Sequence analysis, behavioral study
**Shows**: Custom labels if provided

---

## ⚙️ Advanced Features

### Ranked vs Random Order

**Ranked Order**:
- First label → Most frequent state
- Second label → Second most frequent state
- Good for: Pre-defined hierarchies

**Random Order**:
- Labels randomly shuffled to states
- Reproducible (uses seed=42)
- Good for: Blind analysis, avoiding bias

### Node Labels

**If Custom Options**:
- Shows your label (e.g., "Product A")
- Displays in center of node

**If Default**:
- Shows numeric rank (1, 2, 3, ...)
- Displays in center of node

---

## 🐛 Common Issues & Solutions

| Problem | Solution |
|---------|----------|
| Labels not showing | Click "Generate Analysis" after entering labels |
| Network graph too small | Labels are shortened; try shorter names |
| Numbers showing instead of labels | Confirm labels were entered and saved |
| Random order gives same result | This is correct - seed is fixed for reproducibility |
| Episode Options mismatch | Number of labels must ≤ Episode Options value |

---

## 💡 Tips & Tricks

1. **Start Simple**: Try default (no labels) first to understand the data
2. **Use Short Labels**: Keeps network graph readable (5-15 chars ideal)
3. **Consistent Naming**: Use same format (all caps, snake_case, etc.)
4. **Test Order**: Compare Ranked vs Random to see impact
5. **Check Preview**: Look at "Stream by Ranked Order" preview before downloading
6. **Export Everything**: Download all 3 CSV files for complete record

---

## 🔍 Analysis Tips

### For Frequency Analysis
1. Look at **Edge value** - divides head from tail
2. Check **Clustering Coefficient** - how grouped items are
3. Review **Frequency Table** - see exact distribution

### For Network Analysis
1. Observe **node colors** - dark = frequent items
2. Check **edge thickness** - common transitions
3. Look at **node proximity** - related items cluster

### For Power Law
1. Check **Alpha value**:
   - α > 2: Very skewed distribution
   - α ≈ 1.5: Moderately skewed
   - α < 1: Weak power law
2. View **log-log plot** - straight line = good fit

---

## 📚 Documentation

- **THE_OPTIONS_GUIDE.md**: Detailed feature documentation
- **README_WEBAPP.md**: General app information
- **DEPLOYMENT_GUIDE.md**: How to deploy on GitHub
- **FEATURES_UPDATE.md**: Latest changes and updates

---

## ⌨️ Keyboard Shortcuts

- **R**: Refresh app
- **C**: Clear cache
- **Ctrl+S**: Save page

---

**Last Updated**: January 21, 2026  
**Version**: 2.0
