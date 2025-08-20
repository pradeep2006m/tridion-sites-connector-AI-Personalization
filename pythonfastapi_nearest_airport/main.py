from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from scipy.spatial import KDTree
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import os
import uvicorn
import logging
import pickle
app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://airlines-preview.tridiondemo.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create logs directory if it doesn't exist
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Define log file path
log_file_path = os.path.join(log_dir, "python.log")

# Configure logging
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,  # or DEBUG, WARNING, etc.
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Example log
logging.info("Logging started.")
 
filename_roomtype_finalized_model = 'roomtype_finalized_model.sav'
knn_filename_roomtype_finalized_model = pickle.load(open(filename_roomtype_finalized_model, 'rb'))
le_pets = pickle.load(open("le_pets.sav", 'rb'))
le_room_type = pickle.load(open("le_room_type.sav", 'rb'))


filename_airport_finalized_model = 'airport_finalized_model.sav'
knn_filename_airport_finalized_model = pickle.load(open(filename_airport_finalized_model, 'rb'))
airport_codes = pickle.load(open("airport_codes.sav", 'rb'))
df = pickle.load(open("df.sav", 'rb'))

 
# Input models
class LocationRequest(BaseModel):
    latitude: float
    longitude: float

class AirportCodeRequest(BaseModel):
    code: str
    
class TravellerDetails(BaseModel):
    airPortCode : str
    adults : int
    children : int
    max_child_age : int
    rooms : int
    pets : str
 
 

# Core logic
def Recommendnearesthotel_and_Roomtype(lat, lon, req, k=3):
    print(f"Entered Recommendnearesthotel_and_Roomtype  method")   
   # If total airports < k, adjust k
    total_airports = len(airport_codes)
    k = min(k, total_airports)

    # Get k nearest airports
    _, idxs = knn_filename_airport_finalized_model.query((lat, lon), k=k)

   # Make sure idxs is always iterable
    if k == 1:
        idxs = [idxs]

    # Ensure idxs is iterable (even when k=1)
    if isinstance(idxs, int):
        idxs = [idxs]

    # Build and return list of dictionaries
    nearest_airports = []
  #  print("idxx count", len(idxs))
    for idx in idxs:
        code, name, country, region, touristplace, hotels = airport_codes[idx]
        nearest_airports.append({
            "AirportCode": code,
            "Name": name,
            "CountryCode": country,
            "Region": region,
            "TouristPlace": touristplace,
            "Hotels": hotels
        })  
 
    
    roomtype = predict_room_type(req.adults,req.children,req.max_child_age,req.rooms,req.pets)
    # Example log
     
    print(f"Print Predicted room type: {roomtype}")
    logging.info(f"Logging Predicted room type: {roomtype}")
    print(f"Print nearest_airports: {nearest_airports}")
    #return {"nearest_airports": nearest_airports, "room_type": roomtype}
    return nearest_airports , roomtype
    
# Reusable prediction function
def predict_room_type(adults: int, children: int, max_child_age: int, rooms: int, pets: str):
    input_df = pd.DataFrame([{
        'adults': adults,
        'children': children,
        'max_child_age': max_child_age,
        'rooms': rooms,
        'pets_encoded': le_pets.transform([pets])[0]
    }])
    prediction = knn_filename_roomtype_finalized_model.predict(input_df)
  
    roomtype = le_room_type.inverse_transform(prediction)[0]
    return {"roomtype" : roomtype }




 
# API endpoint 2: recommend
@app.post("/recommend")
def recommend(req: TravellerDetails):
    print(f"Entered recommend endpoint")
    airport_code = req.airPortCode.strip().upper()
    selected = df[df["AirportCode"] == airport_code]
    if selected.empty:
        raise HTTPException(status_code=404, detail=f"Airport code {req.airPortCode} not found.")
    
    lat, lon = selected.iloc[0]["Latitude"], selected.iloc[0]["Longitude"]
     
    print(f"Print latitude: {lat}")
    print(f"Print longitude : {lon}")
    print(f"Print TravellerDetails : {req}")
    nearest = Recommendnearesthotel_and_Roomtype(lat, lon, req, k=3)
    print(f"Print nearest : {nearest}")
    return {"nearest_airports": nearest}



 