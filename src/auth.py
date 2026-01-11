import os
import webbrowser
from fyers_apiv3 import fyersModel
from dotenv import load_dotenv

load_dotenv()

def get_fyers_session():
    client_id = os.getenv("FYERS_CLIENT_ID")
    secret_key = os.getenv("FYERS_SECRET_KEY")
    redirect_uri = os.getenv("FYERS_REDIRECT_URI")
    
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type="code",
        grant_type="authorization_code",
        state="sample"
    )
    return session

def generate_access_token(auth_code):
    client_id = os.getenv("FYERS_CLIENT_ID")
    secret_key = os.getenv("FYERS_SECRET_KEY")
    redirect_uri = os.getenv("FYERS_REDIRECT_URI")
    
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type="code",
        grant_type="authorization_code"
    )
    session.set_token(auth_code)
    response = session.generate_token()
    return response.get("access_token")