from django.shortcuts import render


def getLogin(request):
    if request.method == 'POST':
        username = request.POST['gitLogin']
        context = {
            'username': username
        }
        print(type(context), context['username'])
        return render(request, 'search/result.html', context)

    return render(request, 'search/index.html')
