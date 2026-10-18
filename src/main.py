import joblib
import pandas as pd
from fastapi import FastAPI , HTTPException
from pydantic import BaseModel , Field

app = FastAPI()

model = joblib.load("house_model.joblib")
features = joblib.load("house_features.joblib")

class HouseFeatures(BaseModel):

    MedInc:float = Field(gt = 0 , description = "median income of neighbourhood")
    HouseAge:float = Field(gt = 0 , description = "Average age of house")
    AveRooms:float = Field(description = "Average number of rooms")
    AveBedrms:float = Field(description = "Average number of bedrooms")
    Population:float = Field(description = "Total population of the area")
    AveOccup:float = Field(gt = 0 , description = "Average number of person in a house")
    Latitude:float = Field(description = "Latitude")
    Longitude:float = Field(description = "Longitude")

@app.get("/")
def home():
    return {
        "message":"California house prediction api",
        "status":"running",
        "endpoint":"send POST request to /predict"
    }     

@app.get("/health")
def health():
    return {
        "status":"running",
        "model":"RandomForestRegressor",
        "features":features,
        "avg_error":"$32,773"
    }

#prediction
@app.post("/predict")
def predict(house:HouseFeatures):

    try:
        input_data = pd.DataFrame([{
            "MedInc":house.MedInc,
            "HouseAge":house.HouseAge,
            "AveRooms":house.AveRooms,
            "AveBedrms":house.AveBedrms,
            "Population":house.Population,
            "AveOccup":house.AveOccup,
            "Latitude":house.Latitude,
            "Longitude":house.Longitude
        }])

        predicted = model.predict(input_data)[0]
        price_usd = predicted*100000

        return{
            "Predicted_price":f"${price_usd:,.0f}",
            "Price_range":f"${price_usd - 32773:,.0f} to ${price_usd + 32773:,.0f}"
        }

    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail = "Prediction Failed"
        )    
