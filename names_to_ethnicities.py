#!/usr/bin/env python
"""
coding=utf-8
"""

import pandas as pd
import nameparser
import sys


def normalize_pct(input):
    if isinstance(input, ):
        print 'hi'


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
    # names_df = names_df[['last']]
    names_df['last'] = names_df['last'].apply(lambda x: x.upper())

    return names_df


def normalize_linked_in(
        data_path='test_data/linkedin_connections_export_microsoft_outlook.csv'):
    raw_df = pd.read_csv(data_path)

    # raw_df['full_name'] = raw_df['First Name'] + ' ' + raw_df['Last Name']
    raw_df['full_name'] = raw_df['First Name'] + ' ' + raw_df['Last Name']
    raw_df = raw_df[['full_name']]
    raw_df.to_csv('test_data/linked_in_normalized.txt', index=False)


def main():
    # normalize_linked_in('test_data/msan.csv')
    normalize_linked_in()

    # Create normalized ethnicity lookup DataFrame
    ethnicity_df = create_ethnicity_df()

    # Create DataFrame containing last names
    names_df = create_names_df('test_data/linked_in_normalized.txt')

    combined_df = pd.merge(names_df, ethnicity_df, how='left', on='last')

    print combined_df.mean().reset_index().as_matrix()


if __name__ == '__main__':
    main()


