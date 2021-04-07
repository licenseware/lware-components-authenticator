import requests
import logging
import os

class Authenticator:

    """
        If init variables are not provided on class initialization it will try 
        to get from environment variables the following values:
        - LWARE_IDENTITY_USER
        - LWARE_IDENTITY_PASSWORD
        - AUTH_SERVICE_URL

        If environment variables are set then you can connect to licenseware with:
        ```
        
        Authenticator.connect()

        ```
        Otherwise specify parameters and call `login`:
        ```
        Authenticator(
            user="your user", 
            password="your password", 
            auth_url="authentification url"
        ).login()
        ```
    """

    def __init__(
        self, 
        user=None, 
        password=None, 
        auth_url=None,
        debug=False
    ):
        
        self.user = user or os.getenv("LWARE_IDENTITY_USER")
        self.password = password or os.getenv("LWARE_IDENTITY_PASSWORD")
        self.auth_url = auth_url or os.getenv("AUTH_SERVICE_URL")
        self.debug = debug

        
    @classmethod
    def connect(cls):
        response = cls().login()
        if response:
            cls().show_logs('Logged in')
            os.environ['AUTH_TOKEN'] = response["Authorization"]
            os.environ['TENANT_ID'] = response["TenantId"]
            os.environ['APP_AUTHENTICATED'] = 'true'
        else:
            os.environ['APP_AUTHENTICATED'] = 'false'
            cls().show_logs('Could not login')

    def login(self):
        payload = {
            "user": self.user,
            "lware_identity_password": self.lware_identity_password
        }

        self.show_logs(payload)
        response = requests.post(url=f'{self.auth_url}/login', json=payload)
        self.show_logs(response.content)

        if response.status_code == 200:
            return response.json()
        else:
            return self.create_user()

    def create_user(self):
        payload = {
            "user": os.getenv("user"),
            "password": os.getenv("LWARE_IDENTITY_lware_identity_password"),   
        }

        self.show_logs(payload)
        response = requests.post(url=f'{self.auth_url}/create', json=payload)
        
        if response.status_code == 201:
            return response.json()
    
        self.show_logs(response.content)
        

    def show_logs(self, debug_info):
        if self.debug: logging.warning(debug_info)

