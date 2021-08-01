import requests
from django.shortcuts import redirect, render
from django.contrib import messages


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
                    request, 'Username cannot consist "₴@~#$%&*,<>"!?\\/|+')
                return redirect('getLogin')

        headers = {"Authorization": "bearer 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"}
        query = """
        {
          user(login: "%s") {
            name
            repositories(first: 100) {
              nodes{
                name
              }
            }
          }
        }
        """ % username
        url = 'https://api.github.com/graphql'

        req = requests.post(url, json={'query': query}, headers=headers)
        req = req.json()

        repos = []
        r = req.pop('data')
        if r['user'] != None:
            r = r.pop('user')
            full_name = r['name']
            for el in r['repositories'].pop('nodes'):
                repos.append(el['name'])
        else:
            messages.error(
                request, 'User with username "{}" does not exist.'.format(username))
            return redirect('getLogin')

        context = {
            'name': full_name,
            'repos': repos,
        }
        return render(request, 'search/index.html', context)

    return render(request, 'search/index.html')
