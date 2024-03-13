from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# This route simulates receiving a play's unique identifier and processing it
@app.route('/process_play/<play_id>', methods=['GET'])
def process_play(play_id):
    # Placeholder for logic to find the play details and update the spreadsheet
    # For example, you could use pandas here to update your spreadsheet based on play_id
    
    # Simulating the update process
    print(f"Processing play with ID: {play_id}")
    
    # Responding to the request to confirm the play has been processed
    return jsonify({"message": "Play processed successfully", "play_id": play_id})

if __name__ == '__main__':
    # Note: In production, you might not want to expose the debug mode or hard-code the port
    app.run(host="0.0.0.0", port=5000, debug=True)
