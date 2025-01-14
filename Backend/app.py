"""Flask Application"""

from flask import Flask, abort, json, jsonify, request
from services.new_monitoring import run_scanPortRange
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

@app.route('/api/runScanPortRange', methods=['POST'])
def run_scan_port_range():
    """Run Scan Port Range"""

    if not request.json or 'toPort' not in request.json or 'fromPort' not in request.json:
        return abort(400, description="Invalid data")

    to_port = request.json['toPort']
    from_port = request.json['fromPort']

    result_from_scanning = run_scanPortRange(from_port, to_port)

    return jsonify(result_from_scanning), 200


# ----- Error Handling -----
@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""

    response = e.get_response()

    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8001)
