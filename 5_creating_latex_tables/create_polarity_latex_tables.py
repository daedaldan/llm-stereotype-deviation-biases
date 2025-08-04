import numpy as np
import json

# Independent Variables
MODELS = ["claude_3.5_sonnet", "gpt_4o_mini", "llama_3.1_70b", "command_r_plus"]
GENDERS = ['male', 'female']
ETHNICITIES = ['white', 'black', 'hispanic', 'asian', 'neutral']
AGE_GROUPS = ['baby_boomer', 'generation_x', 'millennial', 'generation_z', 'generation_alpha']
BIAS_TYPES = ['implicit', 'explicit']

# Polarity Values  
polarity_values = {}

# Load the data.
# Go through each model.
for model in MODELS:
    # Initialize the polarity dictionaries.
    polarity_values[model] = {}

    implicit_polarity_values = {
        'male': [],
        'female': [],
        'white': [],
        'black': [],
        'hispanic': [],
        'asian': [],
        'neutral': [],
        'baby_boomer': [],
        'generation_x': [],
        'millennial': [],
        'generation_z': [],
        'generation_alpha': []
    }

    explicit_polarity_values = {
        'male': [],
        'female': [],
        'white': [],
        'black': [],
        'hispanic': [],
        'asian': [],
        'neutral': [],
        'baby_boomer': [],
        'generation_x': [],
        'millennial': [],
        'generation_z': [],
        'generation_alpha': []
    }

    # Go through each bias type.
    for bias_type in BIAS_TYPES:
        # Go through each gender.
        for gender in GENDERS:
            # Load the JSON file with the texts.
            with open(f"../2_generating_and_preprocessing_texts/{model}/{bias_type}/{gender}.json") as f:
                data = json.load(f)

                # Iterate through the texts and extract polarity values.
                for text in data.values():
                    if bias_type == 'implicit':
                        try:
                            implicit_polarity_values[gender].append(text['attributes']['polarity'])
                        except:
                            implicit_polarity_values[gender].append(-1)
                    else:
                        try:
                            explicit_polarity_values[gender].append(text['attributes']['polarity'])
                        except:
                            explicit_polarity_values[gender].append(-1)

        # Go through each ethnicity/gender combination.
        for ethnicity in ETHNICITIES:
            for gender in GENDERS:
                # Load the JSON file with the texts.
                with open(f"../2_generating_and_preprocessing_texts/{model}/{bias_type}/{ethnicity}_{gender}.json") as f:
                    data = json.load(f)

                    # Iterate through the texts and extract polarity values.
                    for text in data.values():
                        if bias_type == 'implicit':
                            try:
                                implicit_polarity_values[ethnicity].append(text['attributes']['polarity'])
                            except:
                                implicit_polarity_values[ethnicity].append(-1)
                        else:
                            try:
                                explicit_polarity_values[ethnicity].append(text['attributes']['polarity'])
                            except:
                                explicit_polarity_values[ethnicity].append(-1)

        # Go through each age/gender combination.
        for age in AGE_GROUPS:
            for gender in GENDERS:
                # Load the JSON file with the texts.
                with open(f"../2_generating_and_preprocessing_texts/{model}/{bias_type}/{age}_{gender}.json") as f:
                    data = json.load(f)

                    # Iterate through the texts and extract polarity values.
                    for text in data.values():
                        if bias_type == 'implicit':
                            try:
                                implicit_polarity_values[age].append(text['attributes']['polarity'])
                            except:
                                implicit_polarity_values[age].append(-1)
                        else:
                            try:
                                explicit_polarity_values[age].append(text['attributes']['polarity'])
                            except:
                                explicit_polarity_values[age].append(-1)

    # Store the polarity values for the model.
    polarity_values[model]["implicit"] = implicit_polarity_values
    polarity_values[model]["explicit"] = explicit_polarity_values

def calculate_stats(values):
    """
    Calculate the median, standard deviation, and refusal percentage for a list of values.
    """
    # Filter out refusal values (-1).
    filtered_values = [v for v in values if v != -1]

    # If there are no valid values, return 0 for median and std, and 100% refusal.
    if not filtered_values:
        return 0, 0, 100
    
    # Calculate median, standard deviation, and refusal percentage.
    median = np.median(filtered_values)
    std = np.std(filtered_values)
    refusal_percentage = (len(values) - len(filtered_values)) / len(values) * 100

    return median, std, refusal_percentage

def generate_latex_table(data, title, model, bias_type):
    """
    Generate a LaTeX table from the given data.

    :param data: The data to be included in the table.
    :param title: The title of the table.
    :param model: The model name.
    :param bias_type: The type of bias (implicit or explicit).

    :return: A string containing the LaTeX table.
    """
    # Initialize the LaTeX table string.
    table = f"\\begin{{table}}[h!]\n\\centering\n\\small\n\\renewcommand{{\\arraystretch}}{{1.0}}\n\\begin{{tabular}}{{@{{}}llcccccccc@{{}}}}\n\\toprule\n"
    table += f"\\multicolumn{{5}}{{c}}{{\\textbf{{{model.replace('_', '-')}}}}} & \\\\ \\midrule\n"
    table += "& & Median & Standard Deviation & Refusal \\\\ \\midrule\n"
    
    # Gender
    table += "\\multirow{2}{*}{\\textbf{Gender}} \n"
    for gender in ['male', 'female']:
        median, std, refusal = calculate_stats(data[gender])
        table += f"& {gender.title()} & {median:.2f} & {std:.2f} & {refusal:.2f} \\\\ \n"
    table += "\\midrule\n"
    
    # Ethnicity/Race
    table += "\\multirow{5}{*}{\\textbf{Ethnicity/Race}} \n"
    for ethnicity in ['neutral', 'white', 'black', 'hispanic', 'asian']:
        median, std, refusal = calculate_stats(data[ethnicity])
        table += f"& {ethnicity.title()} & {median:.2f} & {std:.2f} & {refusal:.2f} \\\\ \n"
    table += "\\midrule\n"
    
    # Age
    table += "\\multirow{5}{*}{\\textbf{Age}} \n"
    for age in ['baby_boomer', 'generation_x', 'millennial', 'generation_z', 'generation_alpha']:
        median, std, refusal = calculate_stats(data[age])
        table += f"& {age.replace('_', ' ').title()} & {median:.2f} & {std:.2f} & {refusal:.2f} \\\\ \n"

    table += "\\bottomrule\n\\end{tabular}\n\\caption{" + title + "}\n\\end{table}\n"

    table +="\n\n"

    return table

# Define the output path for the LaTeX tables.
output_path = "polarity_stats_latex_table.tex"

# Write the tables to the output file.
with open(output_path, "a") as file:
    # Go through each bias type.
    for bias_type in BIAS_TYPES:
        print(f"Creating tables analyzing {bias_type} polarity bias.")

        # Go through each model.
        for model_name in MODELS:
            latex_table = generate_latex_table(
                polarity_values[model_name][bias_type],
                f"Table analyzing {bias_type} polarity bias statistics for {model_name.replace('_', '-')}.",
                model_name,
                bias_type
            )

            # Write it to the output file.
            file.write(f"% Table analyzing {bias_type} polarity bias statistics for {model_name.replace('_', '-')}." + "\n")
            file.write(latex_table)
            print(f"{model_name} table was successfully written.")

        print(f"Finished creating tables for {bias_type} bias.\n")