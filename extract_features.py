import pandas as pd
from collections import defaultdict

# Loading data as csv file
df = pd.read_csv(r"C:\Users\NTres\OneDrive - Danmarks Tekniske Universitet\Bachelor_projekt\test.csv")

#Extracting summary statistics for all conditions for all channels
ch_stats = defaultdict(list)
different_conditions = df["condition"].unique()
different_channels = [col for col in df.columns if "hbo" in col or "hbr" in col ]
for condition in different_conditions:
    epoch_df = df[df["condition"] == condition]
    for channel in different_channels:
        stats = epoch_df[channel].describe()
        ch_stats["participant"].append("participant_1")
        ch_stats["channel"].append(channel)
        ch_stats["condition"].append(condition)
        for metric, value in stats.items():
            ch_stats[metric].append(value)
channel_df = pd.DataFrame(ch_stats)

import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter

with localconverter(robjects.default_converter + pandas2ri.converter):
    r_dataframe = robjects.conversion.py2rpy(channel_df)
    robjects.globalenv['channel_df'] = r_dataframe
    
    # Simple, clean R code
    lme_analysis = '''
    print("=== MIXED EFFECTS MODEL ANALYSIS ===")

    # Try lme4 first, fallback to nlme
    if(require(lme4, quietly = TRUE)) {
        print("Using lme4 for analysis")
        
        if(require(lmerTest, quietly = TRUE)) {
            print("Using lmerTest for p-values")
        }
        
        # Random intercepts + slopes
        model <- lmer(mean ~ condition + (1 + condition | participant) + (1 | participant:channel), data = channel_df)
        print(summary(model))
        
    } else if(require(nlme, quietly = TRUE)) {
        print("Using nlme for analysis") 
        
        # nlme version — channels nested in participants
        model <- lme(mean ~ condition, random = ~ condition | participant/channel, data = channel_df)
        print(summary(model))
        
    } else {
        stop("Neither lme4 nor nlme available")
    }
    '''

    
    try:
        robjects.r(lme_analysis)
        print("LME analysis completed!")
    except Exception as e:
        print(f"Error: {e}")