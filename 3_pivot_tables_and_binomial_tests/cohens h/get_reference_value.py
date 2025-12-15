import pandas as pd
import os


def get_reference_value(row):
    """
    This function takes a row of a DataFrame and returns the corresponding reference value from the CSV files in the reference_values directory.
    Reference values are the percentages of groups from real world data (example: 67% of males are christians).

    Parameters:
    row (pandas.Series): A row of a DataFrame, containing the input attribute category, output attribute category, input attribute, and output attribute.
    
    Returns:
    str: The reference value from the CSV files, or "No reference value found" if the value is not found.
    """
    input_attribute_category = row['input_attribute_category'].lower()
    output_attribute_category = row['output_attribute_category'].lower()
    input_attribute = row['input_attribute'].lower()
    output_attribute = row['output_attribute'].lower()
    

    #print(input_attribute_category, output_attribute_category, input_attribute, output_attribute)
    df = pd.read_csv(f'./3_pivot_tables_and_binomial_tests/reference_values/{output_attribute}_by_{input_attribute}.csv', index_col=0)
    df.columns = df.columns.str.lower()
    df.index = df.index.str.lower()

    if 'homosexual' in df.columns and 'bisexual' in df.columns:
        df['lgbt'] = df['homosexual'] + df['bisexual']
    if output_attribute_category == 'lgbtq':
        output_attribute_category = 'lgbt'
    if input_attribute_category == 'millennial':
        input_attribute_category = 'millennials'
    
    if input_attribute_category == 'baby_boomer':
        input_attribute_category = 'baby boomers'

    if '_' in input_attribute_category:
        input_attribute_category = input_attribute_category.replace('_', ' ')

    #print(df.loc[input_attribute_category, output_attribute_category], row['test'])

    # if pd.isnull(df.loc[input_attribute_category, output_attribute_category]):
            
    #     # Add debugging before the return:
    #     print(f"Looking for index: '{input_attribute_category}'")
    #     print(f"Available indices: {df.index.tolist()}")
    #     print(f"Looking for column: '{output_attribute_category}'")
    #     print(f"Available columns: {df.columns.tolist()}")
    #     print(df)
    #     print(f"Returning: {df.loc[input_attribute_category, output_attribute_category]}")
    #     print("\n\n")

    if pd.isnull(df.loc[input_attribute_category, output_attribute_category]):
        return "No reference value found"

    return df.loc[input_attribute_category, output_attribute_category]
