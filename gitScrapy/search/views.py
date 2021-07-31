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

        user = requests.get(
            'https://api.github.com/users/{}'.format(username))

        if not user:
            messages.error(
                request, 'User with username "{}" does not exist.'.format(username))
            return redirect('getLogin')

        repos = requests.get(
            'https://api.github.com/users/{}/repos'.format(username))

        repo_list = []
        for repo in repos.json():
            repo_list.append(repo['name'])

        context = {
            'name': user.json()['name'],
            'repos': repo_list
        }
        return render(request, 'search/index.html', context)

    return render(request, 'search/index.html')
