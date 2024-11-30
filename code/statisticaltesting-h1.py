import pandas as pd
from scipy.stats import ttest_ind, pearsonr
import matplotlib.pyplot as plt

# Load the dataset
file_path = "./data/cleaned-a-dataset.csv"
df = pd.read_csv(file_path)

############## Independent Samples t-Test ##############

# Extract relevant columns
df_ttest = df[['LILATracts_1And10', 'Diagnosed Diabetes (Percentage)']].dropna()

# Split data into two groups based on food insecurity
food_insecure = df_ttest[df_ttest['LILATracts_1And10'] == 1]['Diagnosed Diabetes (Percentage)']
food_secure = df_ttest[df_ttest['LILATracts_1And10'] == 0]['Diagnosed Diabetes (Percentage)']
t_stat, p_value_ttest = ttest_ind(
    food_insecure,
    food_secure,
    alternative='greater'
)

# Print the t-test results
print("\nIndependent Samples t-Test (One-tailed):")
print(f"t-statistic = {t_stat:.4f}, p-value = {p_value_ttest:.4f}")

############## Visualization ##############

# visualize data with a box plot
plt.figure(figsize=(8, 6))
plt.boxplot(
    [food_insecure, food_secure],
    labels=['Food-Insecure Counties', 'Food-Secure Counties'],
    patch_artist=True,
    boxprops=dict(facecolor='lightblue', color='blue'),
    medianprops=dict(color='red'),
)
plt.title('Diabetes Prevalence by Food Insecurity Status')
plt.ylabel('Diagnosed Diabetes (Percentage)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig("boxplot_diabetes_prevalence.png")  
plt.show(block=False)

############## Pearson Correlation Coefficient ##############

df_pearson = df[['LILATracts_1And10', 'Diagnosed Diabetes (Percentage)']].dropna()


df_pearson['LILATracts_1And10'] = pd.to_numeric(df_pearson['LILATracts_1And10'], errors='coerce')
df_pearson['Diagnosed Diabetes (Percentage)'] = pd.to_numeric(df_pearson['Diagnosed Diabetes (Percentage)'], errors='coerce')
df_pearson = df_pearson.dropna()
correlation, p_value_pearson = pearsonr(df_pearson['LILATracts_1And10'], df_pearson['Diagnosed Diabetes (Percentage)'])

# print correlation results
print("\nPearson Correlation Coefficient:")
print(f"Correlation (r) = {correlation:.4f}")
print(f"p-value = {p_value_pearson:.4f}")

