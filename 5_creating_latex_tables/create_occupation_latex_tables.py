import pandas as pd
import json

# Independent Variables
MODELS = ["claude_3.5_sonnet", "gpt_4o_mini", "llama_3.1_70b", "command_r_plus"]
GENDERS = ['male', 'female']
ETHNICITIES = ['white', 'black', 'hispanic', 'asian', 'neutral']
AGE_GROUPS = ['baby_boomer', 'generation_x', 'millennial', 'generation_z', 'generation_alpha']
BIAS_TYPES = ['implicit', 'explicit']

# Dependent Variables
attributes = ["occupation", "socioeconomic_status", "religion", "politics", "sexual_orientation", "total_height", "polarity", "subjectivity"]

def get_occupation_percentages(group, model, bias_type):
    """
    Get the percentage of each occupation for a given demographic group, model, and bias type.

    :param group: The demographic group.
    :param model: The model.
    :param bias_type: The bias type.

    :return: The percentage of each occupation.
    """
    # If the group is male or female, directly load the data from the JSON file.
    if group in ["male", "female"]:
        with open(f"../2_generating_and_preprocessing_texts/{model}/{bias_type}/{group}.json") as f:
            texts = json.load(f)

    # If the group is not male or female, combine the male and female JSONs.
    else:
        with open(f"../2_generating_and_preprocessing_texts/{model}/{bias_type}/{group}_male.json") as f:
            male_texts = json.load(f)
        with open(f"../2_generating_and_preprocessing_texts/{model}/{bias_type}/{group}_female.json") as f:
            female_texts = json.load(f)

        # Combine the two dictionaries.
        texts = {**male_texts, **female_texts}

    # Create a dictionary to store the texts with the attribute data on the same level.
    texts_with_attributes = {}

    # Go through each text.
    for text_key in texts.keys():
        # print("Text key: ", text_key)
        # Create a new dictionary for the text.
        texts_with_attributes[text_key] = {}

        # Add the text to the new dictionary.
        texts_with_attributes[text_key]["generated_text"] = texts[text_key]["generated_text"]

        # Check if the text is missing attributes i.e. a refusal occurred.
        if "attributes" not in texts[text_key].keys():
            # If so, add a placeholder for each key.
            for attribute in attributes:
                texts_with_attributes[text_key][attribute] = "refusal"

            # Skip to the next text.
            continue

        # Add the attributes to the new dictionary.
        for attribute_key in texts[text_key]["attributes"].keys():
            texts_with_attributes[text_key][attribute_key] = texts[text_key]["attributes"][attribute_key]

    # Create a DataFrame from the data.
    group_df = pd.DataFrame(texts_with_attributes)

    # Transpose the DataFrame.
    group_df = group_df.T

    # Remove any additional formatting from the occupation value.
    group_df['occupation'] = group_df['occupation'].apply(lambda occupation : occupation.replace("-", "").strip())

    # Get the number of unique occupations.
    num_occupations = group_df['occupation'].nunique()

    # Print the unique occupations.
    # print(f"Unique occupations: {group_df['occupation'].unique()}")

    # Get the relative percentage of each occupation.
    occupation_percentages = group_df['occupation'].value_counts(normalize=True)

    # If there are more than 5 occupations, only consider the top 5.
    if num_occupations > 5:
       occupation_percentages = occupation_percentages.head(5)

    # Convert the decimals to percentages with four decimal places.
    occupation_percentages = occupation_percentages.apply(lambda percent : round(percent * 100, 4))

    # Convert the percentages to a dictionary.
    occupation_percentages = dict(occupation_percentages)

    occupation_percentages_str = ""

    # Go through each occupation.
    for occupation in occupation_percentages.keys():
        occupation_percentages_str += f"{occupation} ({occupation_percentages[occupation]}\%), "

    return occupation_percentages_str.strip(", ")

def get_table(title, model, bias_type):
    """
    Create the LaTeX table for the given model and bias type.

    :param model: The model.
    :param bias_type: The bias type.

    :return: The LaTeX table.
    """
    occupation_percentages = {}

    # Get the occupation percentages for each gender.
    for gender in GENDERS:
        occupation_percentages[gender] = get_occupation_percentages(gender, model, bias_type)

    # Get the occupation percentages for each ethnicity.
    for ethnicity in ETHNICITIES:
        occupation_percentages[ethnicity] = get_occupation_percentages(ethnicity, model, bias_type)

    # Get the occupation percentages for each age group.
    for age_group in AGE_GROUPS:
        occupation_percentages[age_group] = get_occupation_percentages(age_group, model, bias_type)
    
    # Initialize the LaTeX table string.
    table = f"\\begin{{table}}[h!]\n\\centering\n\\small\n\\renewcommand{{\\arraystretch}}{{1.0}}\n\\begin{{tabular}}{{@{{}}l p{{1.7cm}} p{{12cm}} ccccccc@{{}}}}\n\\toprule\n"
    table += f"\\multicolumn{{3}}{{c}}{{\\textbf{{{model.replace('_', '-')}}}}} & \\\\ \\midrule\n"
    table += "& & Most Popular Occupations \\\\ \\midrule\n"
    
    # Gender
    table += "\\multirow{2}{*}{\\textbf{Gender}} \n"
    for gender in ['male', 'female']:
        table += f"& {gender.title()} & {occupation_percentages[gender]} \\\\ \n"
    table += "\\midrule\n"
    
    # Ethnicity/Race
    table += "\\multirow{5}{*}{\\textbf{Ethnicity/Race}} \n"
    for ethnicity in ['neutral', 'white', 'black', 'hispanic', 'asian']:
        table += f"& {ethnicity.title()} & {occupation_percentages[ethnicity]} \\\\ \n"
    table += "\\midrule\n"
    
    # Age
    table += "\\multirow{5}{*}{\\textbf{Age}} \n"
    for age in ['baby_boomer', 'generation_x', 'millennial', 'generation_z', 'generation_alpha']:
        table += f"& {age.replace('_', ' ').title()} & {occupation_percentages[age]} \\\\ \n"

    table += "\\bottomrule\n\\end{tabular}\n\\caption{" + title + "}\n\\end{table}\n"

    table +="\n\n"

    return table

# Define the output path for the LaTeX tables.
output_path = "occupation_stats_latex_table.tex"

# Write the tables to the output file.
with open(output_path, "a") as file:
    # Go through each bias type.
    for bias_type in BIAS_TYPES:
        print(f"Creating tables analyzing {bias_type} occupation bias.")

        # Go through each model.
        for model_name in MODELS:
            latex_table = get_table(
                f"Table analyzing {bias_type} occupation bias statistics for {model_name.replace('_', '-')}.",
                model_name,
                bias_type
            )

            # Write the table to the output file.
            file.write(f"% Table analyzing occupation {bias_type} bias statistics for {model_name}." + "\n")
            file.write(latex_table)
            print(f"{model_name} table was successfully written.")

        print(f"Finished creating tables for {bias_type} bias.\n")