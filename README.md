# Authenticator (Beta)

This can be used to Licenseware authentification. Note that you must have already an account on [licenseware.io](https://licenseware.io/).


## Quickstart

Install this package using the following pip command:
```bash

pip3 install git+https://git@github.com/licenseware/lware-components-authenticator.git

```

You can add the link in a `requirements.txt` file. You can use `git+ssh` if you have ssh keys configured. 


Set login values in environment variables:
- LWARE_IDENTITY_USER (the email)
- LWARE_IDENTITY_PASSWORD (the password)
- AUTH_SERVICE_URL (the url for login)

Otherwise you can pass them directly into Authenticator (not recommended).
- email
- password
- auth_url

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
    email="email@company.com", 
    password="not recommended", 
    auth_url="https://licenseware.io/auth"
).connect()

# check response


```

The `response` will be json, status_code tuple.

