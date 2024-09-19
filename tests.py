import requests
import os

API_KEY = os.getenv('API_KEY')

headers = {'x-api-key': API_KEY}

def test_parse_dmarc():
    url = 'http://localhost:8080/parse_dmarc'
    headers['Content-Type'] = 'application/json'
    data = {
        'dmarc_record': 'v=DMARC1; p=none; rua=mailto:reports@example.com'
    }
    response = requests.post(url, json=data, headers=headers)
    assert response.status_code == 200, f'Expected status code 200, got {response.status_code}'
    json_response = response.json()
    assert json_response.get('v') == 'DMARC1', 'Incorrect DMARC version parsed'
    assert json_response.get('p') == 'none', 'Incorrect policy parsed'
    assert json_response.get('rua') == 'mailto:reports@example.com', 'Incorrect RUA parsed'

def test_check_dmarc():
    url = 'http://localhost:8080/check_dmarc/example.com'
    response = requests.get(url, headers=headers)
    assert response.status_code in [200, 404], f'Unexpected status code {response.status_code}'
    if response.status_code == 200:
        json_response = response.json()
        assert json_response.get('v') == 'DMARC1', 'Incorrect DMARC version retrieved'
        assert 'p' in json_response, 'Policy not found in response'

if __name__ == '__main__':
    test_parse_dmarc()
    print('test_parse_dmarc passed')
    test_check_dmarc()
    print('test_check_dmarc passed')
