# Spotify-Data-Analysis-Project
Huseyin Samed Dagci - CS210 Data Science Course Project

# Music Preferences Analysis

This repository contains the code and analysis for a data science project exploring seasonal variations in music preferences based on audio features and genres. The project investigates whether there is a significant difference in music preferences across different seasons.

## Hypotheses

### Null Hypothesis (H₀):
There is no significant difference in music preferences, as measured by audio features and genres, across different seasons. Specifically, the mean values of both audio features and genres remain constant throughout each season.

### Alternative Hypothesis (Hₐ):
There is a significant difference in music preferences, as measured by audio features and genres, across different seasons. Specifically, the mean values of either audio features or genres (or both) change noticeably from one season to another, indicating a seasonal variation in music preferences.

## Project Structure

- `data/`: Contains the dataset used for analysis (`StreamingHistory0.json`).
- `notebooks/`: Jupyter notebooks with the analysis and visualization code.
  - `1_seasonal.py.ipynb`: Cleaning and preprocessing of the Spotify data.
  - `2_seasonal.py`: Utilizing Spotify API for additional feature extraction.
  - `3_heatmap.py`: Visualizing seasonal variations in music preferences.
- `spotify_final2.csv`: Original dataset obtained from Spotify.
- `requirements.txt`: Dependencies required for running the notebooks.

## Data Cleaning and Preprocessing

The dataset was obtained from Spotify and cleaned using Pandas DataFrame. The cleaning process included handling missing values, transforming data types, and preparing the data for further analysis.

## Feature Engineering

Spotify API was used to extract additional features related to music preferences. This enhanced the dataset with more detailed information for a comprehensive analysis.

## Visualizations

Jupyter notebooks in the `notebooks/` directory contain visualizations illustrating the seasonal variations in music preferences. These visualizations include plots showcasing the dominant genres, top genres in each season, and more.

## Usage

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
