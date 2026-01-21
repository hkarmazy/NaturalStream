import numpy as np


def ModelTimeSeries(SamplingNumber, MaxNumberPossibleStates, SelectedNumber, Handling):
    """
    Generate a time series of selected items based on a behavioral model.
    
    Parameters:
    -----------
    SamplingNumber : int
        Number of time steps to sample
    MaxNumberPossibleStates : int
        Maximum number of possible items
    SelectedNumber : int
        Number of items to select at each time step
    Handling : float
        Probability of selecting items (between 0 and 1)
    
    Returns:
    --------
    selections : ndarray
        Array of shape (SamplingNumber, SelectedNumber) containing selected items
    """
    
    selections = np.zeros((SamplingNumber, SelectedNumber), dtype=int)
    Items = np.arange(1, MaxNumberPossibleStates + 1)
    PreviousEvents = np.zeros(MaxNumberPossibleStates)
    NumberEvents = np.zeros(MaxNumberPossibleStates)
    
    effort = np.ones(MaxNumberPossibleStates) / MaxNumberPossibleStates
    
    for r in range(SamplingNumber):
        # Random selection: either select items or not based on Handling probability
        handelings = np.random.choice([0, 1], p=[1 - Handling, Handling])
        
        if handelings > 0:
            t = r + 1  # Time step (1-indexed)
            c = 10.25
            
            # Update effort for each item based on recency and frequency
            for p in range(len(Items)):
                TheToy = Items[p]
                n = NumberEvents[TheToy - 1]
                const = c - n
                if const < 1.25:
                    const = 1.25
                
                eventT = PreviousEvents[TheToy - 1]
                top = 1.84 * 100
                Log_10 = np.log10(t - eventT) if (t - eventT) > 0 else 0
                buttom = (Log_10 ** const) + 1.84
                Mb = top / buttom
                effort[TheToy - 1] = Mb
            
            # Normalize effort to create a probability distribution
            effort_normalized = effort / np.sum(effort)
            
            # Sample items based on effort probabilities
            selectedToys = np.random.choice(Items, size=handelings, replace=True, p=effort_normalized)
            
            # Record selected items and update tracking
            for k in range(len(selectedToys)):
                selectedToy = selectedToys[k]
                selections[r, k] = selectedToy
                effort[selectedToy - 1] = 100  # Boost effort for selected item
                PreviousEvents[selectedToy - 1] = t
                NumberEvents[selectedToy - 1] += 1
        else:
            # No selection, fill with 0
            selections[r, :] = 0
    
    return selections
