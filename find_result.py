from flask import Flask, jsonify
import get_result_api as ge


app = Flask(__name__)

# API endpoints find all the data stored in mongodb
@app.route('/find/', methods=['GET'])
def get_result():
    result = []
    cluster = ge.connect()
    db = cluster.nu
    query = db["nu_test"].find({},{"_id":False})
    output = {}
    for records in query:
        result.append(records)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host = "0.0.0.0")
