## Modeling Wildfire Impact on Housing Price Changes

### Feature Construction and Data Preparation

To understand the effect of wildfires on housing price changes, we filtered the dataset to include only ZIP codes with wildfire exposure (`FIRE_EXPOSED == 1`) and removed rows with missing wildfire variables. We sorted the data by `ZipCode` and `YEAR` to enable lag-based feature engineering.

We only allowed the model to use **historical information** when predicting price changes in a given year. Specifically, we created the following lagged features:
- `HOME_PRICE_LAG1`: home price in the previous year
- `PRICE_CHANGE_LAG1`: price change in the previous year
- `PRICE_CHANGE_DIFF`: difference between current and previous price change

To capture wildfire-specific effects, we constructed:
- `FIRE_SHOCK`: a binary indicator if `NUM_FIRES` is above the median (ZIP-specific fire shock)
- `FIRE_LAST_YEAR`: whether a major fire occurred in the prior year

### Two-Stage Modeling Strategy

To address the concern that housing price changes are largely driven by their own historical values, we used a two-stage modeling approach:

1. **Historical Price Model**  
   A linear regression model was trained to predict `PCT_PRICE_CHANGE (%)` using only `HOME_PRICE_LAG1` and `PRICE_CHANGE_LAG1`. The residuals from this model represent unexplained variation.

2. **Wildfire Residual Model**  
   We used XGBoost to model the residuals from step 1 using wildfire-related variables and constructed shock indicators. This allows us to isolate the contribution of wildfire shocks beyond what historical pricing already predicts.

### Results and Interpretation

**Fire Shock Distribution**  
The FIRE_SHOCK variable shows a clear shift over time, with more fire-intensive ZIP codes appearing from 2016 onward.

**Model Performance**  
The final combined model achieves:
- RMSE: 3.9760
- MAE : 2.8412
- R²  : 0.4323

This indicates a decent level of predictive accuracy, especially considering the limited data and strict constraint of using only lagged price features.

**Actual vs. Predicted Scatter Plot**  
The scatter plot of actual vs. predicted `PCT_PRICE_CHANGE (%)` shows a strong linear trend, indicating the model is capturing general dynamics well. However, some extreme price movements are still under- or over-estimated.

**Feature Importance (Residual Model)**  
Among wildfire-related predictors, the most important features were:
- `AVG_FIRE_DURATION_DAYS`
- `TOTAL_ACRES_BURNED_IN_ZIP`
- `MAX_PCT_ZIP_BURNED`

Interestingly, constructed shock indicators (`FIRE_SHOCK`, `FIRE_LAST_YEAR`) also showed moderate importance, supporting the idea that recent or intense fire events may affect housing prices beyond long-term patterns.

### Conclusion

This two-stage approach effectively separates the historical pricing signal from wildfire-driven shocks. The results suggest that wildfire exposure — particularly when prolonged or large-scale — plays a measurable role in explaining housing price variations after controlling for historical pricing momentum.