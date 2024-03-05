from flask import Flask
import requests

app = Flask(__name__)

@app.route('/metadata', methods=['GET'])
def return_instance_metadata():

    token_response = requests.put("http://169.254.169.254/latest/api/token", headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"})
    token = token_response.text

    metadata_url = "http://169.254.169.254/latest/meta-data/"
    metadata_response = requests.get(metadata_url, headers={"X-aws-ec2-metadata-token": token})

    return (metadata_response.text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)