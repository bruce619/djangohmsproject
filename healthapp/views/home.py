from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from healthapp.forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import get_template
import sweetify


def home(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            template = get_template('contact_template.txt')
            context = {
                'name': name,
                'email': email,
                'message': message,
            }
            content = template.render(context)
            try:
                send_mail(
                    "New contact form submission",
                    content,
                    "HEALTHFORALL" + '',
                    ['petrobruz@gmail.com'],
                    fail_silently=False,
                )
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            sweetify.success(request, title='Sent', icon='success', button='Ok', timer=3000)
            return redirect('home')

    return render(request, 'home.html', {'form': form})


def error_404(request, exception):
    data = {}
    return render(request, 'error_404.html', data)


def error_500(request):
    data = {}
    return render(request, 'error_500.html', data)





