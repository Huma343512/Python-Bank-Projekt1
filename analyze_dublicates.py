import pandas as pd

# Läs in CSV-filen
df = pd.read_csv("data/clean/customers_clean.csv")

# Gruppera på personnummer och visa antal rader per personnummer
count_per_personnummer = df.groupby("Personnummer").size().reset_index(name="Antal förekomster")

# Visa adresser och telefonnummer som finns per personnummer
agg_info = df.groupby("Personnummer").agg({
    "Address": lambda x: list(x.unique()),
    "Phone": lambda x: list(x.unique())
}).reset_index()

# Slå ihop antalet med adresser och telefonnummer
result = pd.merge(count_per_personnummer, agg_info, on="Personnummer")

# Visa resultatet, t.ex. de personnummer som har flera förekomster
print(result[result["Antal förekomster"] > 1])

# Eller spara till fil för närmare analys
result.to_csv("personnummer_analysis.csv", index=False)
