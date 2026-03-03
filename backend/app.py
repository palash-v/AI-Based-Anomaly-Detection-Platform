from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route("/alerts")
def get_alerts():
    try:
        df = pd.read_csv("data/alerts.csv")
        return jsonify(df.tail(10).to_dict(orient="records"))
    except:
        return jsonify([])

if __name__ == "__main__":
    app.run(debug=True, port=5000)