import requests
from django.shortcuts import redirect, render
from django.contrib import messages
from django.conf import settings


def getLogin(request):
    if request.method == 'POST':
        username = request.POST['gitLogin']

        if username == '':
            messages.error(request, 'Please enter username!')
            return redirect('getLogin')

        exception = '₴@~#$%&*,<>!?\\/|+'
        for el in list(username):
            if el in exception:
                messages.error(
                    request, 'Username cannot consist "₴@~#$%&*,<>!?\\/|+"')
                return redirect('getLogin')

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

        headers = {"Authorization": settings.GITHUB_TOKEN}
        url = settings.GITHUB_API_URL

        req = requests.post(url, json={'query': query}, headers=headers)
        req = req.json()

        repos = []
        r = req.pop('data')
        if r['user'] is not None:
            r = r.pop('user')
            full_name = r['name']
            avatar = r['avatarUrl']
            for el in r['repositories'].pop('nodes'):
                repos.append(el['name'])
        else:
            messages.error(
                request,
                'User with username "{}" does not exist.'.format(username))
            return redirect('getLogin')

        print('...............................................')
        print(avatar)

        context = {
            'login': username,
            'name': full_name,
            'avatar': avatar,
            'repos': repos,
        }
        return render(request, 'search/index.html', context)

    return render(request, 'search/index.html')
