import pytest
import numpy as np

from cat import Sheet, get_config, read_google_sheet, q, compose_answer

def test_get_config():
    config = get_config()
    assert 'private_key' in config
    assert 'client_email' in config
    assert 'token_uri' in config
    assert 'scopes' in config
    assert 'spreadsheet_id' in config
    assert 'range_name' in config

def test_read_google_sheet():
    config = get_config()
    config["range_name"] = "A1"
    sheet = read_google_sheet(config)
    assert sheet[0] == 'Ubicación'

@pytest.fixture
def sheet_model():
    sheet = np.array([ 
        ['101','film'],
        ['102','CaSe'],
        ['103','film 2'],
        ['104','film 3'],
        ['105','El señor de los anillos'],
        ['106','El señor Smith'],
    ])
    return sheet

def test_q_case_insensitive(sheet_model):
    sel = q(sheet_model,'cAsE')
    assert len(sel) == 1
    assert sel[0,0] == '102'
    assert sel[0,1] == 'CaSe'

def test_q_more_than_one_result(sheet_model):
    sel = q(sheet_model,'film')
    assert len(sel) == 3
    assert sel[0,0] == '101'
    assert sel[1,0] == '103'
    assert sel[2,0] == '104'

def test_q_more_than_one_word(sheet_model):
    sel = q(sheet_model,'señor anillos'.split())
    assert len(sel) == 1
    assert sel[0,0] == '105'
    sel = q(sheet_model,'anillos señor'.split())
    assert len(sel) == 1
    assert sel[0,0] == '105'

def test_q_no_words_to_search(sheet_model):
    sel = q(sheet_model,[])
    assert len(sheet_model) == len(sel)

def test_q_no_sheet_in_search(sheet_model):
    sel = q([],'any')
    assert sel == []

def test_compose_answer_film_not_found():
    sel = np.array([])
    assert compose_answer('film', sel) == 'No he encontrado la peli film'

def test_compose_answer_one_film_found():
    sel = np.array([['100','Matrix']])
    assert compose_answer('matrix', sel) == 'La peli Matrix está en el disco 100'

def test_compose_answer_four_films_found():
    sel = np.array([ 
        ['101','film 1'],
        ['102','film 2'],
        ['103','film 3'],
        ['104','film 4']
    ])
    assert compose_answer('matrix', sel) == 'Esto es lo que he encotrado: film 1 en el disco 101. film 2 en el disco 102. film 3 en el disco 103. film 4 en el disco 104.'

def test_compose_answer_too_many_answers():
    sel = np.array([ 
        ['101','film 1'],
        ['102','film 2'],
        ['103','film 3'],
        ['104','film 4'],
        ['105','film 5']
    ])
    assert compose_answer('film', sel) == f'demasiado coincidencias para film. Intenta ser más específico.'
