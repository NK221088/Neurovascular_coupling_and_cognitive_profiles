import pandas as pd
from collections import defaultdict

# Loading data as csv file
df = pd.read_csv(r"C:\Users\NTres\OneDrive - Danmarks Tekniske Universitet\Bachelor_projekt\test.csv")

#Extracting summary statistics for all conditions for all channels
ch_stats = defaultdict(lambda: defaultdict())
different_epochs = df["epoch"].unique()
different_channels = [col for col in df.columns if "hbo" in col or "hbr" in col ]
for ep in different_epochs:
    epoch_df = df[df["epoch"] == ep]
    for channel in different_channels:
        ch_stats[epoch_df["condition"].unique()[0]][channel] = epoch_df[channel].describe()