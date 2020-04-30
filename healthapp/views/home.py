from django.shortcuts import render


def home(request):
    return render(request, 'home.html', {})


def error_404(request, exception):
    data = {}
    return render(request, 'error_404.html', data)


def error_500(request):
    data = {}
    return render(request, 'error_500.html', data)





