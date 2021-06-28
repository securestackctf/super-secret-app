import os

import boto3
from flask import Flask, request, current_app, redirect
app = Flask(__name__)


@app.route('/<super_secret>')
def authenticate(super_secret):
    ssm = boto3.client('ssm', os.environ['AWS_REGION'])

    apikey = ssm.get_parameter(
        Name='/supersecretapp/password',
        WithDecryption=True
    )['Parameter']['Value']

    if super_secret == "":
        return current_app.send_static_file('auth.html')
    elif super_secret == apikey:
        return redirect('https://ctf.niftybank.org/%s/flag' % apikey, 301)


@app.route('/')
def super_secret():
    return current_app.send_static_file('index.html')


if __name__ == '__main__':
    app.run()