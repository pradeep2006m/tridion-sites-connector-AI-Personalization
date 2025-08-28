Nearest Airport & Hotel Recommendation API:
------------------------------------------

> A FastAPI application that recommends the nearest airports and predicts suitable hotel room types for travelers using AI.

Features:
--------

> Find nearest airports from a given airport code.

> Predict hotel room type based on traveler details.

> Uses KNN (K-Nearest Neighbors) and pre-trained .sav ML models.

> Provides a REST API (with Swagger docs at /docs).

> Logs predictions for debugging and monitoring.

Tech Stack:
----------

> FastAPI for API development

> scikit-learn for ML models

> Pickle for model persistence

> Uvicorn as ASGI server

Project Structure:
----------------- 

			pythonfastapi_nearest_airport/
				│── main.py                     # Main FastAPI app  
				│── airport_finalized_model.sav # Pre-trained airport KNN model  
				│── roomtype_finalized_model.sav # Pre-trained room type model  
				│── airport_codes.sav           # Encoded airport dataset  
				│── le_pets.sav                 # LabelEncoder for pets  
				│── le_room_type.sav            # LabelEncoder for room types  
				│── df.sav                      # DataFrame with airport details  
				│── requirements.txt            # Python dependencies  
				│── .dockerignore				# Ignore unwanted file while create docker image
				│── Dockerfile					# Docker configuration
				│── web.config					# Configuration file
				│── README.md                   # Project documentation  
				
Install dependencies:
--------------------

> pip install -r requirements.txt

Run the app:
-----------

> Create App docker Image:
	a) docker build -t fastapi-nearest-airport-one .
	
> Run the docker Image:
	a) docker run -p <port_no>:443 fastapi-nearest-airport-one
	

Access API docs:
---------------

> Swagger UI: https://<domain_name>:<port_no>/docs

API Endpoints:
-------------

https://<domain_name>:<port_no>/recommend

> Example Request Body:
	{
	  "airPortCode": "GOI",
	  "adults": 2,
	  "children": 1,
	  "max_child_age": 12,
	  "rooms": 1,
	  "pets": "No"
	}
	
SSL Setup:
---------

> To enable SSL(HTTPS) in Application: "EXPOSE 443" port in Dockerfile.
> Add the below files into root folder Structure.
	a) <certificate_name>.crt.pem
	b) <certificate_name>.key.pem


