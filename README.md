California House Price Prediction API
A REST API that predicts median house prices in California from neighbourhood data.
It serves a Random Forest model trained on the California Housing dataset, built with
FastAPI, scikit-learn, and pandas.
> Status: learning project. Not for real-world pricing decisions.
Features
`POST /predict` returns a predicted price and a typical error range
Input validation with Pydantic (invalid or out-of-range values return a clear 422 error)
`GET /health` shows that the API is running and which features the model expects
Interactive API docs at `/docs` (Swagger UI)
Tech stack
Python, FastAPI, Uvicorn, scikit-learn (RandomForestRegressor), pandas, joblib
Project structure
```
.
├── main.py                  # the FastAPI app
├── house_model.joblib       # trained model
├── house_features.joblib    # feature names, in training order
├── requirements.txt
└── README.md
```
Run it locally
With uv:
```bash
uv add fastapi uvicorn pandas scikit-learn joblib
uv run uvicorn main:app --reload
```
With pip:
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
Then open http://127.0.0.1:8000/docs and try the `/predict` endpoint.
Example request
`POST /predict`
```json
{
  "MedInc": 5.0,
  "HouseAge": 20,
  "AveRooms": 5,
  "AveBedrms": 1,
  "Population": 1000,
  "AveOccup": 3,
  "Latitude": 34.0,
  "Longitude": -118.0
}
```
Example response (values will depend on your model):
```json
{
  "predicted_price": "$255,256",
  "typical_range": "$222,483 to $288,029"
}
```
Input fields
Field	Meaning	Rule
`MedInc`	Median income of the neighbourhood (in $10,000s)	greater than 0
`HouseAge`	Median age of houses	greater than 0, up to 100
`AveRooms`	Average number of rooms	greater than 0
`AveBedrms`	Average number of bedrooms	greater than 0
`Population`	Total population of the area	greater than 0
`AveOccup`	Average number of people per house	greater than 0
`Latitude`	Latitude (California)	32 to 42.5
`Longitude`	Longitude (California)	-124.5 to -114
About the model
Model: Random Forest Regressor
Dataset: California Housing (scikit-learn)
The dataset's target is in units of $100,000, so the API multiplies the prediction by 100,000.
Average error on the test set: about $32,773. The "typical range" in the response is
the prediction plus or minus this average error. It is not a guaranteed interval,
and some predictions will be off by more.
Test-set metrics: add your R² / MAE / RMSE here
Notes
Use the same scikit-learn version that trained the model, or loading the `.joblib` file may fail or warn.
Only load `.joblib` files that you created or trust.
Possible improvements---
Add automated tests for the endpoints
Containerize with Docker
Deploy to a cloud platform
Add a real prediction interval instead of a fixed error range
