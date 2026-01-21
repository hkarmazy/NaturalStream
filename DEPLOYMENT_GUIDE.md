# Stream Analysis Web App - Deployment Guide

This guide explains how to deploy the Streamlit web app on GitHub and host it using Streamlit Cloud.

## Prerequisites

- GitHub account (free)
- GitHub repository for this project

## Steps to Deploy

### 1. Prepare Your GitHub Repository

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Stream Analysis Web App"

# Create a new repository on GitHub and push
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### 2. Create a `.streamlit/config.toml` File

Create a `.streamlit/` directory and add a `config.toml` file:

```toml
[theme]
primaryColor = "#0275398C"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = true

[server]
headless = true
port = 8501
```

### 3. Deploy Using Streamlit Cloud

1. Visit [https://streamlit.io/cloud](https://streamlit.io/cloud)
2. Sign up with your GitHub account
3. Click "New app"
4. Select your repository, branch, and the app file (`streamlit_app.py`)
5. Click "Deploy"

The app will be live at a URL like: `https://your-username-your-repo-name.streamlit.app`

### 4. Update Your GitHub README

Add this section to your `README.md`:

```markdown
## 🚀 Live Demo

[Try the app online](https://your-username-your-repo-name.streamlit.app)

## Running Locally

```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`
```

## File Structure

```
your-repo/
├── streamlit_app.py          # Main Streamlit application
├── PlotsPart2.py             # Original analysis script
├── ModelTimeSeries.py        # Stream generation
├── Ranking.py                # Stream ranking
├── clustering_coef_wu.py     # Clustering coefficient
├── PowerLawFit.py            # Power law fitting
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml          # Streamlit configuration
└── README.md                # Documentation
```

## Features

- ✅ Interactive parameter input (Episode Length, Options, Probability)
- ✅ Real-time visualization of 3 plots
- ✅ Key metrics display (Edge, Clustering Coef, Avg Path, Alpha)
- ✅ Power law analysis with log-log plots
- ✅ CSV download for Frequency Table and Stream data
- ✅ Responsive design for desktop and mobile

## Troubleshooting

### "Module not found" errors
Ensure all files (ModelTimeSeries.py, Ranking.py, etc.) are in the same directory as `streamlit_app.py`

### Plot display issues
Streamlit may cache plots. Add `st.rerun()` or use `st.write(fig)` instead of `st.pyplot(fig)` if needed

### Slow performance
The network layout computation can be slow for large datasets. Consider caching or reducing iterations:
```python
pos = nx.spring_layout(G, k=0.5, iterations=30)  # Reduced from 50
```

## File Size Limits

- Streamlit Cloud has resource limits
- Stream with Episode Length > 500 and Options > 50 may slow down
- Consider limiting parameters: Episode Length max 300, Options max 50

## Contact & Support

For issues or improvements, create a GitHub issue in your repository.
