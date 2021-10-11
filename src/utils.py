import json


def get_token(token_path):
    """retorna o token para autenticar o bot do telegram"""
    token = ''

    with open(token_path , 'r') as json_file: 
        data = json.load(json_file)

        token = data['token']

    return token 