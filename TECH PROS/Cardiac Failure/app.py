
from flask import Flask, request, render_template
import requests


# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "4V8Hmt_nPe0iPHwcUbqXsymoAiHdJCgoW1wrZla65jTD"
token_response = requests.post('https://iam.eu-gb.bluemix.net/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
print("mltoken",mltoken)

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
#payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored, another_array_of_values_to_be_scored]}]}


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/y_predict',methods=['POST'])
def y_predict():
    
    age = request.form["age"]
    sex = request.form["sex"]
    cp = request.form["cp"]
    trtbps = request.form["trtbps"]
    chol = request.form["chol"]
    fbs = request.form["fbs"]
    restecg = request.form["restecg"]
    thalachh = request.form["thalachh"]
    exng = request.form["exng"]
    oldpeak = request.form["oldpeak"]
    slp = request.form["slp"]
    caa = request.form["caa"]
    thall = request.form["thall"]

#age,sex,cp,trtbps,chol,fbs,restecg,thalachh,exng,oldpeak,slp,caa,thall,output
    t = [[int(age),int(sex),int(cp),int(trtbps),int(chol),int(fbs),int(restecg),int(thalachh),int(exng),float(oldpeak),int(slp),int(caa),int(thall)]]
    print(t)
    payload_scoring = {"input_data": [ {"field": [["age","sex","cp","trtbps","chol","fbs","restecg","thalachh","exng","oldpeak","slp","caa","thall"]],
                   "values": t}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/4bb24236-9ec6-46da-ad09-23d3fa10deb8/predictions?version=2021-04-10', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions = response_scoring.json()
    print(predictions)
    pred = predictions['predictions'][0]['values'][0][0]
    if(pred == 0):
        output = "Cardiac Failure"
        print("Cardiac Failure")
    else:
        output = "No Cardiac Failure"
        print("No Cardiac Failure")
    return render_template('index.html', prediction_text= output)


if __name__ == "__main__":
    app.run()
