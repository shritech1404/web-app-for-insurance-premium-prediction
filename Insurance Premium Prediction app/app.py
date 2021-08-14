from flask import Flask, request, url_for, redirect, render_template, jsonify
import pickle
import numpy
import numpy as np
from numpy import get_include
from flask_mysqldb import MySQL


model = pickle.load(open('insurance.pkl', 'rb'))

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'data_science'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        details = request.form
        
        age = details['age']
        sex = details['sex']
        bmi = details['bmi']
        children = details['children']
        smoker = details['smoker']
        region = details['region']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO insurance(age, sex, bmi, children, smoker, region) VALUES (%s, %s, %s, %s, %s, %s)", (age, sex, bmi, children, smoker, region))
        mysql.connection.commit()
        cur.close()
        int_features = [float(x) for x in request.form.values()]
        final_features = [np.array(int_features)]
        prediction = model.predict(final_features)

        output = round(prediction[0], 2)

        return render_template('result.html', prediction_text='Premium should be ₹ {}'.format(output))

    return render_template('index.html')


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    return render_template('result.html')




@app.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

   

if __name__ == '__main__':
    app.run(debug=True, port=8000)