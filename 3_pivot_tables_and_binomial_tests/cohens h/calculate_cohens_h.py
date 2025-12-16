import pandas as pd
import ast
from cohens_h import cohens_h_statsmodels, interpret_cohens_h

df = pd.read_csv('./3_pivot_tables_and_binomial_tests/CI_results.csv')
df['counts'] = df['counts'].apply(ast.literal_eval)


def call_cohens_h(row):

    if row['total_trials'] == 0:
        return 'Unknown'

    if row['reference_value'] == 'No reference value found':
        return 'Unknown'
    
    
    if row['reference_value'] is None:
        return 'Unknown'

    observed_percentage = row['positive_trials'] / row['total_trials']
    reference_percentage = row['reference_value']



    return cohens_h_statsmodels(float(observed_percentage), float(reference_percentage))

df['cohens_h'] = df.apply(call_cohens_h, axis=1)


#print(df)
df.to_csv('./3_pivot_tables_and_binomial_tests/Cohens_H.csv', index=False)
# df.to_csv('./3_pivot_tables_and_binomial_tests/Cohens_H.csv', index=False)