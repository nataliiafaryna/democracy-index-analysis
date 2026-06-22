#  Macroeconomic Data Analysis: GDP, Democracy & Corruption
An end-to-end Data Science project that models and visualizes the mathematical relationship between a country's economic wealth (GDP), political transparency (Corruption Index), and democratic freedoms.

##  About the Project
Instead of standard statistical analysis, this project uses machine learning to find **macroeconomic anomalies**—countries whose real-world development significantly deviates from expected mathematical trends (e.g., "resource autocracies").

**Key Features:**
- **Data Engineering:** Automated data collection via World Bank API and integration of datasets (World Bank, EIU, Transparency International) using ISO-3166 codes.
- **Machine Learning:** - *Multiple Linear Regression* to predict the expected Democracy Index and calculate anomalies.
  - *K-Means Clustering* to group countries into 4 distinct macroeconomic systems.
- **Interactive Dashboard:** A Plotly/Dash web application featuring interactive Choropleth maps and dynamic data filtering.

##Tech Stack
- **Language:** Python 3.x
- **Data Processing:** `pandas`, `numpy`, `wbgapi`
- **Machine Learning:** `scikit-learn` (KMeans, LinearRegression, StandardScaler)
- **Visualization:** `matplotlib`, `seaborn`, `plotly`, `dash`

##Key Insights

Corruption stifles growth: A 1-point improvement in the transparency index is mathematically associated with a ~$1,260 increase in GDP per capita.

The Anomaly Phenomenon: Wealth alone does not guarantee democracy. Several nations (e.g., in the Middle East) artificially maintain autocracies despite having the financial capacity for democratic institutions.

Global Clusters: The K-Means algorithm successfully grouped the world into 4 stable systems: Wealthy Democracies, Ultra-Rich Resource Economies, Transitional Regimes, and Poor Autocracies.
