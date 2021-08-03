from django.conf import settings
import requests


def get_query(username):
    query = """
    {
      user(login: "%s") {
        name
        avatarUrl
        repositories(first: 100) {
          nodes{
            name
          }
        }
      }
    }
    """ % username

    return query


def url_exists(url):
    r = requests.get(url)
    if r.status_code == 200:
        return True

    elif r.status_code == 404:
        return False


def process_response(username):
    query = get_query(username)
    headers = {"Authorization": settings.GITHUB_TOKEN}
    url = settings.GITHUB_API_URL
    r = requests.post(url, json={'query': query}, headers=headers)
    return r
