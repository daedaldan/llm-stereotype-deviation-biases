"""
Calculate Cohen's h effect size for comparing two proportions.
Cohen's h measures the distance between two proportions using arcsin transformation.
"""

from statsmodels.stats.proportion import proportion_effectsize
import numpy as np

def cohens_h_statsmodels(p1, p2):
    """
    Calculate Cohen's h using statsmodels.
    
    Parameters:
    -----------
    p1 : float
        First proportion (between 0 and 1) (the observed percentages in our experiment)
    p2 : float
        Second proportion (between 0 and 1) (the reference percentages in our experiment)
    
    Returns:
    --------
    float : Cohen's h effect size
        if positive, that means the observed percentage is greater than the reference percentage
        if negative, that means the observed percentage is less than the reference percentage
    """
    return proportion_effectsize(p1, p2)

def interpret_cohens_h(h):
    """
    Interpret Cohen's h effect size.
    
    Cohen's conventions: link --> https://resources.nu.edu/statsresources/cohensd
    - Small effect: |h| = 0.2
    - Medium effect: |h| = 0.5
    - Large effect: |h| = 0.8
    """
    abs_h = abs(h)
    if abs_h < 0.2:
        return "negligible"
    elif abs_h < 0.5:
        return "small"
    elif abs_h < 0.8:
        return "medium"
    else:
        return "large"
    
