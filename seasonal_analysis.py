"""
==============================================================================
Major Project: Seasonal Agriculture Performance Analysis
==============================================================================
VOIS AICTE Batch 1 2026-2027

This script analyzes agricultural data across different seasons (Kharif, Rabi, Zaid)
to identify meaningful patterns, trends, relationships, and differences in 
agricultural performance.

Author: Student
Date: 2026
==============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import f_oneway, kruskal, chi2_contingency
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 11


# =============================================================================
# SECTION 1: DATA LOADING AND INITIAL EXPLORATION
# =============================================================================
print("=" * 80)
print("SECTION 1: DATA LOADING AND INITIAL EXPLORATION")
print("=" * 80)

# Load the dataset
df = pd.read_csv('seasonal_agriculture_performance_dataset.csv')

# Basic information about the dataset
print("\n1.1 Dataset Shape:")
print(f"   Rows: {df.shape[0]}, Columns: {df.shape[1]}")

print("\n1.2 First 5 Rows:")
print(df.head())

print("\n1.3 Dataset Information:")
print(df.info())

print("\n1.4 Statistical Summary:")
print(df.describe())

print("\n1.5 Missing Values:")
print(df.isnull().sum())

print("\n1.6 Unique Seasons:")
print(df['Season'].unique())

print("\n1.7 Season Distribution:")
print(df['Season'].value_counts())


# =============================================================================
# SECTION 2: DATA CLEANING AND PREPARATION
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 2: DATA CLEANING AND PREPARATION")
print("=" * 80)

# Create a copy for cleaning
df_clean = df.copy()

# 2.1 Handle Missing Values
print("\n2.1 Handling Missing Values:")
numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    if df_clean[col].isnull().sum() > 0:
        median_val = df_clean[col].median()
        df_clean[col].fillna(median_val, inplace=True)
        print(f"   Filled {col} with median: {median_val:.2f}")

# 2.2 Create Season Categories for Analysis
print("\n2.2 Creating Season Categories:")
season_mapping = {'Kharif': 'Kharif', 'Rabi': 'Rabi', 'Zaid': 'Zaid'}
df_clean['Season_Category'] = df_clean['Season'].map(season_mapping)

# 2.3 Create Profit Margin Column
df_clean['Profit_Margin'] = (df_clean['Profit_INR'] / df_clean['Revenue_INR']) * 100

# 2.4 Create Water Efficiency Category
df_clean['Water_Efficiency_Category'] = pd.cut(
    df_clean['Water_Efficiency_t_per_1000m3'],
    bins=[0, 2, 5, 10, 50],
    labels=['Low', 'Medium', 'High', 'Very High']
)

# 2.5 Create Disease Risk Category
df_clean['Disease_Risk_Category'] = pd.cut(
    df_clean['Disease_Pest_Risk_pct'],
    bins=[0, 25, 50, 75, 100],
    labels=['Low', 'Medium', 'High', 'Very High']
)

print("\n2.3 Dataset After Cleaning:")
print(f"   Shape: {df_clean.shape}")
print(f"   Missing Values: {df_clean.isnull().sum().sum()}")


# =============================================================================
# SECTION 3: EXPLORATORY DATA ANALYSIS (EDA)
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 3: EXPLORATORY DATA ANALYSIS (EDA)")
print("=" * 80)

# 3.1 Seasonal Distribution Analysis
print("\n3.1 Seasonal Distribution:")
season_counts = df_clean['Season'].value_counts()
print(season_counts)

# 3.2 Seasonal Performance Metrics
print("\n3.2 Average Performance Metrics by Season:")
seasonal_metrics = df_clean.groupby('Season').agg({
    'Yield_Tonnes_Ha': 'mean',
    'Production_Tonnes': 'mean',
    'Revenue_INR': 'mean',
    'Profit_INR': 'mean',
    'Total_Cost_INR': 'mean',
    'Water_Efficiency_t_per_1000m3': 'mean',
    'Disease_Pest_Risk_pct': 'mean'
}).round(2)
print(seasonal_metrics)

# 3.3 Crop Distribution by Season
print("\n3.3 Top Crops by Season:")
for season in df_clean['Season'].unique():
    season_data = df_clean[df_clean['Season'] == season]
    top_crops = season_data['Crop'].value_counts().head(3)
    print(f"\n   {season} Season:")
    for crop, count in top_crops.items():
        print(f"     - {crop}: {count} farms")


# =============================================================================
# SECTION 4: VISUALIZATION
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 4: VISUALIZATION")
print("=" * 80)

# 4.1 Seasonal Distribution Plot
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Season Distribution
season_counts.plot(kind='bar', ax=axes[0, 0], color=['#2ecc71', '#3498db', '#e74c3c'])
axes[0, 0].set_title('Distribution of Farms by Season', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Season')
axes[0, 0].set_ylabel('Number of Farms')
axes[0, 0].tick_params(axis='x', rotation=0)

# Plot 2: Yield by Season
seasonal_yield = df_clean.groupby('Season')['Yield_Tonnes_Ha'].mean()
seasonal_yield.plot(kind='bar', ax=axes[0, 1], color=['#2ecc71', '#3498db', '#e74c3c'])
axes[0, 1].set_title('Average Yield by Season', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Season')
axes[0, 1].set_ylabel('Yield (Tonnes/Ha)')
axes[0, 1].tick_params(axis='x', rotation=0)

# Plot 3: Profit by Season
seasonal_profit = df_clean.groupby('Season')['Profit_INR'].mean()
seasonal_profit.plot(kind='bar', ax=axes[1, 0], color=['#2ecc71', '#3498db', '#e74c3c'])
axes[1, 0].set_title('Average Profit by Season', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Season')
axes[1, 0].set_ylabel('Profit (INR)')
axes[1, 0].tick_params(axis='x', rotation=0)

# Plot 4: Water Efficiency by Season
seasonal_water = df_clean.groupby('Season')['Water_Efficiency_t_per_1000m3'].mean()
seasonal_water.plot(kind='bar', ax=axes[1, 1], color=['#2ecc71', '#3498db', '#e74c3c'])
axes[1, 1].set_title('Average Water Efficiency by Season', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('Season')
axes[1, 1].set_ylabel('Water Efficiency (t/1000m³)')
axes[1, 1].tick_params(axis='x', rotation=0)

plt.tight_layout()
plt.savefig('seasonal_analysis_overview.png', dpi=300, bbox_inches='tight')
plt.show()
print("   Saved: seasonal_analysis_overview.png")

# 4.2 Crop Performance by Season
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Top Crops by Yield
crop_yield = df_clean.groupby(['Crop', 'Season'])['Yield_Tonnes_Ha'].mean().unstack()
crop_yield.head(10).plot(kind='bar', ax=axes[0], width=0.8)
axes[0].set_title('Top 10 Crops: Yield by Season', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Crop')
axes[0].set_ylabel('Yield (Tonnes/Ha)')
axes[0].legend(title='Season')
axes[0].tick_params(axis='x', rotation=45)

# Plot 2: Top Crops by Revenue
crop_revenue = df_clean.groupby(['Crop', 'Season'])['Revenue_INR'].mean().unstack()
crop_revenue.head(10).plot(kind='bar', ax=axes[1], width=0.8)
axes[1].set_title('Top 10 Crops: Revenue by Season', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Crop')
axes[1].set_ylabel('Revenue (INR)')
axes[1].legend(title='Season')
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('crop_performance_by_season.png', dpi=300, bbox_inches='tight')
plt.show()
print("   Saved: crop_performance_by_season.png")

# 4.3 Environmental Conditions by Season
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Rainfall Distribution by Season
for season in df_clean['Season'].unique():
    season_data = df_clean[df_clean['Season'] == season]['Rainfall_mm']
    axes[0, 0].hist(season_data, alpha=0.5, label=season, bins=20)
axes[0, 0].set_title('Rainfall Distribution by Season', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Rainfall (mm)')
axes[0, 0].set_ylabel('Frequency')
axes[0, 0].legend()

# Plot 2: Temperature Distribution by Season
for season in df_clean['Season'].unique():
    season_data = df_clean[df_clean['Season'] == season]['Avg_Temperature_C']
    axes[0, 1].hist(season_data, alpha=0.5, label=season, bins=20)
axes[0, 1].set_title('Temperature Distribution by Season', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Temperature (°C)')
axes[0, 1].set_ylabel('Frequency')
axes[0, 1].legend()

# Plot 3: Humidity Distribution by Season
for season in df_clean['Season'].unique():
    season_data = df_clean[df_clean['Season'] == season]['Humidity_pct']
    axes[1, 0].hist(season_data, alpha=0.5, label=season, bins=20)
axes[1, 0].set_title('Humidity Distribution by Season', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Humidity (%)')
axes[1, 0].set_ylabel('Frequency')
axes[1, 0].legend()

# Plot 4: Soil Moisture by Season
for season in df_clean['Season'].unique():
    season_data = df_clean[df_clean['Season'] == season]['Soil_Moisture_pct']
    axes[1, 1].hist(season_data, alpha=0.5, label=season, bins=20)
axes[1, 1].set_title('Soil Moisture Distribution by Season', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('Soil Moisture (%)')
axes[1, 1].set_ylabel('Frequency')
axes[1, 1].legend()

plt.tight_layout()
plt.savefig('environmental_conditions_by_season.png', dpi=300, bbox_inches='tight')
plt.show()
print("   Saved: environmental_conditions_by_season.png")

# 4.4 Correlation Heatmap
fig, ax = plt.subplots(figsize=(16, 12))
numeric_cols_for_corr = ['Farm_Area_Hectares', 'Rainfall_mm', 'Avg_Temperature_C', 
                         'Humidity_pct', 'Soil_pH', 'Nitrogen_kg_ha', 'Phosphorus_kg_ha',
                         'Potassium_kg_ha', 'Fertilizer_kg_ha', 'Yield_Tonnes_Ha',
                         'Production_Tonnes', 'Revenue_INR', 'Profit_INR', 
                         'Water_Efficiency_t_per_1000m3', 'Disease_Pest_Risk_pct']
corr_matrix = df_clean[numeric_cols_for_corr].corr()
sns.heatmap(corr_matrix, annot=True, cmap='RdYlBu_r', center=0, ax=ax,
            fmt='.2f', linewidths=0.5, square=True)
ax.set_title('Correlation Heatmap of Agricultural Metrics', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()
print("   Saved: correlation_heatmap.png")

# 4.5 Box Plots for Seasonal Comparison
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

metrics_to_compare = ['Yield_Tonnes_Ha', 'Revenue_INR', 'Profit_INR', 
                      'Water_Efficiency_t_per_1000m3', 'Disease_Pest_Risk_pct', 'Total_Cost_INR']

for idx, metric in enumerate(metrics_to_compare):
    row = idx // 3
    col = idx % 3
    df_clean.boxplot(column=metric, by='Season', ax=axes[row, col])
    axes[row, col].set_title(f'{metric.replace("_", " ")} by Season', fontsize=12, fontweight='bold')
    axes[row, col].set_xlabel('Season')
    axes[row, col].set_ylabel(metric.replace('_', ' '))

plt.suptitle('Seasonal Comparison of Key Metrics', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('seasonal_boxplots.png', dpi=300, bbox_inches='tight')
plt.show()
print("   Saved: seasonal_boxplots.png")


# =============================================================================
# SECTION 5: STATISTICAL ANALYSIS
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 5: STATISTICAL ANALYSIS")
print("=" * 80)

# 5.1 ANOVA Test for Seasonal Differences
print("\n5.1 ANOVA Test for Seasonal Differences:")
print("-" * 50)

key_metrics = ['Yield_Tonnes_Ha', 'Revenue_INR', 'Profit_INR', 
               'Water_Efficiency_t_per_1000m3', 'Disease_Pest_Risk_pct']

for metric in key_metrics:
    groups = [group[metric].dropna() for name, group in df_clean.groupby('Season')]
    f_stat, p_value = f_oneway(*groups)
    
    print(f"\n   {metric}:")
    print(f"     F-statistic: {f_stat:.4f}")
    print(f"     p-value: {p_value:.6f}")
    if p_value < 0.05:
        print(f"     Result: Significant difference (p < 0.05)")
    else:
        print(f"     Result: No significant difference (p >= 0.05)")

# 5.2 Kruskal-Wallis Test (Non-parametric)
print("\n\n5.2 Kruskal-Wallis Test (Non-parametric):")
print("-" * 50)

for metric in key_metrics:
    groups = [group[metric].dropna() for name, group in df_clean.groupby('Season')]
    h_stat, p_value = kruskal(*groups)
    
    print(f"\n   {metric}:")
    print(f"     H-statistic: {h_stat:.4f}")
    print(f"     p-value: {p_value:.6f}")
    if p_value < 0.05:
        print(f"     Result: Significant difference (p < 0.05)")
    else:
        print(f"     Result: No significant difference (p >= 0.05)")

# 5.3 Chi-Square Test for Categorical Variables
print("\n\n5.3 Chi-Square Test for Categorical Relationships:")
print("-" * 50)

# Test relationship between Season and Crop
contingency_table = pd.crosstab(df_clean['Season'], df_clean['Crop'])
chi2, p_value, dof, expected = chi2_contingency(contingency_table)
print(f"\n   Season vs Crop:")
print(f"     Chi-square statistic: {chi2:.4f}")
print(f"     p-value: {p_value:.6f}")
print(f"     Degrees of freedom: {dof}")
if p_value < 0.05:
    print(f"     Result: Significant association (p < 0.05)")
else:
    print(f"     Result: No significant association (p >= 0.05)")

# Test relationship between Season and Irrigation Method
contingency_table2 = pd.crosstab(df_clean['Season'], df_clean['Irrigation_Method'])
chi2, p_value, dof, expected = chi2_contingency(contingency_table2)
print(f"\n   Season vs Irrigation Method:")
print(f"     Chi-square statistic: {chi2:.4f}")
print(f"     p-value: {p_value:.6f}")
print(f"     Degrees of freedom: {dof}")
if p_value < 0.05:
    print(f"     Result: Significant association (p < 0.05)")
else:
    print(f"     Result: No significant association (p >= 0.05)")

# 5.4 Seasonal Performance Summary Statistics
print("\n\n5.4 Detailed Seasonal Performance Summary:")
print("-" * 50)

seasonal_summary = df_clean.groupby('Season').agg({
    'Yield_Tonnes_Ha': ['mean', 'median', 'std', 'min', 'max'],
    'Revenue_INR': ['mean', 'median', 'std', 'min', 'max'],
    'Profit_INR': ['mean', 'median', 'std', 'min', 'max'],
    'Water_Efficiency_t_per_1000m3': ['mean', 'median', 'std'],
    'Disease_Pest_Risk_pct': ['mean', 'median', 'std']
}).round(2)

print(seasonal_summary)


# =============================================================================
# SECTION 6: ADVANCED ANALYSIS
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 6: ADVANCED ANALYSIS")
print("=" * 80)

# 6.1 Regional Analysis by Season
print("\n6.1 Regional Performance by Season:")
regional_seasonal = df_clean.groupby(['State', 'Season']).agg({
    'Yield_Tonnes_Ha': 'mean',
    'Profit_INR': 'mean',
    'Revenue_INR': 'mean'
}).round(2)

# Top performing states by season
for season in df_clean['Season'].unique():
    season_data = df_clean[df_clean['Season'] == season]
    state_performance = season_data.groupby('State')['Profit_INR'].mean().sort_values(ascending=False)
    print(f"\n   Top 3 States by Profit in {season} Season:")
    for i, (state, profit) in enumerate(state_performance.head(3).items(), 1):
        print(f"     {i}. {state}: INR {profit:,.2f}")

# 6.2 Irrigation Method Analysis by Season
print("\n\n6.2 Irrigation Method Effectiveness by Season:")
irrigation_seasonal = df_clean.groupby(['Irrigation_Method', 'Season']).agg({
    'Yield_Tonnes_Ha': 'mean',
    'Water_Efficiency_t_per_1000m3': 'mean',
    'Profit_INR': 'mean'
}).round(2)
print(irrigation_seasonal)

# 6.3 Crop-Wise Seasonal Performance
print("\n\n6.3 Top Performing Crops by Season:")
for season in df_clean['Season'].unique():
    season_data = df_clean[df_clean['Season'] == season]
    crop_performance = season_data.groupby('Crop').agg({
        'Yield_Tonnes_Ha': 'mean',
        'Profit_INR': 'mean'
    }).sort_values('Profit_INR', ascending=False)
    
    print(f"\n   Top 5 Crops in {season} Season (by Profit):")
    for i, (crop, row) in enumerate(crop_performance.head(5).iterrows(), 1):
        print(f"     {i}. {crop}: Yield={row['Yield_Tonnes_Ha']:.2f} t/ha, Profit=INR {row['Profit_INR']:,.2f}")

# 6.4 Environmental Impact Analysis
print("\n\n6.4 Environmental Factors Impact on Yield by Season:")
for season in df_clean['Season'].unique():
    season_data = df_clean[df_clean['Season'] == season]
    corr_rainfall = season_data['Rainfall_mm'].corr(season_data['Yield_Tonnes_Ha'])
    corr_temp = season_data['Avg_Temperature_C'].corr(season_data['Yield_Tonnes_Ha'])
    
    print(f"\n   {season} Season:")
    print(f"     Rainfall-Yield Correlation: {corr_rainfall:.3f}")
    print(f"     Temperature-Yield Correlation: {corr_temp:.3f}")


# =============================================================================
# SECTION 7: KEY FINDINGS AND INSIGHTS
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 7: KEY FINDINGS AND INSIGHTS")
print("=" * 80)

print("\n7.1 Seasonal Performance Patterns:")
print("-" * 50)

# Calculate seasonal averages
seasonal_avg = df_clean.groupby('Season').agg({
    'Yield_Tonnes_Ha': 'mean',
    'Revenue_INR': 'mean',
    'Profit_INR': 'mean',
    'Water_Efficiency_t_per_1000m3': 'mean',
    'Disease_Pest_Risk_pct': 'mean'
}).round(2)

# Find best season for each metric
print("\n   Best Season by Metric:")
for metric in seasonal_avg.columns:
    best_season = seasonal_avg[metric].idxmax()
    best_value = seasonal_avg[metric].max()
    print(f"   - {metric.replace('_', ' ')}: {best_season} ({best_value:,.2f})")

print("\n7.2 Key Observations:")
print("-" * 50)

# Calculate profit margins by season
seasonal_profit_margin = df_clean.groupby('Season').apply(
    lambda x: (x['Profit_INR'].sum() / x['Revenue_INR'].sum()) * 100
).round(2)

print(f"\n   1. Profit Margin by Season:")
for season, margin in seasonal_profit_margin.items():
    print(f"      - {season}: {margin:.2f}%")

# Water efficiency comparison
seasonal_water_eff = df_clean.groupby('Season')['Water_Efficiency_t_per_1000m3'].mean()
print(f"\n   2. Water Efficiency Ranking:")
for season, eff in seasonal_water_eff.sort_values(ascending=False).items():
    print(f"      - {season}: {eff:.2f} t/1000m³")

# Disease risk comparison
seasonal_disease = df_clean.groupby('Season')['Disease_Pest_Risk_pct'].mean()
print(f"\n   3. Disease/Pest Risk Ranking (Lower is better):")
for season, risk in seasonal_disease.sort_values(ascending=True).items():
    print(f"      - {season}: {risk:.2f}%")

print("\n7.3 Recommendations:")
print("-" * 50)
print("""
   Based on the analysis, the following recommendations are made:
   
   1. SEASONAL PLANNING:
      - Optimize crop selection based on seasonal performance patterns
      - Consider weather forecasts for planting decisions
   
   2. RESOURCE MANAGEMENT:
      - Implement efficient irrigation methods based on seasonal needs
      - Adjust fertilizer and pesticide application according to season
   
   3. RISK MANAGEMENT:
      - Monitor disease/pest risk patterns by season
      - Implement preventive measures during high-risk periods
   
   4. ECONOMIC OPTIMIZATION:
      - Focus on high-margin crops in each season
      - Consider market price fluctuations across seasons
   
   5. ENVIRONMENTAL CONSERVATION:
      - Optimize water usage based on seasonal requirements
      - Implement sustainable farming practices
""")


# =============================================================================
# SECTION 8: EXPORT RESULTS
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 8: EXPORT RESULTS")
print("=" * 80)

# Export cleaned data
df_clean.to_csv('cleaned_agriculture_data.csv', index=False)
print("\n   Saved: cleaned_agriculture_data.csv")

# Export seasonal summary
seasonal_summary.to_csv('seasonal_performance_summary.csv')
print("   Saved: seasonal_performance_summary.csv")

# Export regional analysis
regional_seasonal.to_csv('regional_seasonal_analysis.csv')
print("   Saved: regional_seasonal_analysis.csv")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE!")
print("=" * 80)
print("\nGenerated Files:")
print("   1. seasonal_analysis_overview.png")
print("   2. crop_performance_by_season.png")
print("   3. environmental_conditions_by_season.png")
print("   4. correlation_heatmap.png")
print("   5. seasonal_boxplots.png")
print("   6. cleaned_agriculture_data.csv")
print("   7. seasonal_performance_summary.csv")
print("   8. regional_seasonal_analysis.csv")
print("\n" + "=" * 80)
