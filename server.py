from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS to handle Cross-Origin Resource Sharing
from pytrends.request import TrendReq
import json

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for the app, allowing requests from any domain

# Define route '/get_trends' for GET requests
@app.route('/get_trends', methods=['GET'])
def get_trends():
    # Retrieve the 'keyword' from the query parameters
    keyword = request.args.get('keyword')

    # If no keyword is provided, return an error response
    if not keyword:
        return jsonify({"error": "No keyword provided"}), 400

    # Initialize pytrends request
    pytrends = TrendReq(hl='en-US', tz=360)

    # Build the payload for Google Trends with the provided keyword
    pytrends.build_payload([keyword], timeframe='today 5-y')

    # Get interest over time data from Google Trends
    data = pytrends.interest_over_time()

    # If the returned data is empty, return a 'no data' response
    if data.empty:
        return jsonify({"message": "No data found for the given keyword"}), 404

    # Reset the index of the DataFrame to make 'date' a column instead of an index
    data.reset_index(inplace=True)

    # Convert the DataFrame to a JSON string, formatting dates in ISO 8601 format
    data_json = data.to_json(orient='records', date_format='iso')

    # Parse the JSON string back into a Python list of dictionaries
    data_list = json.loads(data_json)

    # Return the data as a JSON response
    return jsonify(data_list)

# Run the app only if this script is executed as the main program
if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Start the Flask app with debugging enabled on port 5000

