from requests import auth


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')