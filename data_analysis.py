import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def analyze_data(df: pd.DataFrame, industry: str) -> str:
    report_lines = [f"Industry: {industry}", "\nData Overview:", str(df.describe(include='all'))]

    # Detect categorical columns and encode them
    cat_cols = df.select_dtypes(include=['object']).columns
    le = LabelEncoder()
    for col in cat_cols:
        try:
            df[col] = le.fit_transform(df[col].astype(str))
        except Exception as e:
            report_lines.append(f"Could not encode column {col}: {str(e)}")

    # Fill missing values
    df = df.fillna(df.mean(numeric_only=True))

    # Simple Linear Regression if enough data
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) >= 2:
        target = numeric_cols[-1]
        features = numeric_cols[:-1]
        X = df[features]
        y = df[target]

        try:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = LinearRegression()
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            mse = mean_squared_error(y_test, preds)

            report_lines.append("\nLinear Regression Analysis:")
            report_lines.append(f"Features: {features.tolist()}")
            report_lines.append(f"Target: {target}")
            report_lines.append(f"Mean Squared Error: {mse:.2f}")
            report_lines.append(f"Model Coefficients: {model.coef_}")
        except Exception as e:
            report_lines.append(f"Linear regression failed: {str(e)}")

    # KMeans Clustering if enough numeric features
    if len(numeric_cols) >= 2:
        try:
            kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
            clusters = kmeans.fit_predict(df[numeric_cols])
            df['Cluster'] = clusters
            cluster_summary = df.groupby('Cluster').mean(numeric_only=True)

            report_lines.append("\nKMeans Clustering Results:")
            report_lines.append(cluster_summary.to_string())
        except Exception as e:
            report_lines.append(f"KMeans clustering failed: {str(e)}")

    # Industry-specific suggestions
    report_lines.append("\nStrategic Suggestions:")
    if industry.lower() == "retail" or "warehouse" in industry.lower():
        report_lines.append("- Consider analyzing product seasonality trends and reorder thresholds.")
        report_lines.append("- Optimize inventory using clustering for customer segments.")
    elif "health" in industry.lower():
        report_lines.append("- Look for correlations in patient metrics and forecast patient demand.")
        report_lines.append("- Consider clustering for health service usage patterns.")
    else:
        report_lines.append("- Use regression and clustering to uncover trends and segment customers.")

    return {
        "summary": f"Analyzed {len(df)} records with {len(df.columns)} features.",
        "strategy": "Use the insights above to take action based on linear trends and clusters.",
        "insights": "\n".join(report_lines),
        "plots": [],
        "table_data": df.head(10).values.tolist()
    }

