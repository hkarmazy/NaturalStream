import numpy as np
import pandas as pd


def Ranking(Stream):
    """
    Rank items in the stream based on their frequency and generate frequency table.
    
    Parameters:
    -----------
    Stream : ndarray
        Array of items selected over time
    
    Returns:
    --------
    StreamRanked : ndarray
        Stream with item ranks instead of original values
    FrequencyTable : DataFrame
        Table containing frequency information for each item
    """
    
    numRows, numCols = Stream.shape
    x = Stream
    
    # Find unique items (excluding 0)
    u = np.unique(x)
    u = u[u != 0]
    
    B = []
    for i in range(len(u)):
        item = u[i]
        # Find all rows where this item appears
        rows = np.where(x == item)
        # Count unique row indices (how many time steps this item appeared)
        frq = len(np.unique(rows[0]))
        Btable = [item, frq]
        B.append(Btable)
    
    B = np.array(B)
    
    # Sort by frequency (descending)
    B = B[np.argsort(B[:, 1])[::-1]]
    
    # Add rank column
    ranks = np.arange(1, len(B) + 1).reshape(-1, 1)
    B = np.hstack([B, ranks])
    
    # Add proportion column
    props = B[:, 1] / np.sum(B[:, 1])
    B = np.hstack([B, props.reshape(-1, 1)])
    
    # Add subject column (all 1s)
    subs = np.ones((len(B), 1))
    B = np.hstack([B, subs])
    
    # Create frequency table as DataFrame
    FrequencyTable = pd.DataFrame(B, columns=['State', 'Freq', 'rank', 'prop', 'sub'])
    FrequencyTable = FrequencyTable.astype({'State': int, 'Freq': int, 'rank': int})
    
    # Compute cumulative proportions
    cumulative = np.cumsum(FrequencyTable['prop'].values)
    FrequencyTable['cumulative'] = cumulative
    
    # Create ranked stream: replace items with their ranks
    StreamRanked = np.zeros_like(x)
    for r in range(numRows):
        for c in range(numCols):
            item = x[r, c]
            if item > 0:
                # Find the rank of this item
                itemRank = FrequencyTable[FrequencyTable['State'] == item]['rank'].values
                if len(itemRank) > 0:
                    StreamRanked[r, c] = itemRank[0]
    
    return StreamRanked, FrequencyTable
