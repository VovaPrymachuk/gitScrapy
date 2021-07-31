import requests
from django.shortcuts import redirect, render
from django.contrib import messages


def getLogin(request):
    if request.method == 'POST':
        username = request.POST['gitLogin']

        if username == '':
            messages.error(request, 'Please enter username!')
            return redirect('getLogin')

        users = requests.get(
            'https://api.github.com/users/{}'.format(username))
        repos = requests.get(
            'https://api.github.com/users/{}/repos'.format(username))

        repo_list = []
        for repo in repos.json():
            repo_list.append(repo['name'])

        print(repo_list)

        context = {
            'name': users.json()['name'],
            'repos': repo_list
        }
        return render(request, 'search/index.html', context)

    return render(request, 'search/index.html')
