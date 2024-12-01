import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configure logging for Lambda
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
)
logger = logging.getLogger()

# Conversion functions
def convert_units(value, from_unit, to_unit):
    conversions = {
        "temperature": {
            "celsius": lambda x: {"kelvin": x + 273.15, "fahrenheit": x * 9/5 + 32, "rankine": (x + 273.15) * 9/5},
            "kelvin": lambda x: {"celsius": x - 273.15, "fahrenheit": (x - 273.15) * 9/5 + 32, "rankine": x * 9/5},
            "fahrenheit": lambda x: {"celsius": (x - 32) * 5/9, "kelvin": (x - 32) * 5/9 + 273.15, "rankine": x + 459.67},
            "rankine": lambda x: {"celsius": (x - 491.67) * 5/9, "kelvin": x * 5/9, "fahrenheit": x - 459.67},
        },
         "distance": {
            "meters": lambda x: {"kilometers": x / 1000, "miles": x / 1609.34},
            "kilometers": lambda x: {"meters": x * 1000, "miles": x / 1.60934},
        },
        "weight": {
            "grams": lambda x: {"kilograms": x / 1000, "pounds": x / 453.592},
            "kilograms": lambda x: {"grams": x * 1000, "pounds": x * 2.20462},
        },
    }
    for category, units in conversions.items():
        if from_unit in units and to_unit in units[from_unit](value):
            return round(units[from_unit](value)[to_unit], 2)
    return None  # Invalid unit conversion

@app.route("/convert", methods=["POST"])
def convert():
    try:
        data = request.json
        if not data or "value" not in data or "from_unit" not in data or "to_unit" not in data or "student_response" not in data:
            return jsonify({"output": "invalid"}), 400

        value = float(data.get("value"))
        from_unit = data.get("from_unit").lower()
        to_unit = data.get("to_unit").lower()
        student_response = float(data.get("student_response"))

        # Validate units
        valid_units = ["celsius", "kelvin", "fahrenheit", "rankine", "meters", "kilometers", "grams", "kilograms"]
        if from_unit not in valid_units or to_unit not in valid_units:
            return jsonify({"output": "invalid"}), 400

        correct_value = convert_units(value, from_unit, to_unit)
        if correct_value is None:
            return jsonify({"output": "invalid"}), 400

        # Validate student's response
        if abs(correct_value - student_response) < 0.05:
            return jsonify({"output": "correct"}), 200
        else:
            return jsonify({"output": "incorrect"}), 200
    except ValueError:
        return jsonify({"output": "invalid"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
