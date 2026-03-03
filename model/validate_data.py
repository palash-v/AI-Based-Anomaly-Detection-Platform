import pandas as pd

# Load dataset
df = pd.read_csv("data/live_vitals.csv")

print("Dataset shape:", df.shape)

print("\nMissing values:\n")
print(df.isnull().sum())

print("\nBasic statistics:\n")
print(df.describe())

print("\nDataset preview:\n")
print(df.head())