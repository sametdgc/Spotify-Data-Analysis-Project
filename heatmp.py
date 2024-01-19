import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Assuming your data is stored in a DataFrame named df_loaded
df_loaded = pd.read_csv('spotify_final2.csv')

# Melt the DataFrame to make it suitable for visualization
df_melted = pd.melt(df_loaded, id_vars=['artistName', 'trackName', 'genres', 'track_id', 'fall', 'spring', 'summer', 'winter'], 
                    var_name='audio_feature', value_name='value')

# Filter out rows where audio features are null
df_filtered = df_melted.dropna(subset=['value'])

# Define a function to calculate the average audio features for a season
def calculate_average_features(df, season, audio_feature):
    season_df = df[(df[season] > 0) & (df['audio_feature'] == audio_feature)]
    return pd.to_numeric(season_df['value'], errors='coerce').mean()

# Convert milliseconds to minutes for the 'duration_ms' feature
df_filtered.loc[df_filtered['audio_feature'] == 'duration_ms', 'value'] /= 60000

# Rename 'duration_ms' to 'duration_m' in the DataFrame
df_filtered.loc[df_filtered['audio_feature'] == 'duration_ms', 'audio_feature'] = 'duration_m'

# List of audio features
audio_features = ['danceability', 'energy', 'valence', 'tempo', 'duration_m']

# Create a DataFrame to store average values for each season
df_season_avg = pd.DataFrame(index=audio_features, columns=['Fall', 'Spring', 'Summer', 'Winter'])

# Calculate average audio features for each season for all audio features
for feature in audio_features:
    df_season_avg.loc[feature] = [
        calculate_average_features(df_filtered, 'fall', feature),
        calculate_average_features(df_filtered, 'spring', feature),
        calculate_average_features(df_filtered, 'summer', feature),
        calculate_average_features(df_filtered, 'winter', feature)
    ]

# Convert values to numeric
df_season_avg = df_season_avg.apply(pd.to_numeric, errors='coerce')

# Plotting the differences between seasons for each audio feature
plt.figure(figsize=(12, 8))
sns.heatmap(df_season_avg, annot=True, cmap='viridis', fmt=".3f", linewidths=.5)
plt.title('Average Audio Features Differences Between Seasons')
plt.show()
