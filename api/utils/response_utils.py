from flask import jsonify


def BAD_REQUEST(message):
    return jsonify(
        {
            "status": "ERROR",
            "message": message
        }
    ), 400


def SUCCESS(message):
    return jsonify(
        {
            "status": "SUCCESS",
            "message": message
        }
    ), 200


def INTERNAL_ERROR():
    return jsonify(
        {
            "status": "INTERNAL ERROR"
        }
    ), 500
