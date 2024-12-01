import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    filename='/app/logs/flask.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
)
logger = logging.getLogger()

# Conversion functions
def convert_temperature(value, from_unit, to_unit):
    conversions = {
        "celsius": lambda x: {"kelvin": x + 273.15, "fahrenheit": x * 9/5 + 32, "rankine": (x + 273.15) * 9/5},
        "kelvin": lambda x: {"celsius": x - 273.15, "fahrenheit": (x - 273.15) * 9/5 + 32, "rankine": x * 9/5},
        "fahrenheit": lambda x: {"celsius": (x - 32) * 5/9, "kelvin": (x - 32) * 5/9 + 273.15, "rankine": x + 459.67},
        "rankine": lambda x: {"celsius": (x - 491.67) * 5/9, "kelvin": x * 5/9, "fahrenheit": x - 459.67},
    }
    if from_unit not in conversions or to_unit not in conversions[from_unit](value):
        return None
    return round(conversions[from_unit](value)[to_unit], 1)

@app.route("/convert", methods=["POST"])
def convert():
    try:
        data = request.json
        logger.debug(f"Received data: {data}")

        value = float(data.get("value"))
        from_unit = data.get("from_unit").lower()
        to_unit = data.get("to_unit").lower()
        student_response = float(data.get("student_response"))

        # Perform conversion
        correct_value = convert_temperature(value, from_unit, to_unit)

        if correct_value is None:
            return jsonify({"output": "invalid"}), 400

        logger.debug(f"Correct Value: {correct_value}, Student Response: {student_response}, Rounded Correct: {round(correct_value, 1)}, Rounded Student: {round(student_response, 1)}")
        # Validate student's response
        if round(correct_value, 1) == round(student_response, 1):
            return jsonify({"output": "correct"}), 200
        else:
            return jsonify({"output": "incorrect"}), 200
    except (ValueError, TypeError):
        logger.error(f"Error occurred: {e}")
        return jsonify({"output": "invalid"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
