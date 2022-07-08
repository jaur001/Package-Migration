from flask import Flask, request
from flask.logging import default_handler
from flask_cors import CORS

from Package_API import PackageAPI

app = Flask(__name__)
CORS(app)
app.logger.removeHandler(default_handler)


@app.route("/api/package/migration", methods={'POST'})
def migrate_package():
    try:
        body = request.get_json()
        return PackageAPI.migrate_package(body)
    except Exception as e:
        return "Error in package migration", 500


@app.route("/api/package/creation", methods={'POST'})
def create_package():
    try:
        body = request.get_json()
        return PackageAPI.create_package(body)
    except Exception as e:
        return "Error in package creation", 500


@app.route("/api/package/import", methods={'POST'})
def import_package():
    try:
        body = request.get_json()
        body["type"] = "Import"
        return PackageAPI.import_rollback_package(body)
    except Exception as e:
        return "Error in package import", 500


@app.route("/api/package/rollback", methods={'POST'})
def rollback_package():
    try:
        body = request.get_json()
        body["type"] = "Rollback"
        return PackageAPI.import_rollback_package(body)
    except Exception as e:
        return "Error in package rollback", 500
