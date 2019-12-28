from flask import current_app as app 
from flask import jsonify


@app.errorhandler(404)
def not_found(error=None):

    response = {
        'status': 404,
        'message': str(error),
    }

    return jsonify(response), 404



@app.errorhandler(500)
def internal_error(error=None):

    response = {
        'status': 500,
        'message': str(error),
    }

    return jsonify(response), 500


@app.errorhandler(405)
def not_allowed(error=None):

    response = {
        'status': 405,
        'message': str(error)
    }

    return jsonify(response), 405