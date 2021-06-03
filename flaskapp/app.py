from flask import Flask, request, render_template, jsonify
from flask_cors import CORS, cross_origin
import json
import requests
#from create_and_delete_deployment import create_deployment_object,create_deployment,delete_deployment,get_api_instance,create_service,delete_service
import mlflow

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin()
def home():
    return 'Done'

@app.route('/create', methods=['POST'])
def create():
    try:
        body = request.json
        team_id = body['teamid']
        apps_v1 = get_api_instance()
        deployment = create_deployment_object(team_id)
        create_deployment(apps_v1, deployment)
        create_service(team_id)
        return 'Created MLflow instance', 200
    
    except Exception as e:
        print(str(e))
        error_msg = {'ERROR': str(e)}
        return jsonify(error_msg), 500
    
    return 204

@app.route('/delete', methods=['POST'])
def delete():
    try:
        body = request.json
        team_id = body['teamid']
        apps_v1 = get_api_instance()
        delete_deployment(apps_v1, team_id)
        delete_service(team_id)
        return Response(status=status.HTTP_200_OK)

    except Exception as e:
        error_msg = {'ERROR': str(e)}
        return jsonify(error_msg), 500

    return 204

@app.route('/getruns', methods=['GET'])
def getruns():
    try:
        mlflow.set_tracking_uri("http://localhost:5000/")
        data = mlflow.search_runs()
        data = data.to_json(orient ='records')
        print(data)
        return data

    except Exception as e:
        error_msg = {'ERROR': str(e)}
        return jsonify(error_msg), 500

    return 204


if __name__ == "__main__":
    app.run(port="5002",debug=True)