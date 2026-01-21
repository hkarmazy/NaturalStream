import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
from scipy.spatial.distance import pdist, squareform

from ModelTimeSeries import ModelTimeSeries
from Ranking import Ranking
from clustering_coef_wu import clustering_coef_wu
from PowerLawFit import compute_alpha_mle


def main():
    """
    Main script to generate stream, plots, and compute key values.
    Replicates the MATLAB PlotsPart2.m functionality in Python.
    """
    
    # ============================================
    # Episode Parameters
    # ============================================
    EpisodeLength = 120
    Options2Select = 2
    EpisodeOptions = 32
    SelectionProbability = 0.95
    
    print("=" * 60)
    print("Stream Generation and Analysis")
    print("=" * 60)
    print(f"Episode Length: {EpisodeLength}")
    print(f"Options to Select: {Options2Select}")
    print(f"Episode Options: {EpisodeOptions}")
    print(f"Selection Probability: {SelectionProbability}")
    print()
    
    # ============================================
    # Generate Stream
    # ============================================
    Stream = ModelTimeSeries(EpisodeLength, EpisodeOptions, Options2Select, SelectionProbability)
    print(f"Stream generated with shape: {Stream.shape}")
    
    # ============================================
    # Rank Stream
    # ============================================
    StreamRanked, FrequencyTable = Ranking(Stream)
    PossibleItems = len(FrequencyTable)
    numRows, numCols = StreamRanked.shape
    
    print(f"Ranked stream shape: {StreamRanked.shape}")
    print(f"Possible items: {PossibleItems}")
    print()
    
    # ============================================
    # Compute Key Value: edge
    # ============================================
    Tail = FrequencyTable[FrequencyTable['cumulative'] > 0.5]
    if len(Tail) > 0:
        edge = Tail.iloc[0]['rank']
        edge = int(edge)
    else:
        edge = 1
    
    print(f"Edge (50% cumulative threshold): {edge}")
    
    # ============================================
    # Create FTable for bar graph
    # ============================================
    u = np.unique(StreamRanked)
    u = u[u != 0]
    
    B = []
    for i in range(len(u)):
        item = u[i]
        rows = np.where(StreamRanked == item)
        frq = len(np.unique(rows[0]))
        B.append([item, frq])
    
    B = np.array(B)
    B = B[np.argsort(B[:, 1])[::-1]]
    
    FTable = pd.DataFrame({
        'State': B[:, 0].astype(int),
        'Freq': B[:, 1].astype(int)
    })
    FTable['rank'] = np.arange(1, len(FTable) + 1)
    FTable['prop'] = FTable['Freq'] / FTable['Freq'].sum()
    FTable['sub'] = 1
    FTable = FTable.sort_values('State').reset_index(drop=True)
    
    # ============================================
    # Create figure with subplots
    # ============================================
    fig = plt.figure(figsize=(15, 12))
    
    # Create a 5x5 grid for more flexible layout
    gs = fig.add_gridspec(5, 5, hspace=0.3, wspace=0.3)
    
    # Plot 1: Bar graph (1x1)
    ax1 = fig.add_subplot(gs[0:1, 0:1])
    
    # Plot 2: Spike train (1x1)
    ax2 = fig.add_subplot(gs[0:1, 1:2])
    
    # Plot 3: Network graph (3x3)
    ax3 = fig.add_subplot(gs[2:5, 1:4])
    
    # ============================================
    # Plot 1: Bar Graph (Distribution)
    # ============================================
    colors_bar = np.zeros((len(FTable), 3))
    dark_color = np.array([0.0275, 0.2275, 0.3608])
    light_color = np.array([0.8314, 0.9255, 0.9882])
    
    for i in range(len(FTable)):
        if FTable.iloc[i]['State'] <= edge:
            colors_bar[i] = dark_color
        else:
            colors_bar[i] = light_color
    
    bars = ax1.bar(FTable['rank'], FTable['prop'], color=colors_bar, width=1.0, edgecolor='none')
    ax1.set_ylim([0, 0.5])
    ax1.set_xlim([0, EpisodeOptions])
    ax1.set_xlabel('Rank')
    ax1.set_ylabel('Proportion')
    ax1.set_title('Distribution of Items')
    ax1.grid(False)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    
    # ============================================
    # Plot 2: Spike Train
    # ============================================
    # Create spikes matrix
    spikes = np.zeros((numRows, PossibleItems))
    for i in range(PossibleItems):
        item_rank = i + 1
        rows = np.where(StreamRanked == item_rank)
        spikes[rows[0], i] = 1
    
    # Define colors for spike train
    colors_spike = np.array([
        [0.0275, 0.2275, 0.3608],
        [0.1181, 0.3393, 0.5000],
        [0.1647, 0.4510, 0.6392],
        [0.2843, 0.5490, 0.7255],
        [0.4039, 0.6471, 0.8118],
        [0.5272, 0.7196, 0.8510],
        [0.6510, 0.7922, 0.8902],
        [0.8314, 0.9255, 0.9882],
    ])
    
    # Plot spike train (reversed order for layering)
    for i in range(PossibleItems - 1, -1, -1):
        color_idx = min(i, 7)
        spike_times = np.where(spikes[:, i] == 1)[0]
        ax2.vlines(spike_times, ymin=0, ymax=1, colors=colors_spike[color_idx], linewidth=3)
    
    ax2.set_xlim([0, numRows])
    ax2.set_ylim([0, 1])
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Items')
    ax2.set_title('Spike Train')
    ax2.set_yticks([])
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    
    # ============================================
    # Plot 3: Network Graph
    # ============================================
    # Build adjacency matrix
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
    
    # Normalize adjacency matrix
    total_sum = np.sum(allItemsMatrix)
    if total_sum > 0:
        ItemsMatrix2 = allItemsMatrix / total_sum
    else:
        ItemsMatrix2 = allItemsMatrix
    
    # Create graph
    G = nx.DiGraph()
    G.add_nodes_from(range(1, PossibleItems + 1))
    
    # Add weighted edges
    for i in range(PossibleItems):
        for j in range(PossibleItems):
            if ItemsMatrix2[i, j] > 0:
                G.add_edge(i + 1, j + 1, weight=ItemsMatrix2[i, j])
    
    # Remove isolated nodes
    isolated_nodes = [node for node in G.nodes() if G.degree(node) == 0]
    G.remove_nodes_from(isolated_nodes)
    
    # Remove self-loops
    G.remove_edges_from(nx.selfloop_edges(G))
    
    # Scale weights for visualization
    edge_weights = [G[u][v]['weight'] * 130 for u, v in G.edges()]
    
    # Create node colors based on State value
    node_colors = []
    for node in G.nodes():
        if node <= edge:
            node_colors.append([0.0275, 0.2275, 0.3608])  # Dark color for nodes with rank <= edge
        else:
            node_colors.append([0.8314, 0.9255, 0.9882])  # Light color for others
    
    # ============================================
    # Compute Clustering Coefficient
    # ============================================
    clustering_coef = clustering_coef_wu(ItemsMatrix2)
    clustering_coef[np.isinf(clustering_coef) | np.isnan(clustering_coef)] = 0
    The_clustering_coef = np.mean(clustering_coef)
    
    print(f"Clustering Coefficient: {The_clustering_coef:.6f}")
    
    # ============================================
    # Compute Average Shortest Path
    # ============================================
    # For directed graph, compute distances
    G_undirected = G.to_undirected()
    
    if len(G_undirected.nodes()) > 0:
        AveShortPath = np.zeros((PossibleItems, PossibleItems))
        
        for i in range(PossibleItems):
            for j in range(PossibleItems):
                node_i = i + 1
                node_j = j + 1
                
                if node_i in G_undirected.nodes() and node_j in G_undirected.nodes():
                    try:
                        AveShortPath[i, j] = nx.shortest_path_length(G_undirected, node_i, node_j)
                    except nx.NetworkXNoPath:
                        AveShortPath[i, j] = np.inf
                else:
                    AveShortPath[i, j] = np.inf
        
        AveShortPath[np.isinf(AveShortPath) | np.isnan(AveShortPath)] = 0
        The_AveShortPath = np.nanmean(AveShortPath[AveShortPath > 0]) if np.any(AveShortPath > 0) else 0
    else:
        The_AveShortPath = 0
    
    print(f"Average Shortest Path: {The_AveShortPath:.6f}")
    
    # ============================================
    # Compute Alpha (Power Law Fit)
    # ============================================
    alpha = compute_alpha_mle(FrequencyTable['Freq'].values)
    
    print(f"Alpha (Power Law Exponent): {alpha:.6f}")
    print()
    
    # ============================================
    # Plot Network Graph
    # ============================================
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    
    nx.draw_networkx_nodes(
        G, pos,
        node_color=node_colors,
        node_size=400,
        ax=ax3
    )
    
    nx.draw_networkx_edges(
        G, pos,
        width=edge_weights,
        alpha=0.6,
        ax=ax3,
        edge_color='gray'
    )
    
    ax3.set_title('Network Graph')
    ax3.axis('off')
    
    # ============================================
    # Print Summary
    # ============================================
    print("=" * 60)
    print("KEY VALUES SUMMARY")
    print("=" * 60)
    print(f"Edge (50% threshold):           {edge}")
    print(f"Clustering Coefficient:         {The_clustering_coef:.6f}")
    print(f"Average Shortest Path:          {The_AveShortPath:.6f}")
    print(f"Alpha (Power Law Exponent):     {alpha:.6f}")
    print("=" * 60)
    print()
    
    # Save figure
    output_path = '/Users/hadar/Dropbox/Python Folder/plots_output.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Figure saved to: {output_path}")
    
    # Display figure
    plt.show()
    
    # ============================================
    # Return results as dictionary
    # ============================================
    results = {
        'edge': edge,
        'clustering_coef': The_clustering_coef,
        'average_shortest_path': The_AveShortPath,
        'alpha': alpha,
        'Stream': Stream,
        'StreamRanked': StreamRanked,
        'FrequencyTable': FrequencyTable,
        'FTable': FTable
    }
    
    return results


if __name__ == "__main__":
    results = main()
