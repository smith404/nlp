import requests

response = requests.get(
    'https://en.wikipedia.org/w/api.php',
    params={
    'action': 'query',
    'format': 'json',
    'titles': 'Middlesbrough',
    'prop': 'extracts',
    'exintro': True,
    'explaintext': True,
    }
).json()

page = next(iter(response['query']['pages'].values()))
print(page['extract'])