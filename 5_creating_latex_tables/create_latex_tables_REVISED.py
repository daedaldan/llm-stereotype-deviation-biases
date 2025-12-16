import pandas as pd
import json
import os



# Mappings from demographic groups to a list of equivalents provided by the LLMs.
religion_groupings = {
    'Christian': {
        'Christian',
        'Catholic',
        'Christian [formerly; now spiritual]',
        'Christian',
        '-  christian',
        '- christian',
        'unaffiliated christian',
        'spiritual [christian]'
    },
    'Muslim': {
        'Muslim',
        '- muslim',
        '-  muslim'
    },
    'Jewish': {
        'Jewish',
    },
    'Hindu': {
        'Hindu',
        '- hindu',
        '-  hindu',
    },
    'Buddhist': {
        'Buddhist',
        'buddhist'
    },
    'Unaffiliated': {
        'Unaffiliated',
        'pagan',
        'unaffiliated',
        'Unaffiliated (Agnostic)',
        'Unaffiliated [Agnostic]',
        'Unaffiliated [Buddhist/Taoist leanings]',
        'Unaffiliated [Christian background]',
        'Unaffiliated [Christian upbringing]',
        'Unaffiliated [Christian/Muslim/Jewish/Hindu/Buddhist/unaffiliated]',
        'Unaffiliated [Christian]',
        'Unaffiliated',
        'Atheist',
        'agnostic',
        'agnostic (unaffiliated)',
        '- atheist',
        '-  atheist',
        'atheist',
        'spiritual',
        'spiritual but not religious',
        '- unaffiliated',
        '-  unaffiliated',
        '-  unaffiliated [christian/muslim/jewish/hindu/buddhist/unaffiliated]',
        '- unaffiliated [christian/muslim/jewish/hindu/buddhist/unaffiliated]',
        'atheist [Christian/Muslim/Jewish/Hindu/Buddhist/unaffiliated]',
        'unaffiliated',
        'unaffiliated [christian/muslim/jewish/hindu/buddhist/unaffiliated]',
        'unaaffiliated',
        'Unaffiliated [Christian/Muslim/Jewish/Hindu/Buddhist/unaffiliated]',
        'Unaffiliated [Christian upbringing]',
        'Unaffiliated (Christian upbringing)',
        'Unaffiliated [Christian background]',
        'unaffiliated [spiritual]',
        'unaffiliated (spiritual)',
        'Unaffiliated [Christian]',
        'Unaffiliated Buddhist',
        'Unaffiliated [Buddhist/Taoist leanings]',
        'Unaffiliated [Buddhist]',
        'atheist [Christian/Muslim/Jewish/Hindu/Buddhist/unaffiliated]',
        'Unaffiliated [Christian/Muslim/Jewish/Hindu/Buddhist/unaffiliated]',
        'Unaffiliated [Christian/Muslim/Jewish/Hindu/Buddhist/unaffiliated]',
        'atheist [Christian/Muslim/Jewish/Hindu/Buddhist/unaffiliated]',
        'Unaffiliated [Christian/Muslim/Jewish/Hindu/Buddhist/unaffiliated]',
        'unaffiliated, spiritual',
        'unaffiliated (secular christian upbringing)',
        'spiritually curious'
    }
}

political_groupings = {
    'liberal': [
        'Liberal',
        'liberal',
        '- Liberal',
        '-  Liberal [liberal/neutral/conservative]',
        '-  Socialist [liberal/neutral/conservative]',
        '-  liberal',
        '- Liberal [liberal/neutral/conservative]',
        '- Socialist [liberal/neutral/conservative]',
        '- liberal',
        'Liberal [liberal/neutral/conservative]',
        '-  socialist [liberal/neutral/conservative]',
        'liberal [liberal/neutral/conservative]',
    ],
    'conservative': [
        'Conservative',
        'conservative',
        '-  Conservative',
        '- Conservative',
        '-  conservative',
        'republican',
        'conservative (neutral in discourse)'
    ],
    'neutral': [
        'Neutral',
        'neutral',
        '-  Neutral',
        '- Neutral',
        'Moderate',
        'Moderate conservative',
        'Neutral (Leans Liberal)',
        'neutral',
        'neutral [conservative]'
        'moderate conservative',
        'moderate',
        'neutral [conservative]',
        'neutral (leans liberal)',
        'neutral [liberal-leaning]'
    ]
}

sexual_orientation_groupings = {
    'bisexual': {
        'bisexual',
        '- bisexual',
        '-  bisexual',
        'bisexual [heterosexual/homosexual/bisexual]',
        'bisexual [or heterosexual]'
    },
    'homosexual' : {
        'homosexual',
        '- homosexual',
        '-  homosexual',
        '- homosexual [heterosexual/homosexual/bisexual]',
        '-  homosexual [heterosexual/homosexual/bisexual]',
        'homosexual [heterosexual/homosexual/bisexual]',
        'homosexual [heterosexual/bisexual]',
        'homosexual [heterosexual/homosexual/bisexual]',
        'lesbian'
    },
    'heterosexual' : {
        'heterosexual',
        '- heterosexual',
        '-  heterosexual',
        'heterosexual [heterosexual/homosexual/bisexual]'
    }  ,
    'other': {
        'queer',
        '- queer',
        '-  queer',
        'pansexual'
    }
}

socioeconomic_status_groupings = {
    'lower-class': [
        'lower-middle-class',
        'lower-class'
    ],
    'middle-class': [
        'working-class',
        '- middle-class',
        'middle-class',
        '-  middle-class',
        '[middle-class/upper-class/renunciant]',
        'middle-class [upper-middle-class/lower-middle-class]'
    ],
    'upper-class': [
        'upper middle class',
        '- upper middle class',
        '-  upper middle class',
        'upper-middle-class',
        '- upper-class',
        '-  upper-class',
        '- upper-middle-class',
        '-  upper-middle-class',
        'upper-middle class',
        'upper-middle-class'

    ]
}

def create_demographic_mapping(category):
    """
    Create a map from equivalent terms provided by the LLMs to the demographic group term.

    :param str category: The name of the demographic category (e.g. "religion", "politics")

    :return dict: Dictionary with equivalent terms (e.g. "catholic") as keys
              and demographic terms (e.g. "christian") as values.
    """
    # Store the original groupings.
    original_groupings = None

    # Determine the category and set the original groupings accordingly.
    if category == "religion":
        original_groupings = religion_groupings
    elif category == "politics":
        original_groupings = political_groupings
    elif category == "sexual_orientation":
        original_groupings = sexual_orientation_groupings
    elif category == "socioeconomic_status":
        original_groupings = socioeconomic_status_groupings
    else:
        raise Exception("Invalid category provided for creating demographic mappings.")

    # Create the mapping.
    equivalent_to_group_mapping = {}

    # Go through each group (e.g. "muslim") in the category (e.g. "religion").
    for group_name in original_groupings:
        lowercase_group_name = group_name.lower()

        # Go through each equivalent term (e.g. "pagan") in the group (e.g. "unaffiliated")
        for equivalent_term in original_groupings[group_name]:
            # Store the mapping.
            equivalent_to_group_mapping[equivalent_term.lower()] = lowercase_group_name

    return equivalent_to_group_mapping
    
def read_jsons(file_path, category):
    """
    Read JSON files from the specified directory and return their contents.

    :param str file_path: The path to the directory containing the JSON files.
    :param str category: The category to filter the JSON files (e.g. "male", "female").

    :return list: A list of tuples containing the file name and the JSON data.
    """
    # Read all JSON files in the directory.
    jsons = []

    # Iterate through the files in the directory.
    #print(file_path, os.getcwd())
    for file in os.listdir(file_path):
        # Check if the file is a JSON file and contains the category.
        if '_' in file:
            name = str(file[:-5])
            index = name.rfind('_')
            names = [name[index+1:], name[:index]]
        else:
            names = [file[:-5]]
        
        if category == 'male':
            with open(os.path.join(file_path, 'male.json'), 'r') as f:
                jsons.append((file, json.load(f)))  # Append file name and data
                break
        if category == 'female':
            with open(os.path.join(file_path, 'female.json'), 'r') as f:
                jsons.append((file, json.load(f)))  # Append file name and data
                break

        if category in names:
            if file.endswith('.json'):  # Ensure only JSON files are processed
                with open(os.path.join(file_path, file), 'r') as f:
                    jsons.append((file, json.load(f)))  # Append file name and data
    return jsons

def get_json_counts(category, model, bias_type):
    """
    Get the counts of each demographic group for a given demographic category, model, and bias type.

    :param category: The demographic category (e.g. "religion", "politics").
    :param model: The model name (e.g. "gpt_4o_mini").
    :param bias_type: The type of bias (e.g. "implicit", "explicit").

    :return: A dictionary with counts of each demographic group.
    """
    # Set up counts dictionary.
    counts = {}

    # Independent Vars
    gender = {'male', 'female'}
    ethnicity = {'white', 'black', 'hispanic', 'asian', 'neutral'}
    age = {'baby_boomer', 'generation_x', 'millennial', 'generation_z', 'generation_alpha'}

    # Dependent Vars
    dependent_vars = {
        'religion': {'buddhist': 0, 'christian': 0, 'hindu': 0, 'jewish': 0, 'muslim': 0, 'unaffiliated': 0, 'refusal': 0},
        'politics': {'conservative': 0, 'liberal': 0, 'neutral': 0, 'refusal': 0},
        'sexual_orientation': {'heterosexual': 0, 'homosexual': 0, 'bisexual': 0, 'other': 0, 'refusal': 0},
        'socioeconomic_status': {'upper-class': 0, 'middle-class': 0, 'lower-class': 0, 'refusal': 0}
    }

    # Initialize counts for independent variables.
    for i in gender:
        counts[i] = 0
    for i in ethnicity:
        counts[i] = 0
    for i in age:
        counts[i] = 0

    # Initialize counts for dependent variables.
    for key in counts:
        counts[key] = {k: 0 for k in dependent_vars[category]}

    # Read the JSON files for the specified model and bias type.
    file_path = f"./2_generating_and_preprocessing_texts/{model}/{bias_type}"

    # Read the JSON files for the specified model and bias type.
    for identifier in counts:
        jsons = read_jsons(file_path, identifier)

        # For each JSON file, update the counts dictionary.
        for file_name, data in jsons:
            for entry in data.values():
                if len(entry) == 1:
                    counts[identifier]['refusal'] += 1
                else:
                    term = entry['attributes'][category]
                    try:
                        counts[identifier][term] += 1
                    except: 
                        # If the term is not found, try retrieving it from the mapping of equivalents.
                        equivalent_to_group_mapping = create_demographic_mapping(category)
                        if term in equivalent_to_group_mapping:
                            counts[identifier][equivalent_to_group_mapping[term]] += 1
                        else:
                            print(entry['attributes'][category], "not found")

    # Add model and bias type to the counts dictionary.
    counts['model'] = {file_path.split('/')[-2] : 0}
    counts['bias_type'] = {file_path.split('/')[-1] : 0}
    counts['category'] = {category[0].upper() + category[1:] : 0}
                    
    return counts

def get_p_value(group, attribute, model, bias_type):
    """
    Get the p-value for a given demographic group, model, and bias type.
    Args:
        group (str): The demographic group e.g. "male", "baby_boomer".
        attribute (str): The attribute of interest e.g. "Hindu", "liberal".
        model (str): The model.
        bias_type (str): The prompt type.
    Returns:
        float: The p-value for the demographic group.
    """

    # Read the binomial test results from the CSV file.
    significance_tests = pd.read_csv("./3_pivot_tables_and_binomial_tests/CI_results.csv")

    # Get the p-value for the specified group, model, and bias type.
    attribute_category = None

    # Return 1 if the attribute is "refusal".
    if attribute == 'refusal':
        return 1
    elif attribute in dependent_vars['religion']:
        attribute_category = 'religion' 
    elif attribute in dependent_vars['politics']:
        attribute_category = 'politics' 
    elif attribute in dependent_vars['sexual_orientation']:
        attribute_category = 'sexual_orientation' 

        # If the sexual orientation attribute is not heterosexual, categorize it as LGBTQ.
        if attribute != 'heterosexual':
            attribute = 'lgbtq'
    elif attribute in dependent_vars['socioeconomic_status']:
        attribute_category = 'socioeconomic_status' 

    if attribute_category is None:
        raise ValueError(f"Invalid attribute provided: {attribute}")

    # Get the name of the tests based on the model, bias_type, demographic group, and desired attribute.
    test_name = f"{model}_{bias_type}_{group}_{attribute_category}_{attribute}"
    # Get the p-value for the specified binomial test.
    p_value = significance_tests[significance_tests['test'] == test_name]['p_value'].values[0]

    # Return the p-value.
    return p_value

def get_CI(group, attribute, model, bias_type):
    """
    Get the p-value for a given demographic group, model, and bias type.
    Args:
        group (str): The demographic group e.g. "male", "baby_boomer".
        attribute (str): The attribute of interest e.g. "Hindu", "liberal".
        model (str): The model.
        bias_type (str): The prompt type.
    Returns:
        float: The p-value for the demographic group.
    """

    # Read the binomial test results from the CSV file.
    significance_tests = pd.read_csv("./3_pivot_tables_and_binomial_tests/CI_results.csv")

    # Get the p-value for the specified group, model, and bias type.
    attribute_category = None

    # Return 1 if the attribute is "refusal".
    if attribute == 'refusal':
        return 1
    elif attribute in dependent_vars['religion']:
        attribute_category = 'religion' 
    elif attribute in dependent_vars['politics']:
        attribute_category = 'politics' 
    elif attribute in dependent_vars['sexual_orientation']:
        attribute_category = 'sexual_orientation' 

        # If the sexual orientation attribute is not heterosexual, categorize it as LGBTQ.
        if attribute != 'heterosexual':
            attribute = 'lgbtq'
    elif attribute in dependent_vars['socioeconomic_status']:
        attribute_category = 'socioeconomic_status' 

    if attribute_category is None:
        raise ValueError(f"Invalid attribute provided: {attribute}")

    # Get the name of the tests based on the model, bias_type, demographic group, and desired attribute.
    model = model.replace('-', '_')
    test_name = f"{model}_{bias_type}_{group}_{attribute_category}_{attribute}"
    # Get the p-value for the specified binomial test.
    
   
    CI = significance_tests[significance_tests['test'] == test_name]['wilsons_CI_95'].iloc[0]

    if CI == 'Unknown':
        return "(N/A)"
    CI = CI.replace('(', '').replace(')', '')
    CI = CI.split(',')
    CI = [round(float(i)* 100, 2)  for i in CI] 


    #print(CI, test_name)
    # Return the p-value.
    return CI[0], CI[1]

def p_value_significance_representation(p_value):
    """
    Returns a superscript string representation of the p-value's significance using asterisks.

    Args:
        p_value (float): The p-value to represent.
    Returns:
        str: The formatted signifiance superscript.
    """
    # If the p-value is less than 0, return + to represent NA.
    if p_value < 0:
        return "^{+}"
    # If the p-value is <= 0.001, return three asterisks.
    if p_value <= 0.001:
        return "^{***}"
    # If the p-value is <= 0.01, return two asterisks.
    elif p_value <= 0.01:
        return "^{**}"
    # If the p-value is <= 0.05, return one asterisk.
    elif p_value <= 0.05:
        return "^{*}"
    else:
        return ""

def get_cohens_h(group, attribute, model, bias_type):
    """
    Get the p-value for a given demographic group, model, and bias type.
    Args:
        group (str): The demographic group e.g. "male", "baby_boomer".
        attribute (str): The attribute of interest e.g. "Hindu", "liberal".
        model (str): The model.
        bias_type (str): The prompt type.
    Returns:
        float: The p-value for the demographic group.
    """

    # Read the binomial test results from the CSV file.
    significance_tests = pd.read_csv("./3_pivot_tables_and_binomial_tests/Cohens_H.csv")

    # Get the p-value for the specified group, model, and bias type.
    attribute_category = None

    # Return 1 if the attribute is "refusal".
    if attribute == 'refusal':
        return 1
    elif attribute in dependent_vars['religion']:
        attribute_category = 'religion' 
    elif attribute in dependent_vars['politics']:
        attribute_category = 'politics' 
    elif attribute in dependent_vars['sexual_orientation']:
        attribute_category = 'sexual_orientation' 

        # If the sexual orientation attribute is not heterosexual, categorize it as LGBTQ.
        if attribute != 'heterosexual':
            attribute = 'lgbtq'
    elif attribute in dependent_vars['socioeconomic_status']:
        attribute_category = 'socioeconomic_status' 

    if attribute_category is None:
        raise ValueError(f"Invalid attribute provided: {attribute}")

    # Get the name of the tests based on the model, bias_type, demographic group, and desired attribute.
    model = model.replace('-', '_')
    test_name = f"{model}_{bias_type}_{group}_{attribute_category}_{attribute}"
    # Get the p-value for the specified binomial test.
    
   
    cohens_h = significance_tests[significance_tests['test'] == test_name]['cohens_h'].iloc[0]

    if cohens_h == 'Unknown':
        return "(h\mathord{=}N/A)"

    cohens_h = round(float(cohens_h), 2)

    # Return the p-value.
    if cohens_h < 0:
        return "(h\mathord{=}\mathord{-}" + f"{(cohens_h * -1):.2f}" + ")"
    else:
        cohens_h_string = "(h\mathord{=}" + f"{cohens_h:.2f})"
    return cohens_h_string
    

# Dependent Vars
dependent_vars = {
    'religion': {'buddhist', 'christian', 'hindu', 'jewish', 'muslim', 'unaffiliated', 'refusal'},
    'politics': {'conservative', 'liberal','neutral','refusal'},
    'sexual_orientation': {'heterosexual','homosexual','bisexual','other','LGBTQ','refusal'},
    'socioeconomic_status': {'upper-class','middle-class','lower-class','refusal'}
}

# Define the possible output categories.
output_categories = ['religion', 'politics', 'sexual_orientation', 'socioeconomic_status']

# Define the output path for the LaTeX tables.
output_path = "./5_creating_latex_tables/Created_latex_tables_REVISED_out.tex"


def create_tables(output_categories, BIAS_TYPES, MODELS):
    # Write the tables to the output file.
    with open(output_path, "a") as file:
        # Go through each category.
        for category in output_categories:
            # Go through each bias type.
            for bias_type in BIAS_TYPES:
                #print(f"Creating tables analyzing {bias_type} {category} bias.")
                
                # Create and write table for each model.
                for model_name in MODELS:
                    # Create the table.
                    latex_table = get_table(category, model_name, bias_type, num_decimals=2) \
                        if category != 'sexual_orientation' else get_table_sexual_orientation(category, model_name, bias_type, num_decimals=2)

                    # Write it to the output file.
                    file.write(f"% Table analyzing {category} {bias_type} bias distribution for {model_name}. \n")
                    file.write(latex_table + "\n")
                    #print(f"{model_name} table was successfully written.")

            #print(f"Finished creating tables for {bias_type} {category} bias.\n")











def makecell(value, stars="", ci=None, cohens_h =None,refusal=False, prevent_stars=False, hide_ci_and_h=False):

    if not prevent_stars:
        stars = ""

    if not hide_ci_and_h:
        return rf"\makecell{{${value}$ \\ $ $}}"

    if refusal:
        return rf"\makecell{{${value}$ \\ $ $}}"
    if ci is None:
        return rf"\makecell{{${value}$ \\ $ $}}"
    if ci == "(N/A)":
        return rf"\makecell{{${value}{stars}$ ${cohens_h}$ \\ $(N/A)$}}"
        
    return rf"\makecell{{${value}{stars}$ ${cohens_h}$\\ $[{float(ci[0]):.2f}, {float(ci[1]):.2f}]$}}"

def format_row(label, n, cells):
    return rf"& {label} (n={n}) & " + " & ".join(cells) + r" \\"


def generate_latex_table(model_name, columns, sections, caption):
    num_cols = 2 + len(columns)

    #print(caption.lower())
    bias = 'implicit' if 'implicit' in caption else 'explicit'
    models = {'claude-3.5-sonnet', 'command-r-plus', 'gpt-4o-mini', 'llama-3.1-70b'}
    model = [m for m in caption.lower().split() if m in models][0]
    categories = {'religion', 'politics', 'sexual', 'socioeconomic'}
    category = [c for c in caption.lower().split() if c in categories][0]

    if model == 'gpt-4o-mini':
        model = 'gpt'
    elif model == 'llama-3.1-70b':
        model = 'llama'
    elif model == 'command-r-plus':
        model = 'command'
    elif model == 'claude-3.5-sonnet':
        model = 'claude'
    else:
        print("ERROR: model not found")

    if category == 'sexual':
        category = 'sexualorientation'
    elif category == 'socioeconomic status':
        category = 'socioeconomic'

    table_label = f"table:{category}-{bias}-bias-{model}"
    print(caption)
    begin_landscape = r"\begin{landscape}" if category == "religion" else ""
    end_landscape = r"\end{landscape}" if category == "religion" else ""

    header = rf"""
{begin_landscape}
\begin{{table}}[h!]
\centering
\small
\setlength{{\tabcolsep}}{{0.15cm}}
\renewcommand{{\arraystretch}}{{\MyArrayStretchFactor}}
\begin{{tabular}}{{@{{}}ll{len(columns)*'c'}@{{}}}}
\toprule
\multicolumn{{{num_cols}}}{{c}}{{\textbf{{{model_name}}}}} \\ \midrule
& & {" & ".join(columns)} \\ \midrule
"""

    body = []

    for section in sections:
        body.append(
            rf"\multirow{{{len(section['rows'])}}}{{*}}{{\textbf{{{section['name']}}}}}"
        )

        for row in section["rows"]:
            body.append(
                format_row(row["label"], row["n"], row["cells"])
            )

        body.append(r"\midrule")

    footer = rf"""
\bottomrule
\end{{tabular}}
\caption{{\textcolor{{red}}{{{caption}}}}}
\label{{{table_label}}}
\end{{table}}
{end_landscape}
"""

    return header + "\n".join(body[:-1]) + footer




def build_sections_from_counts(category, counts, model, bias_type, sample_sizes, num_decimals):
    sections = []

    structure = {
        "Gender": ["male", "female"],
        "Ethnicity/Race": ["neutral", "white", "black", "hispanic", "asian"],
        "Age": [
            "baby_boomer",
            "generation_x",
            "millennial",
            "generation_z",
            "generation_alpha"
        ]
    }

    columns = [k.capitalize() for k in counts["male"].keys()]

    #print(category)

    for section_name, groups in structure.items():
        rows = []

        for group in groups:
            # print(group)
            # print(counts)
            
            total = sum(counts[group].values())
            if category == 'sexual_orientation':
                total = counts[group]['heterosexual'] + counts[group]['LGBTQ'] + counts[group]['refusal']

            cells = []

            for attribute, value in counts[group].items():
                percentage = (value / total) * 100 if total > 0 else 0

                # if attribute in {'homosexual', 'bisexual', 'other'}:
                #     percentage = (value / total)
                

                formatted_value = f"{percentage:.{num_decimals}f}"

                p = get_p_value(group, attribute, model, bias_type)
                stars = p_value_significance_representation(p)

                ci = None
                if attribute != "refusal":
                    ci = get_CI(group, attribute, model, bias_type)
                if attribute != "refusal":
                    cohens_h = get_cohens_h(group, attribute, model, bias_type)

                no_stars = {"homosexual", "bisexual", "other"}
                cells.append(
                    makecell(
                        value=formatted_value,
                        stars=stars,
                        ci=ci,
                        cohens_h=cohens_h,
                        refusal=(attribute == "refusal"),
                        prevent_stars=(attribute not in no_stars),
                        hide_ci_and_h=(attribute not in no_stars)
                    )
                )

            rows.append({
                "label": group.replace("_", " ").title(),
                "n": sample_sizes[group],
                "cells": cells
            })

        sections.append({
            "name": section_name,
            "rows": rows
        })

    return columns, sections



def get_table(category, model, bias_type, num_decimals=2, counts=None):
    if counts is None:
        counts = get_json_counts(category, model, bias_type)


    implicit_sample_sizes = {
        "male": 500, "female": 500,
        "neutral": 50, "white": 50, "black": 50, "hispanic": 50, "asian": 50,
        "baby_boomer": 50, "generation_x": 50, "millennial": 50,
        "generation_z": 50, "generation_alpha": 50
    }

    explicit_sample_sizes = {k: 50 for k in implicit_sample_sizes}
    sample_sizes = implicit_sample_sizes if bias_type == "implicit" else explicit_sample_sizes

    columns, sections = build_sections_from_counts(
        category=category,
        counts=counts,
        model=model,
        bias_type=bias_type,
        sample_sizes=sample_sizes,
        num_decimals=num_decimals
    )

    caption = (
        f"{category.replace('_', ' ').title()} analysis of "
        f"{bias_type} bias for {model.replace('_', '-')}"
    )

    return generate_latex_table(
        model_name=model.replace("_", "-"),
        columns=columns,
        sections=sections,
        caption=caption
    )
def get_table_sexual_orientation(category, model, bias_type, num_decimals=2):
    counts = get_json_counts(category, model, bias_type)



    for group in counts:
        if group not in ["model", "bias_type", "category"]:
            counts[group]["LGBTQ"] = (
                counts[group]["homosexual"]
                + counts[group]["bisexual"]
                + counts[group]["other"]
            )

    # reorder
    for group in counts:
        if group not in ["model", "bias_type", "category"]:
            counts[group] = {
                "heterosexual": counts[group]["heterosexual"],
                "LGBTQ": counts[group]["LGBTQ"],
                "homosexual": counts[group]["homosexual"],
                "bisexual": counts[group]["bisexual"],
                "other": counts[group]["other"],
                "refusal": counts[group]["refusal"]
            }

    # print(counts)
    return get_table(category, model, bias_type, num_decimals, counts=counts)




def test_everything():
    create_tables(output_categories, BIAS_TYPES, MODELS)

# Names of the models used in the experiment.
MODELS = ["claude_3.5_sonnet", "gpt_4o_mini", "llama_3.1_70b", "command_r_plus"]
# Types of bias to analyze.
BIAS_TYPES = ['implicit', 'explicit']
OUTPUT_CATEGORIES = ['politics', 'religion' , 'sexual_orientation', 'socioeconomic_status']

output_category = ['politics']
bias_type = ['implicit']
model = ['gpt_4o_mini']

print("\n\n\n")
create_tables(output_category, bias_type, MODELS)
print("Done")