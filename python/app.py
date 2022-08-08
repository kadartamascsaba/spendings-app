from flask import Flask, jsonify, request
from flask_cors import CORS


from models import Spending
from controllers import filter_spendings, order_spendings
from utils import ValidationError


app = Flask(__name__)
CORS(app)

app.spendings = []


@app.route("/spendings", methods=["GET", "POST"])
def get_spendings():
    if request.method == "GET":
        args = request.args
        results = app.spendings

        results = filter_spendings(results, args)
        results = order_spendings(results, args)

        return jsonify(list(map(Spending.to_dict, results)))

    elif request.method == "POST":
        spending_data = request.json

        try:
            Spending.is_valid(spending_data, raise_exception=True)
        except ValidationError as ve:
            return jsonify(ve.details), 400

        spending = Spending(spending_data)
        app.spendings.append(spending)

        return jsonify(spending.to_dict()), 201
