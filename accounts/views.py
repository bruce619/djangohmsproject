from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
import sweetify
from django.contrib.messages.views import SuccessMessageMixin
from accounts.forms import RegistrationForm, AccountUpdateForm, AccountAuthenticationForm
from django.views.generic import CreateView, FormView, RedirectView, UpdateView, ListView
from accounts.models import Account


class LoginView(FormView):
    """
        Provides the ability to login as a user with an email and password
    """
    success_url = reverse_lazy('home')
    form_class = AccountAuthenticationForm
    template_name = 'registration/login.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        if 'next' in self.request.GET and self.request.GET['next'] != '':
            sweetify.success(self.request, title='Logged In', icon='success', button='Ok', timer=3000)
            return self.request.GET['next']
        else:
            sweetify.success(self.request, title='Logged In', icon='success', button='Ok', timer=3000)
            return self.success_url

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/login'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        sweetify.success(request, title='Logged Out', icon='success', button='Ok', timer=3000)
        return super(LogoutView, self).get(request, *args, **kwargs)


class RegisterStaffUserView(CreateView):
    model = Account
    template_name = 'register.html'
    extra_context = {
        'title': 'Register'
    }

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            sweetify.success(self.request, title='Account Created', icon='success', button='Ok', timer=3000)
            return redirect('home')
        else:
            return render(request, 'register.html', {'registration_form': form})

    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        return render(request, 'register.html', {'registration_form': form})

    def get_success_url(self):
        return reverse_lazy('home')


class EditProfileView(SuccessMessageMixin, UpdateView):
    model = Account
    form_class = AccountUpdateForm
    template_name = 'profile.html'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()

        except Http404:
            raise Http404("User doesn't exists")
        # context = self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        obj = self.request.user
        print(obj)
        if obj is None:
            raise Http404("doesn't exists")
        return obj

    def get_success_url(self):
        sweetify.success(self.request, title='Account Updated', icon='success', button='Ok', timer=3000)
        return reverse_lazy('home')


class Staff(ListView):
    model = Account
    template_name = 'account_list.html'
    context_object_name = 'members'
    paginate_by = 7

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return Account.objects.all().order_by('-id')



