import numpy as np


def clustering_coef_wu(W):
    """
    Weighted clustering coefficient for undirected weighted graphs.
    
    The weighted clustering coefficient is the average "intensity"
    (geometric mean) of all triangles associated with each node.
    
    Parameters:
    -----------
    W : ndarray
        Weighted undirected connection matrix (all weights between 0 and 1)
    
    Returns:
    --------
    C : ndarray
        Clustering coefficient vector for each node
        
    Reference: Onnela et al. (2005) Phys Rev E 71:065103
    """
    
    # Convert to float to avoid integer division issues
    W = W.astype(float)
    
    # K: number of connections for each node (non-zero weights)
    K = np.sum(W != 0, axis=1)
    
    # Compute the number of triangles: diag((W^(1/3))^3)
    W_cuberoot = np.cbrt(W)
    cyc3 = np.diag(np.linalg.matrix_power(W_cuberoot, 3))
    
    # Handle division by zero: if no 3-cycles exist, set C = 0 by making K = inf
    K = K.astype(float)
    K[cyc3 == 0] = np.inf
    
    # Clustering coefficient: C = cyc3 / (K * (K - 1))
    C = cyc3 / (K * (K - 1))
    
    return C
