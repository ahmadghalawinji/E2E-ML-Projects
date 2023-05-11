from flask import Flask, render_template, request
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    try:
        Year = int(request.form['Year'])
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Owner=int(request.form['Owner'])

        # Convert fuel type, seller type, and transmission to integers using a dictionary
        conversions = {
            'Petrol': 1,
            'Diesel': 0,
            'Individual': 1,
            'Dealer': 0,
            'Manual': 1,
            'Automatic': 0
        }

        Fuel_Type_Petrol = conversions[request.form['Fuel_Type_Petrol']]
        Fuel_Type_Diesel = 1 - Fuel_Type_Petrol

        Year=2023-Year

        Seller_Type_Individual = conversions[request.form['Seller_Type_Individual']]

        Transmission_Mannual = conversions[request.form['Transmission_Mannual']]

        # Initialize StandardScaler here
        standard_to = StandardScaler()
        Kms_Driven2=np.log(Kms_Driven)
        scaled = standard_to.fit_transform([[Present_Price, Kms_Driven2, Owner, Year, Fuel_Type_Diesel, Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Mannual]])
        prediction=model.predict(scaled)
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    except:
        return render_template('index.html', prediction_texts="Invalid input. Please check your input and try again.")

if __name__=="__main__":
    app.run(debug=True)
