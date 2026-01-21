"""
Stream Analysis Interactive Web App
A Streamlit application for analyzing time series streams with visualization and analysis tools.
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
from io import StringIO
import io

from ModelTimeSeries import ModelTimeSeries
from Ranking import Ranking
from clustering_coef_wu import clustering_coef_wu
from PowerLawFit import compute_alpha_mle


# Set page config
st.set_page_config(
    page_title="Stream Analysis Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Stream Analysis Interactive Tool")
st.markdown("Analyze time series streams with customizable parameters and visualizations")

# Initialize session state
if 'the_options_order' not in st.session_state:
    st.session_state.the_options_order = 'random'

# Sidebar for inputs
st.sidebar.header("⚙️ Episode Parameters")
st.sidebar.markdown("Configure the stream generation parameters:")

col1, col2 = st.sidebar.columns(2)
with col1:
    episode_length = st.number_input(
        "Episode Length",
        min_value=10,
        max_value=500,
        value=120,
        step=10,
        help="Total number of time steps in the episode"
    )

with col2:
    options_2_select = st.number_input(
        "Options to Select",
        min_value=1,
        max_value=10,
        value=2,
        step=1,
        help="Number of items selected at each time step"
    )

col3, col4 = st.sidebar.columns(2)
with col3:
    episode_options = st.number_input(
        "Episode Options",
        min_value=5,
        max_value=100,
        value=32,
        step=5,
        help="Total number of possible items in the universe"
    )

with col4:
    selection_probability = st.slider(
        "Selection Probability",
        min_value=0.0,
        max_value=1.0,
        value=0.95,
        step=0.05,
        help="Probability of selecting preferred items"
    )

# ============================================
# The Options Configuration (Optional)
# ============================================
st.sidebar.markdown("---")
st.sidebar.header("🏷️ The Options (Optional)")
st.sidebar.markdown("Specify custom labels for the items (leave empty to use numeric values)")

the_options = None
has_custom_options = False

with st.sidebar.expander("Configure Options", expanded=False):
    st.markdown(f"**Enter {episode_options} labels** (one per field):")
    
    # Create input fields for The Options
    the_options_inputs = []
    cols = st.columns(2)
    
    for i in range(episode_options):
        col_idx = i % 2
        with cols[col_idx]:
            option_value = st.text_input(
                f"Option {i+1}",
                value="",
                key=f"option_{i}",
                placeholder=f"{i+1}"
            )
            the_options_inputs.append(option_value)
    
    # Order selection
    st.markdown("**Options Order:**")
    is_ranked = st.checkbox(
        "Ranked order (sequential mapping)",
        value=False,
        help="If checked: sequentially map State to Options in order. If unchecked (default): randomly map State to Options"
    )
    st.session_state.the_options_order = 'ranked' if is_ranked else 'random'
    
    # Check if The Options are actually provided (not all empty)
    the_options = [opt.strip() for opt in the_options_inputs]
    has_custom_options = any(the_options)
    
    if has_custom_options:
        st.info(f"✓ {sum(1 for opt in the_options if opt)} custom labels provided")

if st.sidebar.button("🚀 Generate Analysis", use_container_width=True):
    st.session_state['run_analysis'] = True

if st.session_state.get('run_analysis', False):
    with st.spinner("Generating stream and analyzing data..."):
        
        # Generate stream
        Stream = ModelTimeSeries(episode_length, episode_options, options_2_select, selection_probability)
        
        # Rank stream
        StreamRanked, FrequencyTable = Ranking(Stream)
        PossibleItems = len(FrequencyTable)
        numRows, numCols = StreamRanked.shape
        
        # Compute edge value
        Tail = FrequencyTable[FrequencyTable['cumulative'] > 0.5]
        if len(Tail) > 0:
            edge = Tail.iloc[0]['rank']
            edge = int(edge)
        else:
            edge = 1
        
        # Create FTable for bar graph
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
        # Handle The Options Mapping
        # ============================================
        option_labels = None
        state_to_option_mapping = {}
        
        if has_custom_options and the_options:
            # Filter out empty options and get non-empty ones
            non_empty_options = [opt for opt in the_options if opt.strip()]
            
            if len(non_empty_options) > 0:
                # Create mapping based on order
                unique_states = sorted(FTable['State'].unique())
                
                if st.session_state.the_options_order == 'ranked':
                    # Sequential mapping: first state -> first option, etc.
                    for i, state in enumerate(unique_states):
                        if i < len(non_empty_options):
                            state_to_option_mapping[state] = non_empty_options[i]
                else:
                    # Random mapping
                    np.random.seed(42)  # For reproducibility
                    shuffled_options = np.random.permutation(non_empty_options).tolist()
                    for i, state in enumerate(unique_states):
                        if i < len(shuffled_options):
                            state_to_option_mapping[state] = shuffled_options[i]
                
                # Create option labels list indexed by state
                option_labels = [''] * (max(unique_states) + 1)
                for state, label in state_to_option_mapping.items():
                    option_labels[state] = label
        
        # ============================================
        # Build adjacency matrix for network
        # ============================================
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
        
        for i in range(PossibleItems):
            for j in range(PossibleItems):
                if ItemsMatrix2[i, j] > 0:
                    G.add_edge(i + 1, j + 1, weight=ItemsMatrix2[i, j])
        
        isolated_nodes = [node for node in G.nodes() if G.degree(node) == 0]
        G.remove_nodes_from(isolated_nodes)
        G.remove_edges_from(nx.selfloop_edges(G))
        
        # ============================================
        # Compute metrics
        # ============================================
        clustering_coef = clustering_coef_wu(ItemsMatrix2)
        clustering_coef[np.isinf(clustering_coef) | np.isnan(clustering_coef)] = 0
        the_clustering_coef = np.mean(clustering_coef)
        
        # Average shortest path
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
            the_ave_short_path = np.nanmean(AveShortPath[AveShortPath > 0]) if np.any(AveShortPath > 0) else 0
        else:
            the_ave_short_path = 0
        
        # Alpha
        alpha = compute_alpha_mle(FrequencyTable['Freq'].values)
        
        # ============================================
        # Display Key Values
        # ============================================
        st.header("📈 Key Analysis Values")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Edge Value",
                f"{edge}",
                help="Rank where cumulative frequency reaches 50%"
            )
        
        with col2:
            st.metric(
                "Clustering Coefficient",
                f"{the_clustering_coef:.6f}",
                help="Network clustering coefficient"
            )
        
        with col3:
            st.metric(
                "Avg Shortest Path",
                f"{the_ave_short_path:.6f}",
                help="Average shortest path length in network"
            )
        
        with col4:
            st.metric(
                "Alpha (Power Law)",
                f"{alpha:.6f}",
                help="Power law exponent"
            )
        
        # ============================================
        # Display Plots
        # ============================================
        st.header("📊 Visualizations")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "Main Analysis Plots",
            "Power Law Analysis",
            "Frequency Table",
            "Downloads"
        ])
        
        # Tab 1: Main plots
        with tab1:
            st.subheader("Main Analysis Plots")
            
            fig = plt.figure(figsize=(15, 12))
            gs = fig.add_gridspec(5, 5, hspace=0.3, wspace=0.3)
            
            # Bar graph
            ax1 = fig.add_subplot(gs[0:1, 0:1])
            
            colors_bar = np.zeros((len(FTable), 3))
            dark_color = np.array([0.0275, 0.2275, 0.3608])
            light_color = np.array([0.8314, 0.9255, 0.9882])
            
            for i in range(len(FTable)):
                if FTable.iloc[i]['State'] <= edge:
                    colors_bar[i] = dark_color
                else:
                    colors_bar[i] = light_color
            
            ax1.bar(FTable['rank'], FTable['prop'], color=colors_bar, width=1.0, edgecolor='none')
            ax1.set_ylim([0, 0.5])
            ax1.set_xlim([0, episode_options])
            ax1.set_xlabel('Rank')
            ax1.set_ylabel('Proportion')
            ax1.set_title('Distribution of Items')
            ax1.grid(False)
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            
            # Spike train
            ax2 = fig.add_subplot(gs[0:1, 1:2])
            
            spikes = np.zeros((numRows, PossibleItems))
            for i in range(PossibleItems):
                item_rank = i + 1
                rows = np.where(StreamRanked == item_rank)
                spikes[rows[0], i] = 1
            
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
            
            # Network graph
            ax3 = fig.add_subplot(gs[2:5, 1:4])
            
            edge_weights = [G[u][v]['weight'] * 130 for u, v in G.edges()]
            
            node_colors = []
            for node in G.nodes():
                if node <= edge:
                    node_colors.append([0.0275, 0.2275, 0.3608])
                else:
                    node_colors.append([0.8314, 0.9255, 0.9882])
            
            pos = nx.spring_layout(G, k=0.5, iterations=50)
            
            nx.draw_networkx_nodes(
                G, pos,
                node_color=node_colors,
                node_size=800,  # Increased from 400
                ax=ax3
            )
            
            nx.draw_networkx_edges(
                G, pos,
                width=edge_weights,
                alpha=0.6,
                ax=ax3,
                edge_color='gray'
            )
            
            # Add labels to nodes
            if option_labels and has_custom_options:
                # Use The Options labels
                node_labels = {}
                for node in G.nodes():
                    if node <= len(option_labels) - 1 and option_labels[node]:
                        node_labels[node] = option_labels[node]
                    else:
                        node_labels[node] = str(node)
            else:
                # Use rank order numbers
                node_labels = {node: str(node) for node in G.nodes()}
            
            nx.draw_networkx_labels(
                G, pos,
                labels=node_labels,
                font_size=10,
                font_weight='bold',
                ax=ax3
            )
            
            ax3.set_title('Network Graph')
            ax3.axis('off')
            
            st.pyplot(fig)
            plt.close()
        
        # Tab 2: Power law analysis
        with tab2:
            st.subheader("Power Law Analysis")
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            
            frequencies = FrequencyTable['Freq'].values
            ranks = FrequencyTable['rank'].values
            
            # Linear plot
            ax1.scatter(ranks, frequencies, alpha=0.6, s=50)
            ax1.set_xlabel('Rank')
            ax1.set_ylabel('Frequency')
            ax1.set_title('Rank vs Frequency')
            ax1.grid(True, alpha=0.3)
            
            # Log-log plot
            ax2.loglog(ranks, frequencies, 'o', alpha=0.6, markersize=8)
            x_line = np.logspace(np.log10(ranks.min()), np.log10(ranks.max()), 100)
            C = frequencies[0] / (ranks[0] ** (-alpha + 1))
            y_line = C * x_line ** (-alpha + 1)
            ax2.loglog(x_line, y_line, 'r--', linewidth=2, label=f'Power Law (α={alpha:.3f})')
            ax2.set_xlabel('Rank')
            ax2.set_ylabel('Frequency')
            ax2.set_title('Power Law Fit (log-log scale)')
            ax2.legend()
            ax2.grid(True, alpha=0.3, which='both')
            
            st.pyplot(fig)
            plt.close()
        
        # Tab 3: Frequency Table
        with tab3:
            st.subheader("Frequency Table")
            st.dataframe(FrequencyTable, use_container_width=True)
        
        # Tab 4: Downloads
        with tab4:
            st.subheader("📥 Download Data")
            
            col1, col2 = st.columns(2)
            
            # Download FrequencyTable as CSV
            with col1:
                # Create display version of FTable with mapped options
                ftable_display = FTable.copy()
                if option_labels and has_custom_options:
                    ftable_display['State'] = ftable_display['State'].apply(
                        lambda x: option_labels[x] if x < len(option_labels) and option_labels[x] else str(x)
                    )
                
                freq_csv = ftable_display.to_csv(index=False)
                st.download_button(
                    label="📊 Download Frequency Table (CSV)",
                    data=freq_csv,
                    file_name=f"frequency_table_{episode_length}_{episode_options}.csv",
                    mime="text/csv"
                )
            
            # Download Stream as CSV
            with col2:
                stream_df = pd.DataFrame(Stream)
                stream_csv = stream_df.to_csv(index=False, header=False)
                st.download_button(
                    label="📊 Download Stream Data (CSV)",
                    data=stream_csv,
                    file_name=f"stream_{episode_length}_{episode_options}.csv",
                    mime="text/csv"
                )
            
            # Download Stream by Ranked Order
            st.markdown("**Stream by Ranked Order:**")
            
            col3, col4 = st.columns(2)
            
            with col3:
                # Create stream data ranked by state (option) order
                stream_ranked_by_item = []
                for row_idx in range(StreamRanked.shape[0]):
                    row = StreamRanked[row_idx, :]
                    selected_items = [int(x) for x in row if x != 0]
                    
                    if option_labels and has_custom_options:
                        # Use The Options labels
                        selected_labels = [
                            option_labels[item] if item < len(option_labels) and option_labels[item] else str(item)
                            for item in selected_items
                        ]
                        stream_ranked_by_item.append(selected_labels)
                    else:
                        # Use numeric values
                        stream_ranked_by_item.append(selected_items)
                
                # Convert to CSV
                stream_ranked_csv = ""
                for row in stream_ranked_by_item:
                    stream_ranked_csv += ",".join(str(x) for x in row) + "\n"
                
                st.download_button(
                    label="📊 Download Stream by Ranked Order (CSV)",
                    data=stream_ranked_csv,
                    file_name=f"stream_ranked_{episode_length}_{episode_options}.csv",
                    mime="text/csv"
                )
            
            # Show preview
            with col4:
                st.markdown("**Preview:**")
                preview_rows = 5
                preview_text = "First " + str(preview_rows) + " rows of ranked stream:\n\n"
                for i, row in enumerate(stream_ranked_by_item[:preview_rows]):
                    preview_text += f"Time {i+1}: " + ", ".join(str(x) for x in row) + "\n"
                st.code(preview_text, language="text")


# Initial state message
else:
    st.info(
        "👈 **Configure the episode parameters** in the left sidebar and click **'Generate Analysis'** to get started!"
    )
    
    st.markdown("""
    ### Features:
    - 🎛️ **Customizable Parameters**: Adjust episode length, number of options, selection probability
    - 🏷️ **Custom Options (Optional)**: Specify custom labels for items and choose ranked or random mapping
    - 📊 **Three Visualizations**: Distribution bar graph, spike train, and network graph with enhanced node labels
    - 📈 **Power Law Analysis**: View detailed power law fit with log-log plots
    - 📥 **Data Export**: Download frequency tables, raw stream, and ranked stream data as CSV files
    - 📋 **Key Metrics**: Clustering coefficient, average shortest path, and power law exponent
    
    ### Parameters Explained:
    - **Episode Length**: Number of time steps in the stream
    - **Options to Select**: How many items are selected at each time step
    - **Episode Options**: Total universe of possible items
    - **Selection Probability**: Probability of selecting preferred items (higher = more skewed distribution)
    
    ### The Options (Optional):
    - **Custom Labels**: Provide string labels for each item (e.g., "Apple", "Banana", "Cherry")
    - **Order Type**:
      - **Random** (default): Randomly maps numeric states to your labels
      - **Ranked**: Sequentially maps states to labels in the order you provided
    - **Auto Display**: If you don't provide labels, numeric values (1 to Episode Options) are used automatically
    
    ### How The Options Are Used:
    - Frequency table states are replaced with your labels
    - Network graph nodes are labeled with your options
    - Stream downloads include your custom labels
    """)
