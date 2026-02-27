import pandas as pd

path = "data/AB_NYC_2019.csv"
df = pd.read_csv(path)

print("Shape:", df.shape)
print(df.head(3))
print("\nNulls:\n", df.isna().sum().sort_values(ascending=False).head(10))
print("\nPrice describe:\n", df["price"].describe())
print("\nRoom types:\n", df["room_type"].value_counts())
print("\nNeighbourhood groups:\n", df["neighbourhood_group"].value_counts())

print("Listings price = 0:", df[df["price"] == 0].shape[0])
print("Listings price > 1000:", df[df["price"] > 1000].shape[0])

print("\nDuplicates:", df.duplicated().sum())
print("\nDtypes:\n", df.dtypes)