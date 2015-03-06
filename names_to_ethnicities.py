#!/usr/bin/env python
"""
coding=utf-8
"""
import argparse
import logging

import pandas as pd
import nameparser


def create_ethnicity_df(data_path='data/app_c.csv'):
    # Read in from file, with name as index
    raw_names_df = pd.read_csv(data_path, index_col=0)

    # Drop unnecessary columns
    raw_names_df = raw_names_df.drop(['rank', 'count', 'prop100k',
                                      'cum_prop100k'], axis=1)

    # Convert remaining columns to numeric
    raw_names_df = raw_names_df.convert_objects(convert_numeric=True)

    # Change name from index back to column, rename
    raw_names_df = raw_names_df.reset_index()

    # Rename columns to human readable values
    rename_dict = {'name': 'last', 'pctwhite': 'white', 'pctblack': 'black',
                   'pctapi': 'asian_pac_islander', 'pctaian': 'american '
                                                              'indian',
                   'pct2prace': 'two+', 'pcthispanic': 'hispanic'}

    raw_names_df = raw_names_df.rename(columns=rename_dict)

    # NA Values are keyed for unknown percentages, replacing with 0
    raw_names_df = raw_names_df.fillna(0)

    return raw_names_df


def create_names_df(data_path='test_data/test_names.txt'):
    names_list = list()

    # Iterate through file, add parsed names to list
    for line in open(data_path):
        parsed_name = nameparser.HumanName(line).as_dict()
        names_list.append(parsed_name)

    # Convert to DataFrame
    names_df = pd.DataFrame(names_list)

    # Uppercase to match Census data
    names_df['last'] = names_df['last'].apply(lambda x: x.upper())

    return names_df


def normalize_linked_in(
        data_path='test_data/linkedin_connections_export_microsoft_outlook.csv'):
    raw_df = pd.read_csv(data_path)

    raw_df['full_name'] = raw_df['First Name'] + ' ' + raw_df['Last Name']
    raw_df = raw_df[['full_name']]
    raw_df.to_csv('test_data/linked_in_normalized.txt', index=False)


def sum_ethnicity_from_file(file_path):
    logging.info('Begin sum_ethnicity_from_file')
    # Create normalized ethnicity lookup DataFrame
    ethnicity_df = create_ethnicity_df()

    # Create DataFrame containing last names
    names_df = create_names_df(file_path)

    # Merge
    combined_df = pd.merge(names_df, ethnicity_df, how='left', on='last')

    logging.info('End sum_ethnicity_from_file')

    # Output
    return combined_df.mean()

def sum_ethnicity_from_df(names_df, lastname_column='last'):
    logging.info('Begin sum_ethnicity_from_df')
    # Create normalized ethnicity lookup DataFrame
    ethnicity_df = create_ethnicity_df()

    # Normalize DataFrame containing last names
    names_df['last'] = names_df[lastname_column].apply(lambda x: x.upper())
    names_df = names_df[[lastname_column]]

    # Merge
    combined_df = pd.merge(names_df, ethnicity_df, how='left', on='last')

    logging.info('End sum_ethnicity_from_df')
    # Output
    return combined_df.mean()


def main():
    logging.info('Begin Main')
    parser = argparse.ArgumentParser(description='Script to empirially '
                                               'deterime ethnic makeup of a '
                                               'group of names')

    parser.add_argument('--data_path',
                        help='Path to a file, containing one name per line.',
                        type=str, required=True)

    args = parser.parse_args()

    print sum_ethnicity_from_file(args.data_path)
    logging.info('End Main')


if __name__ == '__main__':
    main()


