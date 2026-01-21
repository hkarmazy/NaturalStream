# Python Conversion of MATLAB Stream Analysis Framework

This directory contains Python scripts that replicate the functionality of the MATLAB folder. The framework generates a stream of item selections, analyzes their properties, and creates visualizations.

## Files

### Core Functions

1. **ModelTimeSeries.py**
   - Generates a time series of item selections based on a behavioral model
   - Parameters: EpisodeLength, MaxNumberPossibleStates, SelectedNumber, Handling (selection probability)
   - Returns: Array of selected items over time

2. **Ranking.py**
   - Ranks items in the stream based on their frequency of occurrence
   - Computes frequency statistics and cumulative proportions
   - Returns: Ranked stream and frequency table

3. **clustering_coef_wu.py**
   - Computes weighted clustering coefficient for each node in a network
   - Based on Onnela et al. (2005) method for weighted undirected graphs
   - Returns: Vector of clustering coefficients

4. **PowerLawFit.py**
   - Fits a power law distribution to frequency data using Maximum Likelihood Estimation (MLE)
   - Implements two methods: analytical solution and numerical optimization
   - Returns: Alpha exponent for power law fit

### Main Script

5. **PlotsPart2.py**
   - Main execution script that orchestrates the entire analysis
   - Generates the stream of items using ModelTimeSeries
   - Ranks items using Ranking function
   - Produces three types of visualizations:
     * **Bar Graph**: Distribution of items by frequency (colored by edge threshold)
     * **Spike Train**: Temporal ordering of item selections
     * **Network Graph**: Transition network between items with weighted edges
   - Computes and reports four key values:
     * **edge**: Rank threshold at 50% cumulative frequency
     * **clustering_coef**: Mean clustering coefficient of the transition network
     * **average_shortest_path**: Mean shortest path distance in the network
     * **alpha**: Power law exponent fitted to frequency distribution

## Configuration

Edit the following parameters in `PlotsPart2.py` (lines 24-27):

```python
EpisodeLength = 120          # Total number of time steps
Options2Select = 2           # Number of items to select per time step
EpisodeOptions = 32          # Total number of possible items
SelectionProbability = 0.95  # Probability of selecting items (vs. empty selection)
```

## Dependencies

- numpy
- pandas
- matplotlib
- networkx
- scipy

Install dependencies with:
```bash
pip install numpy pandas matplotlib networkx scipy
```

## Usage

Run the main analysis:

```bash
python PlotsPart2.py
```

The script will:
1. Generate the item selection stream
2. Rank items by frequency
3. Create visualizations
4. Compute network metrics
5. Fit power law distribution
6. Print summary of key values
7. Save the figure as `plots_output.png`

## Output

### Console Output
The script prints:
- Episode parameters
- Stream shape information
- Edge threshold value
- Clustering coefficient
- Average shortest path
- Alpha exponent
- Summary table with all four key values

### Figure Output
A matplotlib figure with three subplots:
- **Top-left**: Bar graph of item distribution
- **Top-middle**: Spike train of item selections
- **Bottom**: Network graph of item transitions

The figure is saved as `plots_output.png` in the same directory.

## Differences from MATLAB Implementation

1. **Python arrays use 0-based indexing**, while MATLAB uses 1-based indexing (adjusted in conversion)
2. **Network graph computation**: Uses NetworkX library for graph operations instead of MATLAB's built-in graph functions
3. **Visualization**: Uses matplotlib instead of MATLAB's plotting functions (layout and appearance may differ slightly)
4. **Power law fitting**: Implemented with analytical MLE solution (faster than numerical optimization)

## Mathematical Details

### Power Law Fit (Alpha Computation)

The power law probability distribution is:
$$P(x) = (\\alpha - 1) x_{min}^{\\alpha - 1} x^{-\\alpha}$$

The MLE estimator for the exponent is:
$$\\alpha = 1 + \\frac{n}{\\sum_{i=1}^{n} \\ln(x_i / x_{min})}$$

Where:
- $n$ = number of observations
- $x_i$ = observed frequencies
- $x_{min}$ = minimum frequency value

### Clustering Coefficient (Weighted)

$$C_i = \\frac{1}{k_i(k_i-1)} \\sum_{j,l} (W_{ij}^{1/3} W_{il}^{1/3} W_{jl}^{1/3})$$

Where:
- $W_{ij}$ = weight of edge between nodes i and j
- $k_i$ = number of connections for node i

## Author Notes

- The clustering coefficient and shortest path calculations use the normalized transition matrix
- Items with zero frequency are excluded from analysis
- The edge threshold marks the transition from "core" items (colored dark) to "peripheral" items (colored light) in visualizations
