import requests

def wd_query(sprql: str):
    return requests.get('https://query.wikidata.org/sparql', params = {'format': 'json', 'query': sprql}).json()