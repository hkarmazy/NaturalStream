# Stream Analysis Interactive Tool

A web-based interactive analysis tool for time series stream data with visualization, network analysis, and power law fitting capabilities.

## 🌐 Live Demo

**[Try the app online on Streamlit Cloud](https://stream-analysis-tool.streamlit.app)** (replace with your actual deployed URL)

## Features

### 📊 Core Features
- **Interactive Parameter Input**: Customize stream generation with 4 parameters
- **Real-time Analysis**: Instant computation of network metrics and statistics
- **Three Visualizations**: Bar distribution, spike train, and network graph
- **Color-coded Ranking**: Dark blue for high-rank items (≤ edge), light blue for others
- **Key Metrics Dashboard**: Edge value, clustering coefficient, average path length, power law exponent

### 📈 Advanced Analysis
- **Power Law Analysis**: Log-log plots with fitted power law curves
- **Frequency Analysis**: Detailed frequency tables with cumulative statistics
- **Network Metrics**: Clustering coefficient and shortest path analysis
- **Data Export**: Download results as CSV files

## 🚀 Quick Start

### Option 1: Online (No Installation)
Simply visit the live demo URL and start analyzing!

### Option 2: Run Locally

**Prerequisites:**
- Python 3.8+
- pip or conda

**Installation:**

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/stream-analysis-tool.git
cd stream-analysis-tool

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

## 📋 Parameters Guide

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| **Episode Length** | 10-500 | 120 | Total number of time steps in the stream |
| **Options to Select** | 1-10 | 2 | Number of items selected at each time step |
| **Episode Options** | 5-100 | 32 | Total universe of possible items |
| **Selection Probability** | 0.0-1.0 | 0.95 | Probability of selecting preferred items (higher = more skewed) |

## 📊 Output Explained

### Visualizations

1. **Distribution Bar Graph**
   - Shows frequency distribution of items
   - Dark blue: High-ranking items (rank ≤ edge)
   - Light blue: Low-ranking items (rank > edge)

2. **Spike Train**
   - Temporal visualization of when each item appears
   - Color gradient from dark (frequent) to light (rare)

3. **Network Graph**
   - Shows item transitions and co-occurrence patterns
   - Node size: Proportional to connectivity
   - Node color: Same as distribution graph
   - Edge thickness: Transition frequency

### Key Metrics

- **Edge Value**: Rank where cumulative frequency reaches 50% (separates head from tail)
- **Clustering Coefficient**: Tendency of items to form clusters (0-1 scale)
- **Average Shortest Path**: Average distance between items in network
- **Alpha**: Power law exponent (β ≈ α - 1)

### Power Law Analysis

Log-log plot showing:
- Actual frequency distribution (points)
- Fitted power law curve (red line)
- Power law exponent (α value)

## 🏗️ Project Structure

```
stream-analysis-tool/
├── streamlit_app.py           # Main Streamlit web app
├── PlotsPart2.py              # Original analysis script (reference)
├── ModelTimeSeries.py         # Stream generation engine
├── Ranking.py                 # Stream ranking algorithm
├── clustering_coef_wu.py      # Weighted clustering coefficient
├── PowerLawFit.py             # Power law fitting
├── requirements.txt           # Python dependencies
├── .streamlit/
│   └── config.toml           # Streamlit configuration
├── DEPLOYMENT_GUIDE.md        # Deployment instructions
└── README.md                 # This file
```

## 🔧 How It Works

1. **Stream Generation**: Creates a synthetic time series using the ModelTimeSeries algorithm
2. **Ranking**: Ranks items by frequency
3. **Network Construction**: Builds transition matrix and creates directed graph
4. **Metrics Computation**:
   - Clustering coefficient from weighted adjacency matrix
   - Shortest paths using NetworkX
   - Power law exponent using MLE
5. **Visualization**: Matplotlib for static plots, Streamlit for interaction

## 📥 Data Export

All analysis results can be downloaded as CSV:
- **Frequency Table**: State, frequency, rank, proportion, cumulative distribution
- **Stream Data**: Raw time series with selected items at each timestep

## 🐳 Docker Support (Optional)

To run with Docker:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

Build and run:
```bash
docker build -t stream-analysis .
docker run -p 8501:8501 stream-analysis
```

## 📚 References

- **Streamlit Documentation**: https://docs.streamlit.io
- **NetworkX**: https://networkx.org
- **Power Law Fitting**: Clauset et al. (2009)

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is provided as-is for educational and research purposes.

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named..."
```bash
pip install -r requirements.txt
```

### Slow performance on large datasets
- Reduce Episode Length (max recommended: 300)
- Reduce Episode Options (max recommended: 50)
- Network layout may take time; be patient on first run

### Plots not displaying
Try clearing cache: `streamlit cache clear`

## 📧 Contact

For issues, suggestions, or questions, please open a GitHub issue.

---

**Last Updated**: January 2026
