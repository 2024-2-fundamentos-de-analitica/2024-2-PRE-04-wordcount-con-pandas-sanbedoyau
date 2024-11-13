"""Taller evaluable"""

import pandas as pd
import glob
import os

def load_input(input_directory):
    '''Load text files in 'input_directory/'''
    files = glob.glob(f'{input_directory}/*')
    dataframes = [
        pd.read_csv(
            file,
            header = None,
            delimiter = '\t',
            names = ['line'],
            index_col = None
        ) for file in files
    ]

    df = pd.concat(dataframes, ignore_index = True)
    return df

def clean_text(dataframe):
    '''Text cleaning'''
    df = dataframe.copy()
    df['line'] = df['line'].str.lower()
    df['line'] = (
     df['line']
     .str.replace(',', '')
     .str.replace('.', '')
    )
    return df

def count_words(dataframe):
    '''Word count'''
    df = dataframe.copy()
    df['line'] = df['line'].str.split()
    df = df.explode('line')
    df = df.groupby('line').size().reset_index(name = 'Count')
    return df

def save_output(dataframe, output_directory):
    '''Save output to a file'''
    if os.path.exists(output_directory):
        files = glob.glob(f'{output_directory}/*')
        for file in files:
            os.remove(file)
        os.rmdir(output_directory)

    os.makedirs(output_directory)

    dataframe.to_csv(
        f'{output_directory}/part-00000',
        sep = '\t',
        index = False,
        header = False,
    )

def create_marker(output_directory):
    '''Create Marker'''

    with open(f'{output_directory}/_SUCCESS', 'w', encoding = 'utf-8') as f:
        f.write('')

#
# Escriba la función job, la cual orquesta las funciones anteriores.
#

def run_job(input_directory, output_directory):
    """Job"""
    df = load_input(input_directory)
    df = clean_text(df)
    df = count_words(df)
    save_output(df, output_directory)
    create_marker(output_directory)


if __name__ == "__main__":

    run_job(
        "files/input",
        "files/output",
    )
