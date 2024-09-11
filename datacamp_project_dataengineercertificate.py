# -*- coding: utf-8 -*-
"""DataCamp_Project_DataEngineerCertificate.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ujYXPFLIVAjRJ1AbSilsCNLckx9wHjtS

Data Engineer Certification - Practical Exam - Supplement Experiments
1001-Experiments makes personalized supplements tailored to individual health needs.

1001-Experiments aims to enhance personal health by using data from wearable devices and health apps.

This data, combined with user feedback and habits, is used to analyze and refine the effectiveness of the supplements provided to the user through multiple small experiments.

The data engineering team at 1001-Experiments plays a crucial role in ensuring the collected health and activity data from thousands of users is accurately organized and integrated with the data from supplement usage.

This integration helps 1001-Experiments provide more targeted health and wellness recommendations and improve supplement formulations.

## Task

1001-Experiments currently has the following four datasets with four months of data:
 - "user_health_data.csv" which logs daily health metrics, habits and data from wearable devices,
 - "supplement_usage.csv" which records details on supplement intake per user,
 - "experiments.csv" which contains metadata on experiments, and
 - "user_profiles.csv" which contains demographic and contact information of the users.

Each dataset contains unique identifiers for users and/or their supplement regimen.

The developers and data scientsits currently manage code that cross-references all of these data sources separately, which is cumbersome and error-prone.

Your manager has asked you to write a Python function that cleans and merges these datasets into a single dataset.

The final dataset should provide a comprehensive view of each user's health metrics, supplement usage, and demographic information.

- To test your code, your manager will run only the code `merge_all_data('user_health_data.csv', 'supplement_usage.csv', 'experiments.csv', 'user_profiles.csv')`
- Your `merge_all_data` function must return a DataFrame, with columns as described below.
- All columns must accurately match the descriptions provided below, including names.

aa
"""

# import libraries
import pandas as pd

# function
def merge_all_data(user_health_file, supplement_usage_file, experiments_file, user_profiles_file):
    # Step 1: Read the datasets
    user_health_data = pd.read_csv(user_health_file)
    supplement_usage = pd.read_csv(supplement_usage_file)
    experiments = pd.read_csv(experiments_file)
    user_profiles = pd.read_csv(user_profiles_file)

    #Step 2a: data cleaning - drop na data if any
    user_profiles = user_profiles.dropna(subset=['user_id', 'email'])
    user_health_data = user_health_data.dropna(subset=['user_id', 'date'])
    supplement_usage = supplement_usage.dropna(subset=['user_id', 'date'])

    #Step 2b: data cleaning - convert 'date' to datetime format
    user_health_data['date'] = pd.to_datetime(user_health_data['date'])
    supplement_usage['date'] = pd.to_datetime(supplement_usage['date'])
    user_health_data['date'] = user_health_data['date'].dt.strftime('%Y-%m-%d')
    supplement_usage['date'] = supplement_usage['date'].dt.strftime('%Y-%m-%d')

    #Step 2c: data cleaning - data type cleaning
    # user_health_data['sleep_hours']
    user_health_data['sleep_hours'] = user_health_data['sleep_hours'].str.replace('h', '', case=False)
    user_health_data['sleep_hours'] = user_health_data['sleep_hours'].str.replace('h', '', case=False)
    user_health_data['sleep_hours'] = pd.to_numeric(user_health_data['sleep_hours'], errors='coerce').where(pd.notnull(user_health_data['sleep_hours']), None)

    #Step 2d: data cleaning - unit conversion - dosage
    supplement_usage['dosage_grams'] = supplement_usage.loc[supplement_usage['dosage_unit'] == 'mg', 'dosage'] / 1000


    #Step 2d: data cleaning - add age groups
    def age_group(age):
        if pd.isna(age):
            return 'Unknown'
        elif age < 18:
            return 'Under 18'
        elif 18 <= age <= 25:
            return '18-25'
        elif 26 <= age <= 35:
            return '26-35'
        elif 36 <= age <= 45:
            return '36-45'
        elif 46 <= age <= 55:
            return '46-55'
        elif 56 <= age <= 65:
            return '56-65'
        else:
            return 'Over 65'
    user_profiles['user_age_group'] = user_profiles['age'].apply(age_group)

    #Step 3: join tables
    merged_df = user_profiles.merge(user_health_data, left_on='user_id', right_on='user_id', how='left', suffixes=('_user_profiles', '_user_health'))
    merged_df = merged_df.merge(supplement_usage, on=['user_id', 'date'], how='left', suffixes=('', '_supplement_usage'))
    merged_df = merged_df.merge(experiments, left_on='experiment_id', right_on='experiment_id', how='left', suffixes=('', '_experiments'))

    #Step 4 fill NAs after join
    merged_df['supplement_name'] = merged_df['supplement_name'].fillna('No intake')

    #Step 5: final output - columns selction and rename
    final_df = merged_df[['user_id', 'date', 'email', 'user_age_group', 'name', 'supplement_name', 'dosage_grams', 'is_placebo', 'average_heart_rate', 'average_glucose', 'sleep_hours', 'activity_level']]
    final_df = final_df.rename(columns={'name': 'experiment_name'})

    return final_df

test = merge_all_data('user_health_data.csv', 'supplement_usage.csv', 'experiments.csv', 'user_profiles.csv')
test