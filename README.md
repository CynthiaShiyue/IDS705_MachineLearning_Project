# IDS705_MachineLearning_Project
*Team member* : Skye Augsorn, Hongyi Duan, Nzarama Kouadio, Shiyue Zhou

# Modeling Housing Market Response to Wildfires: Assessing the Impact of Wildfire Exposure on California Home Prices
Wildfire risk in California has surged with climate change, increasing both the frequency and severity of events. From 1972 to 2018, burned area rose fivefold, and recent fires like the 2018 Camp Fire caused billions in damage. Despite clear impacts on real estate, most home price models rely on historical comparables and omit wildfire exposure.

This project uses machine learning to evaluate how wildfire history affects housing price changes at the census tract level (2012–2022). We integrate wildfire data with economic and demographic features to predict detrended price changes using XGBoost.

We explore four core questions:

Does adding wildfire data improve predictive performance?

Can we better model high-risk price drops using a two-stage system?

Are there geographic spillover effects beyond directly burned tracts?

Does model accuracy vary across racial and income-defined communities?

Our results show that wildfire exposure has a measurable, nonlinear effect on housing prices and that model fairness across groups requires closer attention.


# Experiments

##  Experiment 1: Wildfire Impact on Housing Price Change Prediction

###  Objective

This experiment evaluates whether incorporating **wildfire-specific features** improves the prediction of **detrended housing price changes** at the census tract level.  
We aim to quantify both the **predictive power** and the **direction of influence** of wildfire exposure on local housing markets.


###  Method

We compared two types of models:
- **Linear Regression** (baseline linear benchmark)
- **XGBoost** (non-linear gradient boosting)

Each model was trained using:
- **Baseline features**: economic, demographic, and historical housing price indicators
- **Augmented features**: wildfire-specific variables including:
  - Total area burned
  - Years since last fire
  - Binary flags for recent fire exposure (`FIRE_EXPOSED`)
  - Interaction terms

The evaluation used a **temporal train-test split** to simulate out-of-sample forecasting conditions.


###  Core Results & Insights

#### 1.  Model Selection Matters
- **XGBoost significantly outperformed** Linear Regression:
  - **XGBoost R² ≈ 0.90**
  - **Linear Regression R² ≈ 0.59**
- Non-linear models are essential to capture the **complex relationships** between wildfire exposure and price dynamics.

#### 2.  Wildfire Data Adds Predictive Value (for XGBoost)
- Adding wildfire features to XGBoost:
  - **Improved R² by +0.036**
  - **Reduced RMSE and MAE**
- For Linear Regression, wildfire data provided **negligible gains** (+0.001 R²), highlighting its limitations in modeling interactions.

#### 3. Feature Importance Breakdown (in XGBoost)
- **Baseline features** contributed ≈ **86.3%** of total importance.
- **Wildfire-related features** contributed a meaningful **13.7%**, especially:
  - `FIRE_EXPOSED`
  - `YEARS_SINCE_LAST_FIRE`
  - Interaction terms with income and poverty rates

#### 4.  Direction of Impact
- Wildfire exposure **negatively affects price appreciation**, particularly in recently burned areas:
  - FIRE_EXPOSED tracts: average prediction difference = **-0.71**
  - Non-exposed tracts: difference = **-0.27**


###  Conclusion

- Wildfire features provide **valuable secondary signals** in modeling housing price changes.
- Their effects are **non-linear** and best captured using **tree-based methods** like XGBoost.
- The impact of wildfires tends to be **a modest drag on price growth**, strongest in **recently affected tracts**.

In short: while core economic variables remain the main drivers of housing prices, **wildfire exposure matters—and must not be ignored** in risk-aware real estate modeling.

---
##  Experiment 2: Diagnosing and Mitigating Predictive Bias in Price Drop Estimation

###  Objective

This experiment investigates and addresses the **predictive bias** of our baseline regression model when forecasting **price drops** in the housing market.  
Although the baseline XGBoost model performed well overall, it **consistently underperformed** on falling price cases, which are critical for **risk-sensitive applications** such as:
- Disaster planning  
- Insurance underwriting  
- Housing and urban policy  


###  Key Motivation

- Baseline model performance:
  - **R² = 0.8367** for price increases  
  - **R² = 0.6075** for price drops  
- **Price drop cases** showed greater **complexity and volatility**, especially in **fire-exposed regions**.
- Sample distribution was balanced (**≈58% drop vs. 42% increase**), but the model still struggled on drop predictions.
- Cause: external shocks like **wildfires** increase modeling difficulty for price declines.

To resolve this, we implemented a **two-stage modeling pipeline** targeting improved prediction for high-risk price drop scenarios.


###  Method: Two-Stage Modeling Pipeline

#### **Stage 1: Classification**

- We trained an **XGBoost Classifier** to distinguish:
  - **Price Drop (y < 0)**  
  - **Price Increase (y ≥ 0)**
- **Performance**:
  - **Accuracy**: 89%  
  - **Recall (Drop class)**: 81%  
  - **False positive rate**: <1%  

 The classifier's output is used to **route each test sample** to the appropriate regression model.

#### **Stage 2: Conditional Regression**

- **If Increase (y ≥ 0)** → Use existing **baseline XGBoost model**.
- **If Drop (y < 0)** → Use a **specialized drop model**, retrained only on drop samples and optimized via `RandomizedSearchCV`.

###  Results Summary

| Metric                  | Baseline Model | Two-Stage Model |
|-------------------------|----------------|-----------------|
| **R² (Overall)**        | 0.8961         | **0.9014**      |
| **R² (Drop cases only)**| 0.6075         | **0.6333**      |
| **R² (Increase cases)** | 0.8367         | 0.8470          |

 The two-stage model **significantly improves accuracy** for the **drop group** without sacrificing overall performance.


###  Future Direction

- Replace the two-stage model with a **unified regression model** that embeds:
  - Classification outputs  
  - Fire exposure features  
- Explore **interpretable ML models** to understand why some properties decline more than others.
- Integrate **local economic, geographic, or hazard-specific features** to further enhance the drop-specific regressor.


---

##  Experiment 3: Geographic Spillover Effects of Wildfire

###  Objective

This experiment investigates whether the **impact of wildfires on housing prices extends beyond directly burned areas** to nearby, non-affected regions.  
We aim to determine whether **geographic proximity to wildfire exposure leads to variation in model performance**, thereby revealing **spillover effects** in housing market responses.

Understanding these effects is crucial for:
- Estimating the **true spatial reach** of wildfire damage
- Informing policy, insurance, and risk modeling **beyond fire boundaries**
- Improving predictive models for **non-burned but nearby areas**


### Data & Proximity-Based Grouping

We grouped census tracts into **four proximity tiers** based on their distance to fire-affected tracts in each year:

| Group                 | Distance to Burned Tract     |
|----------------------|------------------------------|
| Affected             | Directly burned that year     |
| Very Close Neighbor  | Within 0–2 km                 |
| Close Neighbor       | 2–10 km                       |
| Far Neighbor         | More than 10 km              |

- Distance was calculated using **tract centroid-to-centroid** distance.
- Thresholds reflect the average spacing of census tracts in California (~2 km, per ACS shapefiles).
- Neighboring labels were **assigned annually** to align with year-specific fire exposure.


###  Model Performance by Proximity

We evaluated our **wildfire-inclusive XGBoost model** across the four groups using:
- **RMSE** (Root Mean Squared Error)
- **MAE** (Mean Absolute Error)
- **R²** (Coefficient of Determination)

| Group               | RMSE   | MAE    | R²    |
|--------------------|--------|--------|-------|
| Affected            | 2.80   | 2.01   | 0.94  |
| Very Close Neighbor | ↑13.7% | ↑27.9% | ↓     |
| Close Neighbor      | ↑17.7% | ↑25.9% | ↓     |
| Far Neighbor        | ↑19.0% | ↑27.6% | ↓     |

- **Prediction error increased** with distance from the fire.
- **R² decreased**, indicating weaker model fit further from the fire zone.
- However, **performance between close and far neighbors was similar**, suggesting that **distance alone does not fully explain the trend**.


### Insights & Limitations

- Geographic spillover effects are evident, but **not linearly explained by distance**:
  - Close neighbors did **not consistently outperform** far neighbors.
  - Other factors (e.g., **socioeconomic differences**, **local development patterns**) may confound results.
- Distance was measured **tract-to-tract**, not fire-to-home, potentially missing finer spatial dynamics.
- Future work should explore:
  - **Higher-resolution geospatial modeling**
  - **Feature-level proximity effects**
  - Use of spatial learning techniques (e.g., **graph-based models** or **spatial attention**)

 Conclusion: There is **evidence of geographic spillover** in wildfire impact on housing markets, but the underlying mechanisms are likely more complex than distance alone.

---
##  Experiment 4: Evaluating Fairness Across Demographic Groups

###  Objective

In this experiment, we assess whether our **wildfire prediction model performs equitably across different demographic communities**.  
We focus on **race and income**, given their strong links to structural disparities in housing markets and disaster responses. While the model may perform well overall, **systematic bias** could still exist if certain groups receive **less accurate predictions**.

We ask:  
> **Does the model perform equally well across racial and income-defined groups, or does it produce higher errors in some communities?**


###  Group Definitions & Methodology

- **Race classification**:  
  - Tracts where ≥60% of residents are White → **"White Areas"**  
  - All others → **"POC Areas"** (People of Color)  
- **Income classification (California-specific brackets)**:
  - Low Income: < $61,000  
  - Middle Income: $61,000–$184,000  
  - High Income: > $184,000  
  - Top 1% tracts (> $250K median income) were excluded due to outlier behavior

**Final 6 groups:**
- Low Income White Area
- Low Income POC Area
- Middle Income White Area
- Middle Income POC Area
- High Income White Area
- High Income POC Area

For each group, we evaluated:
- **RMSE**, **MAE**, and **R²**
- **Residuals** (Predicted – Actual)
- **Groupwise t-tests** to compare error distributions


###  Key Results

- **Overall model performance was strong** across all groups (R² > 0.83)
- However, residual analysis revealed consistent **overprediction** across all groups:
  - Middle Income White Areas had the largest overprediction: **–2.68**
  - Low Income POC Areas had the smallest: **–1.85**

| Group A                      | Group B                    | T-statistic | P-value | Significance     |
|-----------------------------|----------------------------|-------------|---------|------------------|
| Middle Income White Area    | Low Income POC Area        | –10.5475    | 0.0000  | **Significant**  |
| High Income White Area      | High Income POC Area       | –2.1607     | 0.0313  | **Significant**  |
| Middle Income White Area    | Middle Income POC Area     | –12.5817    | 0.0000  | **Significant**  |
| Low Income POC Area         | High Income POC Area       | 0.7317      | 0.4648  | Not Significant  |
| Low Income White Area       | High Income White Area     | 1.8204      | 0.0690  | Not Significant  |

- Statistically significant **racial disparities** in residual error were found **even when income was held constant**
- **No significant differences within same-race comparisons (e.g., Low vs. High Income White)**


###  Fairness Insight

-  The model **overpredicts more** in **White communities**, especially middle-income ones
-  **POC communities** had **smaller residuals**, but still saw systematic overprediction
-  **Racial group membership** appears to be a stronger driver of residual bias than income level alone


###  Conclusion

Although the wildfire prediction model performs well overall, it **does not treat all demographic groups equally**.  
Statistically significant gaps in **residual bias** exist across **racial lines**, even after accounting for income.

This highlights an important **fairness issue** in real-world predictive modeling:
> A model may be accurate on average but still **unfair in practice** if its errors systematically disadvantage certain communities.

📎 Future work should consider:
- Group-specific calibration or reweighting  
- Fairness-aware loss functions  
- Incorporating systemic vulnerability indicators beyond race/income thresholds


