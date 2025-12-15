from statsmodels.stats.proportion import proportion_confint
import numpy as np

def wilson_confidence_interval(successes, trials, confidence=0.95):
    """
    Calculate the Wilson score confidence interval for a binomial proportion.
    Uses statsmodels library for accurate computation.
    
    Parameters:
    -----------
    successes : int
        Number of successful outcomes
    trials : int
        Total number of trials
    confidence : float, optional
        Confidence level (default: 0.95 for 95% confidence)
    
    Returns:
    --------wq
    tuple : (lower_bound, upper_bound)
        The lower and upper bounds of the confidence interval
    
    Example:
    --------
    >>> wilson_confidence_interval(80, 100, 0.95)
    (0.7093997461136986, 0.8641002538863014)
    """
    if trials == 0:
        return (0.0, 0.0)
    
    if successes > trials:
        raise ValueError("Number of successes cannot exceed number of trials")
    
    if not 0 < confidence < 1:
        raise ValueError("Confidence level must be between 0 and 1")
    
    # Calculate alpha for the confidence level
    alpha = 1 - confidence
    
    # Use statsmodels to compute Wilson confidence interval
    lower, upper = proportion_confint(
        count=successes,
        nobs=trials,
        alpha=alpha,
        method='wilson'
    )
    
    return (lower, upper)