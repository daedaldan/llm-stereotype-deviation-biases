import pandas as pd
import ast
from wilson_score_interval import wilson_confidence_interval
from get_reference_value import get_reference_value

df = pd.read_csv('./3_pivot_tables_and_binomial_tests/binomial_test_results.csv')

df['counts'] = df['counts'].apply(ast.literal_eval)





def calculate_total_trials(row):  # Renamed from 'sum'
    """Calculate the total number of trials for a given row.

    Parameters
    ----------
    row : pandas Series
        A row containing the counts for a given test.

    Returns
    -------
    int
        The total number of trials.
    """
    counts = row['counts']
    return sum(counts.values())

def calculate_interval(row, confidence=0.95):
    #print(row)
    """Calculate the confidence interval for a given row.

    Parameters
    ----------
    row : pandas Series
        A row containing the counts for a given test.
    confidence : float, optional
        The desired confidence level of the interval. Defaults to 0.95.

    Returns
    -------
    tuple or str
        A tuple containing the lower and upper bounds of the confidence
        interval, or 'Unknown' if the reference percentage is not found.
    """
    if row['reference_percentage'] == 'No reference value found':
        return 'Unknown'
    total_trials = calculate_total_trials(row)
    expected_successes = row['reference_percentage'] * total_trials
    CI = wilson_confidence_interval(float(expected_successes), total_trials, confidence=0.95)
    return CI

def get_model(row):
    """
    Get the model name from a given row.

    Parameters
    ----------
    row : pandas Series
        A row containing the test name.

    Returns
    -------
    str
        The model name.
    """
    name = row['test']
    if "claude_3.5_sonnet" in name:
        return "claude_3.5_sonnet"
    elif "llama_3.1_70b"   in name:
        return "llama_3.1_70b"
    elif "gpt-4o-mini" in name:
        return "gpt-4o-mini"
    elif "command_r_plus" in name:
        return "command_r_plus"
    else:  
        return "unknown"

def get_bias_type(row):
    """
    Get the bias type from a given row.

    Parameters
    ----------
    row : pandas Series
        A row containing the test name.

    Returns
    -------
    str
        The bias type (either "implicit", "explicit", or "unknown").
    """
    name = row['test']
    if "implicit" in name:
        return "implicit"
    elif "explicit" in name:
        return "explicit"
    else:  
        return "unknown"

def outside_CI(row):
    
    """
    Checks if the observed percentage is outside the 95% confidence interval.

    Parameters
    ----------
    row : pandas Series
        A row containing the test name, total trials, positive trials, and the 95% confidence interval.

    Returns
    -------
    bool
        True if the observed percentage is outside the 95% confidence interval, False otherwise.
    """
    if row['wilsons_CI_95'] == 'Unknown':
        return 'Unknown'
    

    CI = row['wilsons_CI_95']
    lower_bound = CI[0]
    upper_bound = CI[1]
    if row['total_trials'] == 0:
        return "Unknown"
    observed_percentage = row['positive_trials'] / row['total_trials']
    return observed_percentage < lower_bound or observed_percentage > upper_bound

df['total_trials'] = df.apply(calculate_total_trials, axis=1)  # Uses renamed function

df['positive_trials'] = df.apply(lambda row: row['counts'][row['output_attribute_category']], axis=1)

df['model'] = df.apply(get_model, axis=1)
df['bias_type'] = df.apply(get_bias_type, axis=1)

df['reference_percentage'] = df.apply(get_reference_value, axis=1)

df['wilsons_CI_95'] = df.apply(calculate_interval, axis=1, confidence=0.95)
df['wilsons_CI_95_lower_bound'] = df['wilsons_CI_95'].apply(lambda x: x[0])
df['wilsons_CI_95_upper_bound'] = df['wilsons_CI_95'].apply(lambda x: x[1])


df['outside_CI'] = df.apply(outside_CI, axis=1)


#print(df.columns)

df = df[[
    'test',
    'model',
    'bias_type',
    'input_attribute_category',
    'output_attribute_category',
    'input_attribute',
    'output_attribute',
    'wilsons_CI_95_lower_bound',
    'wilsons_CI_95_upper_bound',
    'wilsons_CI_95',
    'reference_percentage',
    'p_value',
    'outside_CI',
    'total_trials',
    'positive_trials',
    'counts'
]]

#df.to_csv('./3_pivot_tables_and_binomial_tests/CI_results.csv', index=False)