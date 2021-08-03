import requests
from django.shortcuts import redirect, render
from django.contrib import messages
from django.conf import settings
from django.views.generic import View

from .utils import get_query, process_response


class GetLogin(View):
    def get(self, request):
        return render(request, 'search/index.html')

    def post(self, request):
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

        req = process_response(username)
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

        context = {
            'login': username,
            'name': full_name,
            'avatar': avatar,
            'repos': repos,
        }
        return render(request, 'search/index.html', context)
