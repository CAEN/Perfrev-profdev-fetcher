import pandas as pd
import numpy as np
from csv import writer

import json


def create_fetch_csv_file(import_file_name):
    # Create the "master" csv file that will be appended to.
    base_fetch_name = (f'{import_file_name}-fetched.csv')
    df = pd.DataFrame({
        'First Name': [],
        'Last Name': [],
        'UM ID': [],
        'Uniqname': [],
        'Dept Name': [],
        'Dept ID': [],
        'Session Title': [],
        'DEI': [],
        'Goals': [],
        'Growth': [],
    })
    df.to_csv(base_fetch_name, index=False)

    return base_fetch_name


def import_and_write_csv_data(import_file_name, export_file_name):
    # Read in csv
    dataFrame = pd.read_csv(import_file_name)

    # Remove all invalid entries
    dataFrame['staffProfessionalDevelopment'].replace('', np.nan, inplace=True)
    dataFrame.dropna(subset=['staffProfessionalDevelopment'], inplace=True)
    dataFrame.dropna(subset=['scribedDate'], inplace=True)

    # Sift through all rows that have profdev and add each entry individually
    with open(export_file_name, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        for index, row in dataFrame.iterrows():
            profdev_json = json.loads(row['staffProfessionalDevelopment'])
            for item in profdev_json:
                dept_name = row[6].split('(')[0].strip()
                dept_id = row[6][row[6].find("(")+1:row[6].find(")")]
                new_row_contents = [row[0], row[1], row[2], row[3],
                                    dept_name, dept_id, item['Session'],
                                    item['DEI'], item['Goals'], item['Growth']]
                csv_writer.writerow(new_row_contents)
    print(f'Process complete... Check ({export_file_name}) for results.')


if __name__ == '__main__':
    # Change this file name
    import_file_name = 'pr-export-coe-all-jelkhati2.csv'

    """
    Create base export file (import_file_name_fetched.csv)
    Skim through the import file and remove any rows
    that are either incomplete or don't have profdev
    Then go through each profdev entry and add
    them to the csv
    """
    import_and_write_csv_data(import_file_name,
                              create_fetch_csv_file(import_file_name))
