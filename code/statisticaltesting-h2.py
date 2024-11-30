import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

# pandas stuff
file_path = "./data/cleaned-a-dataset.csv"
df = pd.read_csv(file_path)
df_regression = df[['PovertyRate', 'Diagnosed Diabetes (Percentage)']].dropna()

# set my vars
X = df_regression['PovertyRate']  
Y = df_regression['Diagnosed Diabetes (Percentage)']  
X = sm.add_constant(X)
model = sm.OLS(Y, X).fit()

regression_results = {
    "Variable": model.params.index,
     "Coefficient": model.params.values,
    "Std. Error": model.bse.values,
    "t-value": model.tvalues.values,
    "P>|t|": model.pvalues.values,
    "[0.025": model.conf_int()[0].values,
    "0.975]": model.conf_int()[1].values
}

df_results = pd.DataFrame(regression_results)
output_file = "./data/ols_regression_results.csv"
df_results.to_csv(output_file, index=False)
print(f"OLS Regression Results saved to {output_file}")

intercept = model.params['const']
slope = model.params['PovertyRate']

# show the scaterrplot regression
plt.figure(figsize=(8, 6))
plt.scatter(df_regression['PovertyRate'], df_regression['Diagnosed Diabetes (Percentage)'], alpha=0.6, label='Data')
plt.plot(df_regression['PovertyRate'], intercept + slope * df_regression['PovertyRate'], color='red', label='Regression Line')
plt.title('Regression Analysis: Poverty Rate vs Diabetes Prevalence')
plt.xlabel('Poverty Rate (%)')
plt.ylabel('Diagnosed Diabetes (Percentage)')
plt.legend()
plt.grid(alpha=0.3)
plt.show()

# Interpret the slope and p-value
slope = model.params['PovertyRate']
p_value = model.pvalues['PovertyRate']
print(f"Slope: {slope:.4f}")
print(f"P-value: {p_value:.4f}")


