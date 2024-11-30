# Generate a new dataset that merges the Food Access and Diabetes Atlas 
# data into one CSV file that can be used for the analysis project.
#
# The new dataset will inlcude the following data elements:
# CID (County + State Concatenated) | Diagnosed Diabetes % | Obesity % | 
# LILATracts_1And10 | lapophalfshare | PovertyRate | MedianFamilyIncome
#
# Store in ./data/cleanedData.csv

import pandas as pd

## Pre-Process diabetes data to have:
## 1. County + State ID
## 2. Eliminate Extraneous Data

# files
input_file_diabetes = "data/DiabetesAtlasData-initialData.csv"
output_file_diabetes = "data/cleaned-diabetes.csv"

# pandas stuff
df = pd.read_csv(input_file_diabetes, skiprows=2)
df.columns = df.columns.str.strip()
df['CountyID'] = df['State'].str.replace(' ', '') + df['County'].str.replace(' ', '')
df = df.drop(columns=['State', 'County'])
columns = ['CountyID'] + [col for col in df.columns if col != 'CountyID']
df = df[columns]
df.to_csv(output_file_diabetes, index=False)

print(f"Cleaned data saved to {output_file_diabetes}")

## Pre-Process food access data to have:
## 1. Merging together Census Blocks by county
## 2. County + State ID
## 3. Eliminate Extraneous Data


input_file_food = "data/FoodAccessResearch.csv"
output_file_food = "data/cleaned-food-access.csv"

# Read the CSV file
df = pd.read_csv(input_file_food)

# Rename columns to strip whitespace and standardize formatting
df.columns = df.columns.str.strip()

# make a county id to compare the results with other data
df['CountyID'] = df['State'].str.replace(' ', '') + df['County'].str.replace(' ', '')

# lila tracts calculation
df['LILATracts_1And10_Count'] = df.groupby('CountyID')['LILATracts_1And10'].transform('sum')
df['LILATracts_1And10_Total'] = df.groupby('CountyID')['LILATracts_1And10'].transform('size')
df['LILATracts_1And10_Percentage'] = df['LILATracts_1And10_Count'] / df['LILATracts_1And10_Total']

# break into binary
df['LILATracts_1And10_Result'] = (df['LILATracts_1And10_Percentage'] >= 0.5).astype(int)

# sum up counties by id
aggregated_df = df.groupby('CountyID').agg({
    'LILATracts_1And10_Result': 'first',  # Use the calculated result
    'lapophalfshare': 'sum',
    'PovertyRate': 'mean',  # Fix: Calculate the average PovertyRate
    'MedianFamilyIncome': 'mean'  # Fix: Calculate the average MedianFamilyIncome
}).reset_index()

# Save the cleaned data to a new CSV file
aggregated_df.to_csv(output_file_food, index=False)

print(f"Cleaned data saved to {output_file_food}")


## Match diabetes and food access data by county


file_food_access = "data/cleaned-food-access.csv"
file_diabetes = "data/cleaned-diabetes.csv"
output_file_final = "data/cleaned-1-dataset.csv"
df_food_access = pd.read_csv(file_food_access)
df_diabetes = pd.read_csv(file_diabetes)
df_merged = pd.merge(df_food_access, df_diabetes, on='CountyID', how='inner')

df_merged.to_csv(output_file_final, index=False)


