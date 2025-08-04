import pandas as pd
import json
import os

# Names of the models used in the experiment.
MODELS = ["claude_3.5_sonnet", "gpt_4o_mini", "llama_3.1_70b", "command_r_plus"]
# Types of bias to analyze.
BIAS_TYPES = ['implicit', 'explicit']

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
    file_path = f"../2_generating_and_preprocessing_texts/{model}/{bias_type}"

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
    binomial_tests_df = pd.read_csv("../3_pivot_tables_and_binomial_tests/binomial_test_results.csv")

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
    p_value = binomial_tests_df[binomial_tests_df['test'] == test_name]['p_value'].values[0]

    # Return the p-value.
    return p_value

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
    
def get_table(category, model, bias_type, as_percentages=False, num_decimals=4):
    """
    Creates a LaTeX table with demographic distribution values for a given demographic category and LLM model.

    Args:
        category (str): The demographic group (e.g., "religion", "politics").
        model (str): The name of the LLM model (e.g., "gpt_4o_mini").
        bias_type (str): Type of bias to analyze ("implicit" or "explicit").
        as_percentages (bool, optional): Whether to display results as percentages. Defaults to False.
        decimal_places (int, optional): Number of decimal places for table values. Defaults to 4.

    Returns:
        str: A LaTeX table string.
    """

    # Get the counts for the specified category, model, and bias type.
    counts = get_json_counts(category, model, bias_type)

    # Get the sample sizes for the specified category, model, and bias type.
    implicit_sample_sizes = {
        "male": 500,
        "female": 500,
        "neutral": 50,
        "white": 50,
        "black": 50,
        "hispanic": 50,
        "asian": 50,
        "baby_boomer": 50,
        "generation_x": 50,
        "millennial": 50,
        "generation_z": 50,
        "generation_alpha": 50,
    }

    explicit_sample_sizes = {
        "male": 50,
        "female": 50,
        "neutral": 50,
        "white": 50,
        "black": 50,
        "hispanic": 50,
        "asian": 50,
        "baby_boomer": 50,
        "generation_x": 50,
        "millennial": 50,
        "generation_z": 50,
        "generation_alpha": 50,
    }

    sample_sizes = implicit_sample_sizes if bias_type == "implicit" else explicit_sample_sizes

    # If as_percentages is False, p-value asterisks are not included.
    table = f"""
        \\begin{{table}}[h!]
        \\centering
        \\small
        \\renewcommand{{\\arraystretch}}{{1.0}}
        \\begin{{tabular}}{{@{{}}llcccccccc@{{}}}}
        \\toprule
        \\multicolumn{{{len(counts['male']) + 2}}}{{c}}{{\\textbf{{{list(counts['model'].keys())[0].replace('_', '-')}}}}} \\\\ \\midrule
        & &  {' & '.join([key[0].upper() + key[1:] for key in counts['male']])} \\\\ \\midrule
        \\multirow{{2}}{{*}}{{\\textbf{{Gender}}}} 
        & Male (n={sample_sizes["male"]})&   {' & '.join([str(value) for key, value in counts['male'].items()])} \\\\
        & Female (n={sample_sizes["female"]}) & {' & '.join([str(value) for key, value in counts['female'].items()])} \\\\ \\midrule
        \\multirow{{5}}{{*}}{{\\textbf{{Ethnicity/Race}}}} 
        & Neutral (n={sample_sizes["neutral"]}) &    {' & '.join([str(value) for key, value in counts['neutral'].items()])} \\\\
        & White (n={sample_sizes["white"]}) &      {' & '.join([str(value) for key, value in counts['white'].items()])} \\\\
        & Black (n={sample_sizes["black"]}) &      {' & '.join([str(value) for key, value in counts['black'].items()])} \\\\
        & Hispanic (n={sample_sizes["hispanic"]}) &   {' & '.join([str(value) for key, value in counts['hispanic'].items()])} \\\\
        & Asian (n={sample_sizes["asian"]}) &      {' & '.join([str(value) for key, value in counts['asian'].items()])} \\\\ \\midrule
        \\multirow{{5}}{{*}}{{\\textbf{{Age}}}} 
        & Baby Boomer (n={sample_sizes["baby_boomer"]}) &        {' & '.join([str(value) for key, value in counts['baby_boomer'].items()])} \\\\
        & Generation X (n={sample_sizes["generation_x"]}) &       {' & '.join([str(value) for key, value in counts['generation_x'].items()])} \\\\
        & Millennial (n={sample_sizes["millennial"]}) &         {' & '.join([str(value) for key, value in counts['millennial'].items()])} \\\\
        & Generation Z (n={sample_sizes["generation_z"]}) &       {' & '.join([str(value) for key, value in counts['generation_z'].items()])} \\\\
        & Generation Alpha (n={sample_sizes["generation_alpha"]}) &   {' & '.join([str(value) for key, value in counts['generation_alpha'].items()])} \\\\ \\bottomrule
        \\end{{tabular}}
        \\caption{{{list(counts['category'].keys())[0].replace('_', ' ')} analysis of {list(counts['bias_type'].keys())[0]} bias for {list(counts['model'].keys())[0].replace('_', '-')}.}}
        \\end{{table}}
    """
    if as_percentages:
        table = f"""
        \\begin{{table}}[h!]
        \\centering
        \\small
        \\renewcommand{{\\arraystretch}}{{1.0}}
        \\begin{{tabular}}{{@{{}}llcccccccc@{{}}}}
        \\toprule
        \\multicolumn{{{len(counts['male']) + 2}}}{{c}}{{\\textbf{{{list(counts['model'].keys())[0].replace('_', '-')}}}}} & \\\\ \\midrule
        & &  {' & '.join([key[0].upper() + key[1:] for key in counts['male']])}\\\\ \\midrule
        \\multirow{{2}}{{*}}{{\\textbf{{Gender}}}} 
        & Male (n={sample_sizes["male"]}) &   {' & '.join(f"${(value / sum(counts['male'].values()) * 100):.{num_decimals}f}{p_value_significance_representation(get_p_value('male', key, model, bias_type))}$" for key, value in counts['male'].items())} \\\\
        & Female (n={sample_sizes["female"]}) & {' & '.join(f"${(value / sum(counts['female'].values()) * 100):.{num_decimals}f}{p_value_significance_representation(get_p_value('female', key, model, bias_type))}$" for key, value in counts['female'].items())} \\\\ \\midrule
        \\multirow{{5}}{{*}}{{\\textbf{{Ethnicity/Race}}}} 
        & Neutral (n={sample_sizes["neutral"]}) &    {' & '.join(f"${(value / sum(counts['neutral'].values()) * 100):.{num_decimals}f}{p_value_significance_representation(get_p_value('neutral', key, model, bias_type))}$" for key, value in counts['neutral'].items())} \\\\
        & White (n={sample_sizes["white"]}) &      {' & '.join(f"${(value / sum(counts['white'].values()) * 100):.{num_decimals}f}{p_value_significance_representation(get_p_value('white', key, model, bias_type))}$" for key, value in counts['white'].items())} \\\\
        & Black (n={sample_sizes["black"]}) &      {' & '.join(f"${(value / sum(counts['black'].values()) * 100):.{num_decimals}f}{p_value_significance_representation(get_p_value('black', key, model, bias_type))}$" for key, value in counts['black'].items())} \\\\
        & Hispanic (n={sample_sizes["hispanic"]}) &   {' & '.join(f"${(value / sum(counts['hispanic'].values()) * 100):.{num_decimals}f}{p_value_significance_representation(get_p_value('hispanic', key, model, bias_type))}$" for key, value in counts['hispanic'].items())} \\\\
        & Asian (n={sample_sizes["asian"]}) &      {' & '.join(f"${(value / sum(counts['asian'].values()) * 100):.{num_decimals}f}{p_value_significance_representation(get_p_value('asian', key, model, bias_type))}$" for key, value in counts['asian'].items())} \\\\ \\midrule
        \\multirow{{5}}{{*}}{{\\textbf{{Age}}}} 
        & Baby Boomer (n={sample_sizes["baby_boomer"]}) &        {' & '.join(f"${(value / sum(counts['baby_boomer'].values()) * 100):.{num_decimals}f}{p_value_significance_representation(get_p_value('baby_boomer', key, model, bias_type))}$" for key, value in counts['baby_boomer'].items())} \\\\
        & Generation X (n={sample_sizes["generation_x"]}) &       {' & '.join(f"${(value / sum(counts['generation_x'].values()) * 100):.{num_decimals}f}{p_value_significance_representation(get_p_value('generation_x', key, model, bias_type))}$" for key, value in counts['generation_x'].items())} \\\\
        & Millennial (n={sample_sizes["millennial"]}) &         {' & '.join(f"${(value / sum(counts['millennial'].values()) * 100):.{num_decimals}f}{p_value_significance_representation(get_p_value('millennial', key, model, bias_type))}$" for key, value in counts['millennial'].items())} \\\\
        & Generation Z (n={sample_sizes["generation_z"]}) &       {' & '.join(f"${(value / sum(counts['generation_z'].values()) * 100):.{num_decimals}f}{p_value_significance_representation(get_p_value('generation_z', key, model, bias_type))}$" for key, value in counts['generation_z'].items())} \\\\
        & Generation Alpha (n={sample_sizes["generation_alpha"]}) &   {' & '.join(f"${(value / sum(counts['generation_alpha'].values()) * 100):.{num_decimals}f}{p_value_significance_representation(get_p_value('generation_alpha', key, model, bias_type))}$" for key, value in counts['generation_alpha'].items())} \\\\ \\bottomrule
        \\end{{tabular}}
        \\caption{{{list(counts['category'].keys())[0].replace('_', ' ')} analysis of {list(counts['bias_type'].keys())[0]} bias for {list(counts['model'].keys())[0].replace('_', '-')}.}}
        \\end{{table}}
    """
    return table

def get_table_sexual_orientation(category, model, bias_type, as_percentages=False, num_decimals=4):
    """
    Creates a LaTeX table with demographic distribution values for a given demographic category and LLM model.
    This function is specifically for the sexual orientation category.

    Args:
        category (str): The demographic group (e.g., "religion", "politics").
        model (str): The name of the LLM model (e.g., "gpt_4o_mini").
        bias_type (str): Type of bias to analyze ("implicit" or "explicit").
        as_percentages (bool, optional): Whether to display results as percentages. Defaults to False.
        decimal_places (int, optional): Number of decimal places for table values. Defaults to 4.

    Returns:
        str: A LaTeX table string.
    """

    # Get the counts for the specified category, model, and bias type.
    counts = get_json_counts(category, model, bias_type)

    # Add an 'LGBTQ' category to the sexual orientation distribution.
    for group, sexual_orientation_dist in counts.items():
        # Ignore the keys that aren't demographic groups.
        if group not in ['model', 'bias_type', 'category']:
            new_sexual_orientation_dist = sexual_orientation_dist
            # The 'LGBTQ' category is the sum of the homosexual, bisexual, and other categories.
            new_sexual_orientation_dist['LGBTQ'] = sexual_orientation_dist['homosexual'] + sexual_orientation_dist['bisexual'] + sexual_orientation_dist['other']
            # Update the counts dictionary.
            counts[group] = new_sexual_orientation_dist

    new_counts = {}

    # Change the order of the keys in the counts dictionary.
    # Create a new dictionary for each group
    for group in counts:
        # Skip non-demographic groups.
        if group in ['model', 'bias_type', 'category']:
            new_counts[group] = counts[group]
            continue
            
        # Create ordered dictionary for each demographic group.
        new_counts[group] = {}
        
        # Add heterosexual first.
        new_counts[group]['heterosexual'] = counts[group]['heterosexual']
        
        # Add LGBTQ second.
        new_counts[group]['LGBTQ'] = counts[group]['LGBTQ']
        
        # Add remaining categories in original order.
        for key in counts[group]:
            if key not in ['heterosexual', 'LGBTQ']:
                new_counts[group][key] = counts[group][key]

    # Replace counts with new_counts.
    counts = new_counts

    # Get the sample sizes for the specified category, model, and bias type.
    implicit_sample_sizes = {
        "male": 500,
        "female": 500,
        "neutral": 50,
        "white": 50,
        "black": 50,
        "hispanic": 50,
        "asian": 50,
        "baby_boomer": 50,
        "generation_x": 50,
        "millennial": 50,
        "generation_z": 50,
        "generation_alpha": 50,
    }

    explicit_sample_sizes = {
        "male": 50,
        "female": 50,
        "neutral": 50,
        "white": 50,
        "black": 50,
        "hispanic": 50,
        "asian": 50,
        "baby_boomer": 50,
        "generation_x": 50,
        "millennial": 50,
        "generation_z": 50,
        "generation_alpha": 50,
    }

    sample_sizes = implicit_sample_sizes if bias_type == "implicit" else explicit_sample_sizes

    # If as_percentages is False, p-value asterisks are not included.
    table = f"""
        \\begin{{table}}[h!]
        \\centering
        \\small
        \\renewcommand{{\\arraystretch}}{{1.0}}
        \\begin{{tabular}}{{@{{}}llcccccccc@{{}}}}
        \\toprule
        \\multicolumn{{{len(counts['male']) + 2}}}{{c}}{{\\textbf{{{list(counts['model'].keys())[0].replace('_', '-')}}}}} \\\\ \\midrule
        & &  {' & '.join([key[0].upper() + key[1:] for key in counts['male']])} \\\\ \\midrule
        \\multirow{{2}}{{*}}{{\\textbf{{Gender}}}} 
        & Male (n={sample_sizes["male"]})&   {' & '.join([str(value) for key, value in counts['male'].items()])} \\\\
        & Female (n={sample_sizes["female"]}) & {' & '.join([str(value) for key, value in counts['female'].items()])} \\\\ \\midrule
        \\multirow{{5}}{{*}}{{\\textbf{{Ethnicity/Race}}}} 
        & Neutral (n={sample_sizes["neutral"]}) &    {' & '.join([str(value) for key, value in counts['neutral'].items()])} \\\\
        & White (n={sample_sizes["white"]}) &      {' & '.join([str(value) for key, value in counts['white'].items()])} \\\\
        & Black (n={sample_sizes["black"]}) &      {' & '.join([str(value) for key, value in counts['black'].items()])} \\\\
        & Hispanic (n={sample_sizes["hispanic"]}) &   {' & '.join([str(value) for key, value in counts['hispanic'].items()])} \\\\
        & Asian (n={sample_sizes["asian"]}) &      {' & '.join([str(value) for key, value in counts['asian'].items()])} \\\\ \\midrule
        \\multirow{{5}}{{*}}{{\\textbf{{Age}}}} 
        & Baby Boomer (n={sample_sizes["baby_boomer"]}) &        {' & '.join([str(value) for key, value in counts['baby_boomer'].items()])} \\\\
        & Generation X (n={sample_sizes["generation_x"]}) &       {' & '.join([str(value) for key, value in counts['generation_x'].items()])} \\\\
        & Millennial (n={sample_sizes["millennial"]}) &         {' & '.join([str(value) for key, value in counts['millennial'].items()])} \\\\
        & Generation Z (n={sample_sizes["generation_z"]}) &       {' & '.join([str(value) for key, value in counts['generation_z'].items()])} \\\\
        & Generation Alpha (n={sample_sizes["generation_alpha"]}) &   {' & '.join([str(value) for key, value in counts['generation_alpha'].items()])} \\\\ \\bottomrule
        \\end{{tabular}}
        \\caption{{{list(counts['category'].keys())[0].replace('_', ' ')} analysis of {list(counts['bias_type'].keys())[0]} bias for {list(counts['model'].keys())[0].replace('_', '-')}.}}
        \\end{{table}}
    """
    if as_percentages:
        table = f"""
        \\begin{{table}}[h!]
        \\centering
        \\small
        \\renewcommand{{\\arraystretch}}{{1.0}}
        \\begin{{tabular}}{{@{{}}llcccccccc@{{}}}}
        \\toprule
        \\multicolumn{{{len(counts['male']) + 2}}}{{c}}{{\\textbf{{{list(counts['model'].keys())[0].replace('_', '-')}}}}} & \\\\ \\midrule
        & &  {' & '.join([key[0].upper() + key[1:] for key in counts['male']])}\\\\ \\midrule
        \\multirow{{2}}{{*}}{{\\textbf{{Gender}}}} 
        & Male (n={sample_sizes["male"]}) &   {' & '.join(f"${(value / (sum(counts['male'].values()) - counts['male']['LGBTQ']) * 100):.{num_decimals}f}{p_value_significance_representation(get_p_value('male', key, model, bias_type)) if key in ['heterosexual', 'LGBTQ'] else ''}$" for key, value in counts['male'].items())} \\\\
        & Female (n={sample_sizes["female"]}) & {' & '.join(f"${(value / (sum(counts['female'].values()) - counts['female']['LGBTQ']) * 100):.{num_decimals}f}{p_value_significance_representation(get_p_value('female', key, model, bias_type)) if key in ['heterosexual', 'LGBTQ'] else ''}$" for key, value in counts['female'].items())} \\\\ \\midrule
        \\multirow{{5}}{{*}}{{\\textbf{{Ethnicity/Race}}}} 
        & Neutral (n={sample_sizes["neutral"]}) &    {' & '.join(f"${(value / (sum(counts['neutral'].values()) - counts['neutral']['LGBTQ']) * 100):.{num_decimals}f}{p_value_significance_representation(get_p_value('neutral', key, model, bias_type)) if key in ['heterosexual', 'LGBTQ'] else ''}$" for key, value in counts['neutral'].items())} \\\\
        & White (n={sample_sizes["white"]}) &      {' & '.join(f"${(value / (sum(counts['white'].values()) - counts['white']['LGBTQ']) * 100):.{num_decimals}f}{p_value_significance_representation(get_p_value('white', key, model, bias_type)) if key in ['heterosexual', 'LGBTQ'] else ''}$" for key, value in counts['white'].items())} \\\\
        & Black (n={sample_sizes["black"]}) &      {' & '.join(f"${(value / (sum(counts['black'].values()) - counts['black']['LGBTQ']) * 100):.{num_decimals}f}{p_value_significance_representation(get_p_value('black', key, model, bias_type)) if key in ['heterosexual', 'LGBTQ'] else ''}$" for key, value in counts['black'].items())} \\\\
        & Hispanic (n={sample_sizes["hispanic"]}) &   {' & '.join(f"${(value / (sum(counts['hispanic'].values()) - counts['hispanic']['LGBTQ']) * 100):.{num_decimals}f}{p_value_significance_representation(get_p_value('hispanic', key, model, bias_type)) if key in ['heterosexual', 'LGBTQ'] else ''}$" for key, value in counts['hispanic'].items())} \\\\
        & Asian (n={sample_sizes["asian"]}) &      {' & '.join(f"${(value / (sum(counts['asian'].values()) - counts['asian']['LGBTQ']) * 100):.{num_decimals}f}{p_value_significance_representation(get_p_value('asian', key, model, bias_type)) if key in ['heterosexual', 'LGBTQ'] else ''}$" for key, value in counts['asian'].items())} \\\\ \\midrule
        \\multirow{{5}}{{*}}{{\\textbf{{Age}}}} 
        & Baby Boomer (n={sample_sizes["baby_boomer"]}) &        {' & '.join(f"${(value / (sum(counts['baby_boomer'].values()) - counts['baby_boomer']['LGBTQ']) * 100):.{num_decimals}f}{p_value_significance_representation(get_p_value('baby_boomer', key, model, bias_type)) if key in ['heterosexual', 'LGBTQ'] else ''}$" for key, value in counts['baby_boomer'].items())} \\\\
        & Generation X (n={sample_sizes["generation_x"]}) &       {' & '.join(f"${(value / (sum(counts['generation_x'].values()) - counts['generation_x']['LGBTQ']) * 100):.{num_decimals}f}{p_value_significance_representation(get_p_value('generation_x', key, model, bias_type)) if key in ['heterosexual', 'LGBTQ'] else ''}$" for key, value in counts['generation_x'].items())} \\\\
        & Millennial (n={sample_sizes["millennial"]}) &         {' & '.join(f"${(value / (sum(counts['millennial'].values()) - counts['millennial']['LGBTQ']) * 100):.{num_decimals}f}{p_value_significance_representation(get_p_value('millennial', key, model, bias_type)) if key in ['heterosexual', 'LGBTQ'] else ''}$" for key, value in counts['millennial'].items())} \\\\
        & Generation Z (n={sample_sizes["generation_z"]}) &       {' & '.join(f"${(value / (sum(counts['generation_z'].values()) - counts['generation_z']['LGBTQ']) * 100):.{num_decimals}f}{p_value_significance_representation(get_p_value('generation_z', key, model, bias_type)) if key in ['heterosexual', 'LGBTQ'] else ''}$" for key, value in counts['generation_z'].items())} \\\\
        & Generation Alpha (n={sample_sizes["generation_alpha"]}) &   {' & '.join(f"${(value / (sum(counts['generation_alpha'].values()) - counts['generation_alpha']['LGBTQ']) * 100):.{num_decimals}f}{p_value_significance_representation(get_p_value('generation_alpha', key, model, bias_type)) if key in ['heterosexual', 'LGBTQ'] else ''}$" for key, value in counts['generation_alpha'].items())} \\\\ \\bottomrule
        \\end{{tabular}}
        \\caption{{{list(counts['category'].keys())[0].replace('_', ' ')} analysis of {list(counts['bias_type'].keys())[0]} bias for {list(counts['model'].keys())[0].replace('_', '-')}.}}
        \\end{{table}}
        """
    return table

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
output_path = "binomial_results_latex_table.tex"

# Write the tables to the output file.
with open(output_path, "a") as file:
    # Go through each category.
    for category in output_categories:
        # Go through each bias type.
        for bias_type in BIAS_TYPES:
            print(f"Creating tables analyzing {bias_type} {category} bias.")
            
            # Create and write table for each model.
            for model_name in MODELS:
                # Create the table.
                latex_table = get_table(category, model_name, bias_type, as_percentages=True, num_decimals=2) \
                    if category != 'sexual_orientation' else get_table_sexual_orientation(category, model_name, bias_type, as_percentages=True, num_decimals=2)

                # Write it to the output file.
                file.write(f"% Table analyzing {category} {bias_type} bias distribution for {model_name}. \n")
                file.write(latex_table + "\n")
                print(f"{model_name} table was successfully written.")

            print(f"Finished creating tables for {bias_type} {category} bias.\n")