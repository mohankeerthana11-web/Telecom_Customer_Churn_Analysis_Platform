# 📡 ChurnIQ — Telecom Churn Analysis Platform

Full-stack web application: **FastAPI backend + React frontend** for end-to-end telecom customer churn analysis.

---

## 🗂️ Project Structure

```
churn-app/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI app + all routers
│   │   ├── routes/
│   │   │   ├── upload.py              # POST /upload  (full pipeline in one shot)
│   │   │   ├── data.py                # GET  /clean-data
│   │   │   ├── model.py               # GET  /train-model
│   │   │   └── dashboard.py           # GET  /dashboard
│   │   ├── services/
│   │   │   ├── data_service.py        # Clean, encode, scale, EDA
│   │   │   ├── model_service.py       # LR / RF / XGBoost training
│   │   │   ├── predict_service.py     # Risk-tiered predictions
│   │   │   └── dashboard_service.py   # KPIs, charts, recommendations
│   │   └── utils/state.py             # In-memory session state
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── public/index.html
│   ├── src/
│   │   ├── App.js                     # Root — Upload or Dashboard
│   │   ├── index.js / index.css       # Entry point + design system
│   │   ├── services/api.js            # All Axios API calls
│   │   ├── pages/
│   │   │   ├── UploadPage.js          # Drag-drop upload with pipeline progress
│   │   │   └── DashboardPage.js       # 5-tab dashboard
│   │   └── components/
│   │       ├── KpiCards.js            # Accuracy, churn rate, risk counts
│   │       ├── ChurnCharts.js         # Donut, bar, histogram, heatmap
│   │       ├── RiskTable.js           # Paginated high-risk customer table
│   │       ├── RecommendationsPanel.js # Filterable retention actions
│   │       └── UploadBanner.js        # Post-upload summary strip
│   └── package.json
└── generate_sample_data.py            # Creates sample_telecom_data.csv
```

---

## ⚡ Quick Start

### 1. Generate sample data
```bash
python generate_sample_data.py
# → sample_telecom_data.csv (1000 rows, ~33% churn rate)
```

### 2. Start the backend
```bash
cd backend
python -m venv venv
source venv/bin/activate          # macOS/Linux
# venv\Scripts\activate           # Windows

pip install -r requirements.txt
python run.py
# → http://localhost:8000
# → http://localhost:8000/docs  (Swagger UI)
```

### 3. Start the frontend
```bash
cd frontend
npm install
npm start
# → http://localhost:3000
```

---

## 🔌 API Reference

### `POST /upload/`
Upload CSV/Excel — automatically runs the full pipeline (clean → train → predict).

```bash
curl -X POST http://localhost:8000/upload/ \
  -F "file=@sample_telecom_data.csv"
```

**Response:**
```json
{
  "success": true,
  "message": "Pipeline complete for 'sample_telecom_data.csv'",
  "target_column": "Churn",
  "best_model": "random_forest",
  "metrics": { "accuracy": 0.82, "f1": 0.71, "roc_auc": 0.87 },
  "total_customers": 1000,
  "predicted_churn": 334,
  "churn_rate": 0.334,
  "cleaning_report": { "missing_filled": 79, "duplicates_removed": 0 }
}
```

### `GET /dashboard/`
Returns the full dashboard payload for the React frontend.

```bash
curl http://localhost:8000/dashboard/
```

### `GET /clean-data/`
Returns the cleaned dataset preview + EDA stats.

### `GET /train-model/`
Returns model metrics and feature importance.

### `GET /predict`
Returns churn predictions for all customers.

### `POST /reset`
Clears all session state for a fresh upload.

---

## 🎨 Dashboard Tabs

| Tab | Contents |
|---|---|
| **Overview** | Churn donut · Risk breakdown · Probability histogram · Feature importance |
| **Risk Analysis** | High-risk customer table (searchable, sortable, paginated) · Charts |
| **Models** | Model comparison bar chart · Metric table · Correlation heatmap |
| **Recommendations** | Filterable retention actions per at-risk customer |
| **Data Explorer** | Class distribution · Feature–target correlations · Summary statistics |

---

## 🧹 Data Cleaning Pipeline

Automatically applied on every upload:

1. **Duplicate removal**
2. **Type inference** — converts numeric-looking strings to numbers
3. **Missing values** — numeric → mean, categorical → mode
4. **Outlier capping** — IQR method (clips, doesn't drop)
5. **Target encoding** — LabelEncoder to 0/1
6. **Categorical encoding** — LabelEncoder per column
7. **ID column detection & removal** — drops columns where every value is unique
8. **Feature scaling** — StandardScaler

---

## 🤖 ML Models

| Model | Notes |
|---|---|
| Logistic Regression | Baseline, `class_weight="balanced"` |
| Random Forest | 150 trees, max depth 8, balanced |
| XGBoost | Auto-included if installed |

Selection criterion: **F1-Score** on 20% held-out test split.

---

## 💡 Recommendation Engine

Rule-based retention actions for at-risk customers:

| Condition | Action |
|---|---|
| Prob ≥ 80%, high charges | 💰 30% discount offer |
| Prob ≥ 75%, low engagement | 📞 Priority retention call |
| New customer (low tenure) | 🎯 90-day onboarding program |
| General medium risk | ⭐ Loyalty rewards |

---

## 🧪 Testing with Different Datasets

The platform auto-detects target columns matching: `churn`, `exited`, `churned`, `attrition_flag`, `target`, `label`.

It also handles:
- Mixed encodings (UTF-8, Latin-1, CP1252)
- Excel files (.xlsx, .xls)
- Columns with inconsistent types
- High-cardinality ID columns (auto-dropped)
- Heavily imbalanced classes (balanced training weights)
