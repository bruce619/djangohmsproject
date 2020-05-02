from django.shortcuts import render, redirect
from healthapp.forms import ContactForm
from django.core.mail import EmailMessage
from django.template.loader import get_template
import sweetify


def home(request):
    form_class = ContactForm
    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            name = request.POST.get(
                'name'
                , '')
            email = request.POST.get(
                'email'
                , '')
            message = request.POST.get('message', '')
            # Email the profile with the
            # contact information
            template = get_template('contact_template.txt')
            context = {
                'name': name,
                'email': email,
                'message': message,
            }
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "HEALTH FOR ALL" + '',
                ['petrobruz@gmail.com'],
                headers={'Reply-To': email}
            )
            email.send()
            sweetify.success(request, title='Sent', icon='success', button='Ok', timer=3000)
            return redirect('home')
    return render(request, 'home.html', {'form': form_class})


def error_404(request, exception):
    data = {}
    return render(request, 'error_404.html', data)


def error_500(request):
    data = {}
    return render(request, 'error_500.html', data)





