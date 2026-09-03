# Seasonal Agriculture Performance Analysis

## VOIS AICTE Batch 1 2026-2027 - Major Project

## Project Overview

This project analyzes agricultural data across different seasons (Kharif, Rabi, Zaid) to identify meaningful patterns, trends, relationships, and differences in agricultural performance. The analysis examines how environmental conditions, farming practices, resource usage, and economic outcomes vary across seasons.

## Dataset Description

The dataset contains information about:
- **Farm Details**: Farm ID, State, District, Crop, Season, Farm Area
- **Environmental Conditions**: Rainfall, Temperature, Humidity, Sunlight Hours
- **Soil Properties**: Soil pH, Moisture, Nitrogen, Phosphorus, Potassium
- **Farming Practices**: Irrigation Method, Fertilizer, Pesticide, Seed Quality
- **Production Metrics**: Yield, Production, Market Price
- **Economic Indicators**: Total Cost, Revenue, Profit
- **Resource Usage**: Water Used, Water Efficiency, Disease/Pest Risk

## Project Structure

```
seasonal_agriculture_performance_analysis/
├── seasonal_agriculture_performance_dataset.csv  # Raw dataset
├── requirements.txt                              # Python dependencies
├── seasonal_analysis.py                          # Main analysis script
├── preprocessing.py                              # Data preprocessing module
├── visualization.py                              # Visualization module
├── statistical_analysis.py                       # Statistical analysis module
├── README.md                                     # Project documentation
└── [Generated Files]                             # Output files
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone or download this project
2. Navigate to the project directory:
   ```bash
   cd seasonal_agriculture_performance_analysis
   ```
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Option 1: Run Complete Analysis
```bash
python seasonal_analysis.py
```

### Option 2: Run Individual Modules
```python
# Data preprocessing
from preprocessing import DataPreprocessor
preprocessor = DataPreprocessor('seasonal_agriculture_performance_dataset.csv')
df_clean, info = preprocessor.prepare_data()

# Visualization
from visualization import AgriculturalVisualizer
visualizer = AgriculturalVisualizer()
visualizer.create_all_plots(df_clean)

# Statistical Analysis
from statistical_analysis import StatisticalAnalyzer
analyzer = StatisticalAnalyzer(df_clean)
results = analyzer.perform_all_tests(['Yield_Tonnes_Ha', 'Revenue_INR', 'Profit_INR'])
analyzer.print_results(results)
```

### Option 3: Jupyter Notebook
Convert the main script to a Jupyter notebook for interactive analysis:
```bash
jupyter notebook
```
Then copy the code sections into notebook cells.

## Analysis Sections

### 1. Data Loading and Exploration
- Load dataset and examine structure
- Check for missing values
- Understand data types and distributions

### 2. Data Cleaning and Preparation
- Handle missing values (median imputation)
- Create derived features (Profit Margin, Efficiency Categories)
- Prepare data for analysis

### 3. Exploratory Data Analysis (EDA)
- Seasonal distribution analysis
- Performance metrics by season
- Crop distribution across seasons
- Environmental conditions comparison

### 4. Visualization
- Seasonal distribution plots
- Crop performance comparisons
- Environmental condition distributions
- Correlation heatmaps
- Box plots for seasonal comparison
- Regional analysis
- Irrigation method effectiveness

### 5. Statistical Analysis
- **ANOVA Tests**: Compare means across seasons
- **Kruskal-Wallis Tests**: Non-parametric alternatives
- **Chi-Square Tests**: Categorical variable relationships
- **Correlation Analysis**: Variable relationships
- **Effect Size Analysis**: Practical significance

### 6. Advanced Analysis
- Regional performance patterns
- Irrigation method effectiveness
- Crop-wise seasonal performance
- Environmental impact analysis

## Key Findings

The analysis identifies:
1. **Seasonal Performance Patterns**: How yield, revenue, and profit vary by season
2. **Environmental Impact**: Relationship between weather conditions and outcomes
3. **Resource Efficiency**: Water and input usage patterns across seasons
4. **Regional Variations**: Geographic differences in seasonal performance
5. **Crop Suitability**: Which crops perform best in each season

## Generated Output Files

### Visualizations
- `seasonal_distribution.png` - Farm distribution by season
- `seasonal_metrics.png` - Key metrics by season
- `crop_performance.png` - Crop yields and revenue by season
- `environmental_conditions.png` - Environmental variable distributions
- `correlation_heatmap.png` - Variable correlations
- `seasonal_boxplots.png` - Seasonal comparisons
- `regional_analysis.png` - Geographic patterns
- `irrigation_analysis.png` - Irrigation effectiveness

### Data Files
- `cleaned_agriculture_data.csv` - Preprocessed dataset
- `seasonal_performance_summary.csv` - Summary statistics
- `regional_seasonal_analysis.csv` - Regional breakdown

## Key Questions Addressed

1. How does agricultural performance vary across seasons?
2. What major seasonal patterns can be observed?
3. Which characteristics change between seasons?
4. Are there noticeable variations in resource usage across seasons?
5. Are there relationships between seasonal environmental conditions and agricultural performance?
6. How do economic outcomes vary across seasons?
7. Are some seasonal patterns consistent across different regions?
8. What insights can be derived from the observed seasonal differences?

## Recommendations

Based on the analysis:
1. **Seasonal Planning**: Optimize crop selection based on seasonal patterns
2. **Resource Management**: Implement efficient irrigation and input usage
3. **Risk Management**: Monitor and mitigate seasonal risks
4. **Economic Optimization**: Focus on high-margin crops in each season
5. **Environmental Conservation**: Optimize water and input usage

## Technical Details

### Libraries Used
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **matplotlib**: Basic plotting
- **seaborn**: Statistical visualizations
- **scipy**: Statistical tests
- **scikit-learn**: Machine learning utilities

### Statistical Methods
- One-way ANOVA
- Kruskal-Wallis test
- Chi-square test
- Pearson correlation
- Cohen's d effect size

## License

This project is for educational purposes as part of the AICTE Major Project.

## Contact

For questions or issues, please contact the project team.
