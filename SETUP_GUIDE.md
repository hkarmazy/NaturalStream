# Python Folder - Complete Framework Summary

## Successfully Converted MATLAB Framework to Python

All files have been created in `/Users/hadar/Dropbox/Python Folder`

### Core Python Modules

1. **ModelTimeSeries.py** (2.6 KB)
   - Implements behavioral time series generation with episode parameters
   - Generates stream of item selections
   - Parameters: EpisodeLength, MaxNumberPossibleStates, SelectedNumber, Handling

2. **Ranking.py** (2.2 KB)
   - Ranks items by frequency of occurrence
   - Creates frequency statistics tables
   - Outputs: StreamRanked (ranked stream) and FrequencyTable (statistics)

3. **clustering_coef_wu.py** (1.1 KB)
   - Weighted clustering coefficient computation (Onnela et al. method)
   - Handles undirected weighted networks
   - Returns clustering coefficient vector for network nodes

4. **PowerLawFit.py** (2.5 KB)
   - Maximum Likelihood Estimation (MLE) power law fitting
   - Computes alpha exponent from frequency distributions
   - Includes two methods: analytical and numerical optimization

5. **PlotsPart2.py** (10 KB) - MAIN SCRIPT
   - Orchestrates entire analysis workflow
   - Generates three visualization plots:
     * Bar graph: Item distribution by frequency
     * Spike train: Temporal sequence of selections
     * Network graph: Item transition network
   - Computes four key values:
     * edge: Rank threshold at 50% cumulative frequency
     * clustering_coef: Mean weighted clustering coefficient
     * average_shortest_path: Mean shortest path in network
     * alpha: Power law exponent

### Documentation Files

1. **README.md** (4.6 KB)
   - User-friendly documentation
   - Installation and usage instructions
   - Configuration parameters
   - Mathematical details

2. **CONVERSION_SUMMARY.md** (5.7 KB)
   - Detailed conversion notes
   - Component mapping from MATLAB to Python
   - Mathematical implementation details
   - Test results and validation notes

3. **examples.py** (6.7 KB)
   - Example usage scripts
   - Custom parameter configurations
   - Batch analysis demonstration
   - Power law analysis examples
   - Network analysis examples

### Configuration & Dependencies

1. **requirements.txt** (75 bytes)
   - Lists all Python dependencies
   - Install with: `pip install -r requirements.txt`

### Output Files

1. **plots_output.png** (197 KB)
   - Generated visualization with three subplots
   - Bar graph, spike train, and network graph
   - Creates automatically when running PlotsPart2.py

## Key Features Implemented

### ✅ All Three Plots Generated
1. **Bar Graph**: Shows distribution of items with color coding
   - Dark colors: Core items (within edge threshold)
   - Light colors: Peripheral items (beyond edge threshold)

2. **Spike Train**: Temporal visualization of item selections
   - X-axis: Time steps
   - Y-axis: Item selections
   - Color gradient represents item frequency ranking

3. **Network Graph**: Item transition network
   - Nodes: Items
   - Edges: Transition probabilities
   - Edge width: Strength of transition
   - Node color: Core vs. peripheral classification

### ✅ Four Key Values Computed
| Value | Description | Computation |
|-------|-------------|-------------|
| **edge** | Core items cutoff (50% cumulative) | From FrequencyTable.cumulative |
| **clustering_coef** | Network clustering | Weighted clustering coefficient |
| **average_shortest_path** | Mean network distance | Shortest paths in network |
| **alpha** | Power law exponent | MLE fit to frequencies |

## Usage

### Basic Usage
```bash
cd /Users/hadar/Dropbox/Python Folder
python PlotsPart2.py
```

### With Custom Parameters
Edit PlotsPart2.py lines 24-27 before running:
```python
EpisodeLength = 120          # Change number of time steps
Options2Select = 2           # Change items per step
EpisodeOptions = 32          # Change total possible items
SelectionProbability = 0.95  # Change selection probability
```

### Batch Analysis
```python
from examples import example_batch_analysis
example_batch_analysis()
```

## Test Results

Successfully executed with default parameters:
```
Episode Length: 120
Options to Select: 2
Episode Options: 32
Selection Probability: 0.95

Stream generated with shape: (120, 2)
Ranked stream shape: (120, 2)
Possible items: 18

Edge (50% threshold):           4
Clustering Coefficient:         0.008627
Average Shortest Path:          1.875817
Alpha (Power Law Exponent):     1.780458
```

## Mathematical Implementations

### Power Law Fit
$$\alpha = 1 + \frac{n}{\sum_{i=1}^{n} \ln(f_i / f_{min})}$$

Where:
- n = number of observations
- f_i = observed frequencies
- f_min = minimum frequency

### Weighted Clustering Coefficient
$$C_i = \frac{1}{k_i(k_i-1)} \sum_{j,l} (W_{ij}^{1/3} W_{il}^{1/3} W_{jl}^{1/3})$$

Where:
- W_ij = weighted connection between nodes i and j
- k_i = number of connections for node i

## Installation Instructions

### Step 1: Verify Python Installation
```bash
python --version  # Should be 3.7 or higher
```

### Step 2: Install Dependencies
```bash
cd /Users/hadar/Dropbox/Python Folder
pip install -r requirements.txt
```

Or install manually:
```bash
pip install numpy pandas matplotlib networkx scipy
```

### Step 3: Run the Analysis
```bash
python PlotsPart2.py
```

### Step 4: View Results
- Output figure saved as `plots_output.png`
- Console output shows all four key values
- Can modify parameters in PlotsPart2.py before running

## File Structure
```
/Users/hadar/Dropbox/Python Folder/
├── ModelTimeSeries.py         # Time series generation
├── Ranking.py                 # Frequency ranking
├── clustering_coef_wu.py      # Weighted clustering
├── PowerLawFit.py             # Power law fitting
├── PlotsPart2.py              # Main script
├── examples.py                # Example usage
├── README.md                  # User documentation
├── CONVERSION_SUMMARY.md      # Conversion details
├── requirements.txt           # Dependencies
└── plots_output.png           # Generated output
```

## Validation Summary

✅ **ModelTimeSeries**: Generates realistic item selection sequences
✅ **Ranking**: Correctly computes frequencies and cumulative distributions
✅ **Clustering Coefficient**: Handles edge cases and weighted networks
✅ **Power Law Fit**: Validates against known distributions
✅ **Main Script**: Successfully generates all three plots and four metrics
✅ **Dependencies**: All required packages available
✅ **Documentation**: Comprehensive guides and examples provided

## Notes

- The framework generates stochastic results (varies between runs due to randomness)
- Visualization styles may differ slightly from MATLAB (matplotlib vs. MATLAB rendering)
- Alpha exponent typically ranges from 1.5 to 2.5 for natural frequency distributions
- Clustering coefficients depend on network density and structure
- All computations use standard numerical methods from scipy and networkx

## Support & Customization

See **examples.py** for:
- Batch processing multiple runs
- Custom parameter configurations
- Power law analysis visualization
- Network analysis details
- Performance comparisons

See **README.md** for:
- Detailed parameter descriptions
- Mathematical background
- Troubleshooting common issues
- Advanced configuration options

---

**Conversion Complete!** All MATLAB functionality has been successfully converted to Python with the addition of power law fitting for alpha computation.
