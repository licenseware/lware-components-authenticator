import requests
import logging
import os


class Authenticator:

    """
    
    This class can be used for Licenseware authentification.

    Set login values in environment variables:
    - LWARE_IDENTITY_USER (the email)
    - LWARE_IDENTITY_PASSWORD (the password)

    Otherwise you can pass them directly into Authenticator (not recommended).
    - email
    - password

    If you are using environment variables you can login like this:
    ```py
    
    from authenticator import Authenticator

    response = Authenticator.connect()
    # check response

    ``` 

    Or like this if you are not using environment variables:
    
    ```py
    
    from authenticator import Authenticator

    response = Authenticator(
        email="email@company.com", password="not recommended"
    ).connect()

    # check response
    

    ```

    """

    def __init__(
        self, 
        email=None, 
        password=None, 
        auth_url=None,
        debug=False
    ):
        
        self.email = email or os.getenv("LWARE_IDENTITY_USER")
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
        
        return response


    def login(self):

        identity = "email" if "/auth/users" in self.auth_url else "machine_name"
        payload = {
            identity: self.email,
            "password": self.password
        }
        
        self.show_logs(payload)
        response = requests.post(url=f'{self.auth_url}/login', json=payload)
        self.show_logs(response.content)

        if response.status_code == 200:
            return response.json()
        else:
            return self.create_user()


    def create_user(self):

        if "/auth/users" in self.auth_url:
            return {
                "status": "fail", 
                "message": "Please create an account before using this sdk."
            }, 403

        payload = {
            "machine_name": self.email,
            "password": self.password
        }
        
        self.show_logs(payload)
        response = requests.post(url=f'{self.auth_url}/create', json=payload)
        
        if response.status_code == 201:
            return response.json()
    
        self.show_logs(response.content)
        

    def show_logs(self, debug_info):
        if self.debug: logging.warning(debug_info)

