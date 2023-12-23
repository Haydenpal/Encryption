from flask import Flask, render_template, request, redirect, url_for, session
import boto3
from werkzeug.utils import secure_filename
import requests

app = Flask(__name__)

# Initialize S3 and Cognito clients
s3 = boto3.client('s3')
cognito = boto3.client('cognito-idp')

# AWS configurations
AWS_REGION = 'us-west-1'
COGNITO_CLIENT_ID = '37logoufcen7j54bg083b385gr'
COGNITO_USER_POOL_ID = 'us-west-1_gmWPINN0h'
S3_BUCKET_NAME = 'hayden1104200301'
REDIRECT_URL = 'http://localhost:5000/callback'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            filename = secure_filename(uploaded_file.filename)
            s3.upload_fileobj(uploaded_file, S3_BUCKET_NAME, filename)

            user_id = request.form.get('user_id')
            username = request.form.get('username')
            password = request.form.get('password')
            # Logic for user signup using Cognito can be added here if needed

            return redirect(url_for('success'))
        else:
            return "No file uploaded", 400
    else:
        return "Method Not Allowed", 405

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if code:
        token_endpoint = f"https://{AWS_REGION}.amazoncognito.com/oauth2/token"
        
        response = requests.post(
            token_endpoint,
            data={
                "grant_type": "authorization_code",
                "client_id": COGNITO_CLIENT_ID,
                "code": code,
                "redirect_uri": REDIRECT_URL
            }
        )

        if response.status_code == 200:
            tokens = response.json()
            access_token = tokens.get('access_token')
            id_token = tokens.get('id_token')
            # Implement logic to verify and decode the ID token if needed

            return redirect(url_for('index'))
        else:
            return "Error occurred during authentication", 500
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    logout_url = f'https://{AWS_REGION}.amazoncognito.com/logout?client_id={COGNITO_CLIENT_ID}&logout_uri={REDIRECT_URL}'
    return redirect(logout_url)

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/files')
def list_files():
    # Use boto3 to list objects in the bucket
    objects = s3.list_objects_v2(Bucket=S3_BUCKET_NAME)

    # Extract file names from the response
    if 'Contents' in objects:
        files = [obj['Key'] for obj in objects['Contents']]
    else:
        files = []

    return render_template('files.html', files=files)

if __name__ == '__main__':
    app.run(debug=True)
