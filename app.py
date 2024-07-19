from flask import Flask
from google.cloud.sql.connector import connector, IPTypes
from datetime import datetime

import json
import logging
import os
import traceback

app = Flask(__name__)

@app.route('/')
def index() -> str:
    result = '<br/>Oh hi!'
    try:
        result = '<pre>' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f") + '<pre>'

        instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]  # e.g. 'project:region:instance'
        db_iam_user = os.environ["DB_IAM_USER"]  # e.g. 'sa-name@project-id.iam'
        fixed_db_iam_user = db_iam_user.split("@")[0] # remove @project-id.iam'
        db_name = os.environ["DB_NAME"]  # e.g. 'my-database'

        result += "<br/>About to open connection: <pre>connector.connect(" + instance_connection_name +', "pymysql", user=' + fixed_db_iam_user + ", db=" + db_name + ", enable_iam_auth=True, ip_type=IPTypes.PRIVATE)"
        connection = connector.connect(instance_connection_name, "pymysql", user=fixed_db_iam_user, db=db_name, enable_iam_auth=True, ip_type=IPTypes.PRIVATE)
        result += "<br/>Successfully connected."
        cursor = connection.cursor()
        result += "<br/>Successfully acquired cursor."
        cursor.execute('SELECT database();')
        result += "<br/>Successfully executed query."
        result += "<br/>Successfully read <pre>" + str(cursor.fetchone()) + "<pre> !"
        result += "<h1>Success!</h1>"
        cursor.close()
        connection.close()
        
    except Exception as e:
        result += "<br/><h1>Failure:</h1><br/><pre>"
        result += traceback.format_exc()
        result += "</pre>"

    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0')
