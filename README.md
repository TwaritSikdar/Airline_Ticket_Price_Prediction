# ✈️ Airline Ticket Price Predictor
## 🌟 Overview
This Machine Learning project aims to accurately predict the price of airline tickets across various carriers, sources, and destinations at different times of a day. By analyzing historical flight data, the model provides valuable insights into the key factors driving price fluctuations, enabling better planning for travelers and potentially optimizing pricing strategies.
### Problem Solved
The project tackles the challenge of dynamic airline pricing, predicting ticket costs based on several variables, including the origin/destination, time duration of the flight, total number of stops, and the airline itself.
## 💾 Data Source, Features and EDA
### Data Source
The dataset used for training and testing the models was sourced from EaseMyTrip.com, providing a real-world foundation for the predictive analysis.
### Feature Engineering
The initial dataset underwent extensive **Exploratory Data Analysis (EDA)** and feature engineering to derive more meaningful predictors.
* **Original Features:** `Airline`, `Date_of_Journey`, `Source`, `Destination`, `Route`, `Dep_Time`, `Arrival_Time`, `Duration`, `Total_Stops`, `Additional_Info`, `Price`.
* **Derived/Engineered Features:**
    * Time-based features extracted from `Date_of_Journey`, `Dep_Time`, and `Arrival_Time`: `journey_day`, `journey_month`, `Dep_hour`, `Dep_minute`, `Arrival_hour`, `Arrival_minute`.
    * Duration features: `Duration_hours`, `Duration_minutes`.
### Model Input Features
Categorical features (`Airline`, `Source`, `Destination`) were transformed using One-Hot Encoding with `drop='first'` to prepare them for the model. The final feature set (30 total features) fitted into the model includes:
* **Encoded Categorical:** Multiple one-hot encoded columns for `Airline`, `Source`, and `Destination`.
* **Numerical/Ordinal:** `Total_Stops`, `journey_day`, `journey_month`, `Dep_hour`, `Dep_minute`, `Arrival_hour`, `Arrival_minute`, `Duration_hours`, `Duration_minutes`.
### Exploratory Data Analysis (EDA)
* Histplots and Countplots to visualize the distribution of values in numerical and categorical columns repectively.
* Boxenplots, Boxplots and Violinplots to visualize the relationship between `Price` and `Airline`, `Source` and `Destination`.
* Heatmap to visualize the correlation between features in the data.
## ⚙️ Methodology and Modeling
### Algorithms Explored
A wide range of regression models were explored and benchmarked to find the optimal predictor:
* Linear Regression
* Lasso
* Decision Tree Regressor
* Extra Trees Regressor
* Random Forest regressor
* Ada Boost Regressor
* LightGBM Regressor
* XGBoost Regressor
* KNeighbors Regressor
* Support Vector Regressor
### Final Model
The best performing model, selected after rigorous Hyperparameter Tuning using **GridSearchCV** and **RandomizedSearchCV**, was the **LightGBM Regressor**.
## 📊 Results and Evaluation
The model's performance was evaluated using standard regression metrics.
### Key Evaluation Metrics and Final Scores
| Model | Score | Interpretation |
| :--- | :--- | :--- |
| **$R^2$ Score** | **0.8499** | Approximately 85% of the variance in the ticket price is explained by the model. |
| **Mean Absolute Error (MAE)** | 1134.95 | On average, the model's prediction is off by approximately ₹1135. |
| **Root Mean Squared Error (RMSE)** | 1658.62 | Measures the standard deviation of the prediction errors. |
| **Mean Absolute Percentage Error (MAPE)** | 0.1312 (13.12%) | The average prediction error is about 13.12% of the actual price. |

**The $R^2$ Score of ~0.85 indicates a strong predictive capability.**
## 💻 Installation and Setup
To run this project locally, follow these steps.
### Prerequisites
You need **Python 3.8+** already installed in your system.
### Dependencies
The required libraries are stored in `requirements.txt` file, you can install all of them using `pip`. Also, there are seperate `requirements.txt` files for the apps **AirlinePricePredictorApp_S** and **AirlinePricePredictorApp_F**. If want to run those only you find `requirements.txt` there.
```
pip install -r requirements.txt
```
## 🗂️ Project Structure
```
├── Airline_price_prediction-CV.ipynb
├── Airline_price_prediction-Raw.ipynb
├── Airline_price_prediction.ipynb
├── airline_dataset.xlsx
├── AirlinePricePredictorApp_F/
│    ├── models/
│    │    └── flight_price_preditor_cv.pkl  
│    ├── static/
│    │    └── index_style.css
│    ├── templates/
│    │    └── index.html
│    ├── app.py
│    └── requirements.txt
└── AirlinePricePredictorApp_S/
│    ├── models/
│    │    └── flight_price_preditor_cv.pkl
│    ├── streamlit_app.py 
│    └── requirements.txt
├── README.md
└── requirements.txt
```
## 🚀 Usage and Deployment
The project provides two separate deployment options, accessible via dedicated folders:
1. **Streamlit Application (Interactive Web App)**
  * Folder: `AirlinePricePredictorApp_S`
  * How to Run (If you are using the entire project):
  ```
  cd AirlinePricePredictorApp_S
  streamlit run streamlit_app.py
  ```
  * How to Run (If you are directly running the app):
  ```
  streamlit run streamlit_app.py
  ```
  * *This will open a local web application in your browser for interactive predictions.*
2. **Flask API (RESTful API Service)**
  *  Folder: `AirlinePricePredictorApp_F`
  *  How to Run (If you are using the entire project):
  ```
  cd AirlinePricePredictorApp_F
  python app.py
  ```
  * How to Run (If you are directly running the app):
  ```
  python app.py
  ```
  * *This will start a local API server, allowing predictions to be accessed via HTTP requests.*