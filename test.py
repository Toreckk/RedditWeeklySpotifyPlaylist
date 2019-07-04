auth_params = {
        "client_id" : "CLIENT_ID",
        "response_type": "code",
        "redirect_uri": "http://127.0.0.1/8080/callback/q",
        "":"STATE", #OPTIONAL
        "scope":"SCOPE", #OPTIONAL
        "show_dialog":"SHOW_DIALOG" #OPTIONAL
    }

args = '&'.join('{}={}'.format(param, auth_params[param]) for param in auth_params)
print('---------------------------')
print(args)
print('---------------------------')