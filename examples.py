#!/usr/bin/env python
"""
Example usage and advanced configurations for the Python Stream Analysis Framework.
This file demonstrates various ways to use the framework and customize it.
"""

import numpy as np
import matplotlib.pyplot as plt
from ModelTimeSeries import ModelTimeSeries
from Ranking import Ranking
from clustering_coef_wu import clustering_coef_wu
from PowerLawFit import compute_alpha_mle


def example_basic_usage():
    """
    Example 1: Basic usage - run default analysis
    """
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Usage")
    print("="*60)
    
    # Just run the main script
    exec(open('PlotsPart2.py').read())


def example_custom_parameters():
    """
    Example 2: Run with custom parameters
    """
    print("\n" + "="*60)
    print("EXAMPLE 2: Custom Parameters")
    print("="*60)
    
    # Custom parameters
    EpisodeLength = 200  # Longer episode
    Options2Select = 3   # More items per step
    EpisodeOptions = 50  # More possible items
    SelectionProbability = 0.85  # Lower probability
    
    print(f"Custom Parameters:")
    print(f"  Episode Length: {EpisodeLength}")
    print(f"  Items to Select: {Options2Select}")
    print(f"  Possible Items: {EpisodeOptions}")
    print(f"  Selection Probability: {SelectionProbability}")
    
    # Generate stream
    Stream = ModelTimeSeries(EpisodeLength, EpisodeOptions, Options2Select, SelectionProbability)
    
    # Rank stream
    StreamRanked, FrequencyTable = Ranking(Stream)
    
    print(f"\nResults:")
    print(f"  Stream shape: {Stream.shape}")
    print(f"  Unique items in stream: {len(FrequencyTable)}")
    print(f"  Top 5 items by frequency:")
    print(FrequencyTable[['State', 'Freq', 'rank', 'prop']].head())


def example_batch_analysis():
    """
    Example 3: Run multiple analyses and compare
    """
    print("\n" + "="*60)
    print("EXAMPLE 3: Batch Analysis - Multiple Runs")
    print("="*60)
    
    num_runs = 5
    results = []
    
    for run_id in range(num_runs):
        print(f"\nRun {run_id + 1}/{num_runs}...")
        
        # Generate stream
        Stream = ModelTimeSeries(120, 32, 2, 0.95)
        
        # Rank and compute metrics
        StreamRanked, FrequencyTable = Ranking(Stream)
        
        # Compute alpha
        alpha = compute_alpha_mle(FrequencyTable['Freq'].values)
        
        # Store results
        results.append({
            'run': run_id + 1,
            'unique_items': len(FrequencyTable),
            'top_freq': FrequencyTable.iloc[0]['Freq'],
            'alpha': alpha
        })
        
        print(f"  Items: {len(FrequencyTable)}, Top Freq: {FrequencyTable.iloc[0]['Freq']}, Alpha: {alpha:.4f}")
    
    # Print summary
    print("\n" + "-"*60)
    print("Summary Statistics:")
    print(f"  Mean items: {np.mean([r['unique_items'] for r in results]):.2f}")
    print(f"  Mean alpha: {np.mean([r['alpha'] for r in results]):.4f}")
    print(f"  Std alpha: {np.std([r['alpha'] for r in results]):.4f}")


def example_power_law_analysis():
    """
    Example 4: Detailed power law analysis
    """
    print("\n" + "="*60)
    print("EXAMPLE 4: Power Law Analysis")
    print("="*60)
    
    # Generate stream
    Stream = ModelTimeSeries(200, 40, 2, 0.95)
    StreamRanked, FrequencyTable = Ranking(Stream)
    
    frequencies = FrequencyTable['Freq'].values
    ranks = FrequencyTable['rank'].values
    
    # Compute alpha
    alpha = compute_alpha_mle(frequencies)
    
    print(f"\nPower Law Fit Results:")
    print(f"  Alpha (exponent): {alpha:.4f}")
    print(f"  Data points: {len(frequencies)}")
    print(f"  Min frequency: {frequencies.min()}")
    print(f"  Max frequency: {frequencies.max()}")
    print(f"  Mean frequency: {frequencies.mean():.2f}")
    
    # Plot power law
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Linear plot
    ax1.scatter(ranks, frequencies, alpha=0.6, s=50)
    ax1.set_xlabel('Rank')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Rank vs Frequency')
    ax1.grid(True, alpha=0.3)
    
    # Log-log plot
    ax2.loglog(ranks, frequencies, 'o', alpha=0.6, markersize=8)
    # Add power law line
    x_line = np.logspace(np.log10(ranks.min()), np.log10(ranks.max()), 100)
    # For power law: f = C * rank^(-alpha+1)
    C = frequencies[0] / (ranks[0] ** (-alpha + 1))
    y_line = C * x_line ** (-alpha + 1)
    ax2.loglog(x_line, y_line, 'r--', linewidth=2, label=f'Power Law (α={alpha:.3f})')
    ax2.set_xlabel('Rank')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Power Law Fit (log-log scale)')
    ax2.legend()
    ax2.grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    plt.savefig('/Users/hadar/Dropbox/Python Folder/power_law_analysis.png', dpi=150)
    print("\nPower law plot saved to: power_law_analysis.png")


def example_network_analysis():
    """
    Example 5: Detailed network analysis
    """
    print("\n" + "="*60)
    print("EXAMPLE 5: Network Analysis")
    print("="*60)
    
    # Generate stream
    Stream = ModelTimeSeries(150, 30, 2, 0.95)
    StreamRanked, FrequencyTable = Ranking(Stream)
    
    numRows, numCols = StreamRanked.shape
    PossibleItems = len(FrequencyTable)
    
    # Build transition matrix
    allItemsMatrix = np.zeros((PossibleItems, PossibleItems))
    
    for r in range(PossibleItems):
        for c in range(PossibleItems):
            n = 0
            for i in range(2, numRows - 1):
                TheEvent = StreamRanked[i, :]
                PrevEvent = StreamRanked[i - 1, :]
                
                if (r + 1) in TheEvent and (c + 1) in PrevEvent:
                    n += 1
            
            allItemsMatrix[r, c] = n
    
    # Normalize
    ItemsMatrix2 = allItemsMatrix / np.sum(allItemsMatrix)
    
    # Compute clustering coefficient
    clustering_coef = clustering_coef_wu(ItemsMatrix2)
    clustering_coef[np.isinf(clustering_coef) | np.isnan(clustering_coef)] = 0
    mean_cc = np.mean(clustering_coef)
    
    print(f"\nNetwork Analysis Results:")
    print(f"  Number of items: {PossibleItems}")
    print(f"  Transition matrix sparsity: {np.sum(allItemsMatrix > 0)}/{PossibleItems**2}")
    print(f"  Mean clustering coefficient: {mean_cc:.6f}")
    print(f"  Max clustering coefficient: {np.max(clustering_coef):.6f}")
    print(f"  Min clustering coefficient: {np.min(clustering_coef[clustering_coef > 0]):.6f}")


if __name__ == "__main__":
    print("\n" + "#"*60)
    print("# Stream Analysis Framework - Example Scripts")
    print("#"*60)
    
    # Run examples (uncomment to execute)
    # example_basic_usage()
    example_custom_parameters()
    example_batch_analysis()
    example_power_law_analysis()
    example_network_analysis()
    
    print("\n" + "#"*60)
    print("# All examples completed!")
    print("#"*60)
