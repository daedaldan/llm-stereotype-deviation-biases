# LaTeX Tables Generator

This directory contains scripts for generating LaTeX tables used in the research paper from the analysis results. The tables present statistical findings about biases in large language models across different demographic attributes.

## Table of Contents
- [Overview](#overview)
- [Scripts](#scripts)
- [Output Files](#output-files)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Output Description](#output-description)

## Overview

The scripts in this directory process statistical analysis results and generate publication-ready LaTeX tables that can be directly included in academic papers. The tables present:

- Statistical significance of bias measurements
- Comparison of bias across different demographic groups
- Occupation-based bias analysis
- Polarity statistics for model responses

## Scripts

### 1. `create_latex_tables_binomial_tests.py`
- **Purpose**: Generates LaTeX tables for binomial test results
- **Input**: Results from binomial tests conducted in earlier analysis
- **Output**: `binomial_results_latex_table.tex`

### 2. `create_occupation_latex_tables.py`
- **Purpose**: Creates LaTeX tables for occupation-based bias analysis
- **Input**: Processed occupation statistics
- **Output**: `occupation_stats_latex_table.tex`

### 3. `create_polarity_latex_tables.py`
- **Purpose**: Generates tables for polarity analysis of model responses
- **Input**: Polarity statistics from sentiment analysis
- **Output**: `polarity_stats_latex_table.tex`

## Output Files

1. `binomial_results_latex_table.tex`
   - Contains formatted results of binomial tests with p-value significance indicators

2. `occupation_stats_latex_table.tex`
   - Presents occupational distributions across different demographic groups

3. `polarity_stats_latex_table.tex`
   - Highlights sentiment analysis results and differences in response polarity

## Usage

1. Ensure all dependencies are installed (see Dependencies section)
2. Run the scripts in the following order:
   ```bash
   python create_latex_tables_binomial_test.py
   python create_occupation_latex_tables.py
   python create_polarity_latex_tables.py
   ```
3. The generated `.tex` files will be saved in the same directory

## Dependencies

- Python 3.7+
- Required Python packages:
  - pandas
  - numpy

## Output Description

### `binomial_results_latex_table.tex`
- Presents statistical significance of binomial tests for multiple demographic categories
- Highlights significant deviation bias results

### `occupation_stats_latex_table.tex`
- Detailed breakdown of occupational distributions by demographic group

### `polarity_stats_latex_table.tex`
- Sentiment analysis results with comparison of response polarity across groups

## Notes

- The scripts are designed to work with the specific output format from the analysis pipeline
- Customization of table formats can be done by modifying the respective Python scripts
