import sys
import requests
import click
from tqdm import tqdm
from ansimarkup import ansiprint as print
from app.export import export_date_medici


url_root = ''
token_auth = ''
token_refresh = ''

@click.command()
@click.option('--api', default='http://localhost:5000/api/v2',  help="root url api\ndefault: http://localhost:5000/api/v2")
@click.option('--tip', default='xlsx', help="tip fisier export\nOptiuni: json, csv, xlsx. \nDefault: xlsx")
@click.option('--email', prompt='Email', help='adresa de email folosita pentru autentificare')
@click.password_option(confirmation_prompt=False, help='parola folosita pentru autentificare')
def app_run(api, tip, email, password):
    # autenficare in api
    # get lista cuim
    # for each get data daca nu are limita
    # write json fil
    url_root = api
    auth(url_root, email, password)
    lista_medic = get_lista_medic(url_root)
    date_medici = get_date_medici(url_root, lista_medic)
    export_date_medici(tip, date_medici)

def get_data_from_api(tip, url, data):
    if tip == 'post':
        try:
            request = requests.post(url, json=data)
        except requests.exceptions.HTTPError as exc:  # This is the correct syntax
            print(exc)
            sys.exit(1)
    else:
        try:
            request = requests.get(url, headers=data)
        except requests.exceptions.HTTPError as exc:  # This is the correct syntax
            print(exc)
            sys.exit(1)
    return data

def auth(url_root, email, password):
    url_auth = url_root + '/autentificare/login'

    data = {
        'email': email,
        'password': password
    }
    
    try:
        request = requests.post(url_auth, json=data)
    except requests.exceptions.HTTPError as exc:  # This is the correct syntax
        print(exc)
        sys.exit(1)

    if request.status_code == 200:
        token_refresh = request.json()['refresh_token']
        token_access = request.json()['access_token']
        print(f'<green>** raspuns server:</green> {request.json()["msg"]}')
    else:
        print(f'<red>** adresa:</red> {request.url}')
        print(f'<red>** raspuns server:</red> {request.text}')
        sys.exit()

def set_headers(tip):
    if tip == 'auth':
        req_headers = {
            'Authorization': f'Bearer {token_access}'
        }
    else:
        req_headers = {
            'Authorization': f'Bearer {token_refresh}'
        }
    return req_headers

def auth_refresh_token(url_root, token_refresh):
    url = url_root + '/autentificare/refresh'
    req_headers = set_headers('refresh')
    request = requests.post(url, headers=req_headers)

    if request.status != 200:
        print(f'<red>** raspuns s:erver:</red> {request.json()["msg"]}')
        sys.exit()

    print(f'<green>** raspuns server:</green> {request.json()["msg"]}')
    token_auth = request.json()["access_token"]

def get_lista_medic(url_root):
    url = url_root + '/cmj/raport/lista_medic'
    lista_medic = []

    req_headers = set_headers('auth')
    request = requests.get(url, headers=req_headers)

    if request.status_code == 404:
        print(f'<red>** adresa api este incorecta</red> {request.url}')
        sys.exit()
    if request.status_code == 401:
        print(f'<yellow>** token-ul de access a expirat</yellow>')
        auth_token = auth_refresh_token(url_root, token_refresh)

        request = requests.get(url, headers=req_headers)

    if request.status_code == 200:
        lista_medic = request.json()['lista_medic']
        print(f'<green>** server.</green> get lista medici id <green>OK</green>')
        
    return lista_medic

def get_date_medici(url_root, lista_medic):
    date_medici = []
    for id in enumerate(tqdm(lista_medic)):
        
        url = url_root + f'/medic/{id[1]}'
        req_headers = {
            'Authorization': f'Bearer {token_access}'
        }
        request = requests.get(url, headers=req_headers)

        if request.status_code == 401:
            print(f'<yellow>** token-ul de access a expirat</yellow>')
            token_access = auth_refresh_token(url_root, token_refresh)
            req_headers = {
                    'Authorization': f'Bearer {token_access}'
                }
            request = requests.get(url, headers=req_headers)
            if request.status_code != 200:
                    print(f'<red>** adresa:</red> {request.url}')
                    print(f'<red>** raspuns server:</red> {request.text}')

        date_medici.append(request.json()['medic'])

    return date_medici
