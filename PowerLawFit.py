import numpy as np
from scipy.optimize import minimize
from scipy.special import digamma


def compute_alpha_mle(frequencies):
    """
    Fit a power law distribution to frequency data using Maximum Likelihood Estimation (MLE).
    
    The power law PDF is: P(x) = (alpha - 1) * x_min^(alpha - 1) / x^alpha
    For a discrete distribution: log(L) = n * log(alpha - 1) + n * (alpha - 1) * log(x_min) - alpha * sum(log(x_i))
    
    Parameters:
    -----------
    frequencies : ndarray
        Array of frequency values (must be > 0)
    
    Returns:
    --------
    alpha : float
        Estimated power law exponent
    """
    
    # Remove zero frequencies and ensure we have positive values
    freqs = frequencies[frequencies > 0]
    
    if len(freqs) == 0:
        return np.nan
    
    # For power law distribution, the MLE estimator is:
    # alpha = 1 + n / sum(log(x_i / x_min))
    # where x_min is the minimum value
    
    x_min = np.min(freqs)
    n = len(freqs)
    
    # Compute the sum of logarithms
    log_sum = np.sum(np.log(freqs / x_min))
    
    if log_sum <= 0:
        return 1.1  # Return a default value close to 1 if sum is non-positive
    
    alpha = 1 + n / log_sum
    
    # Ensure alpha is reasonable (typically > 1 for a valid power law)
    if alpha < 1.01:
        alpha = 1.01
    
    return alpha


def compute_alpha_mle_alternative(frequencies):
    """
    Alternative MLE method using continuous power law approximation.
    Uses numerical optimization to find the alpha that maximizes the likelihood.
    
    Parameters:
    -----------
    frequencies : ndarray
        Array of frequency values (must be > 0)
    
    Returns:
    --------
    alpha : float
        Estimated power law exponent
    """
    
    # Remove zero frequencies
    freqs = frequencies[frequencies > 0]
    
    if len(freqs) == 0:
        return np.nan
    
    x_min = np.min(freqs)
    n = len(freqs)
    
    # Negative log-likelihood for power law: -log(L) = -n*log(alpha-1) - n*(alpha-1)*log(x_min) + alpha*sum(log(x_i))
    def neg_log_likelihood(alpha):
        if alpha <= 1:
            return 1e10  # Large penalty for invalid alpha
        log_norm = np.log(alpha - 1) + (alpha - 1) * np.log(x_min)
        log_like = n * log_norm - alpha * np.sum(np.log(freqs))
        return -log_like
    
    # Optimize to find the best alpha
    result = minimize(neg_log_likelihood, x0=2.0, method='Nelder-Mead')
    alpha = result.x[0]
    
    # Ensure alpha is reasonable
    if alpha < 1.01:
        alpha = 1.01
    
    return alpha
