import os
import re

from typing import TypeVar

import numpy as np

from google.oauth2 import service_account
import googleapiclient.discovery

Sheet = np.ndarray

def get_config():
    config = {
        "private_key":      os.environ["GOOGLE_PRIVATE_KEY"].replace('\\n', '\n'), # The environment variable has escaped newlines, so remove the extra backslash
        "client_email":     os.environ["GOOGLE_CLIENT_EMAIL"],
        "token_uri":        "https://accounts.google.com/o/oauth2/token",
        "scopes":           ["https://www.googleapis.com/auth/spreadsheets.readonly"],
        "spreadsheet_id":   os.environ["GOOGLE_SPREADSHEET_ID"],
        "range_name":       os.environ["GOOGLE_SPREADSHEET_RANGE"],
    }

    return config

def read_google_sheet(config):
    account_info = {
        "private_key":  config["private_key"],
        "client_email": config["client_email"],
        "token_uri":    config["token_uri"],
    }
    service_name = 'sheets'
    api_version = 'v4'

    credentials = service_account.Credentials.from_service_account_info(account_info, scopes=config["scopes"])
    service = googleapiclient.discovery.build(service_name, api_version, credentials=credentials)
    result = service.spreadsheets().values().get(spreadsheetId=config["spreadsheet_id"], range=config["range_name"]).execute()
    return np.array(result.get('values', []))

def q(sheet, any):
    if len(sheet) == 0 or len(any) == 0:
        return sheet

    head, *tail = any
    name = head.lower() 
    r = re.compile(f'.*{name}.*')
    vmatch = np.vectorize(lambda x:bool(r.match(x.lower())))
    if len(tail) == 0:
        return sheet[vmatch(sheet[:,1])]
    else:
        return q(sheet[vmatch(sheet[:,1])],tail)

def compose_answer(name, sel):
    n = len(sel)

    if n == 0:
        answer = f'No he encontrado la peli {name}'
    elif n == 1:
        answer = f'La peli ' + sel[0,1] + ' está en el disco ' + sel[0,0]
    elif n > 4:
        answer = f'demasiado coincidencias para {name}. Intenta ser más específico.'
    else:
        answer = 'Esto es lo que he encotrado:'
        for row in sel:
            answer = answer + ' ' + row[1] + ' en el disco ' + row[0] + '.'
    
    return answer
