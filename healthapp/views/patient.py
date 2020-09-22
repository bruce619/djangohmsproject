from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from healthapp.models import Patient, MedicalHistory
from healthapp.forms import PatientForm, MedicalHistoryForm
from django.contrib.auth.decorators import login_required
from ..filters import PatientFilter
from django_filters.views import FilterView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
import sweetify


class PatientCreateView(CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'create-patient-form.html'
    extra_context = {
        'title': 'Create New Patient'
    }

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PatientCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        sweetify.success(self.request, title='Patient Created', icon='success', button='Ok', timer=3000)
        return reverse_lazy('patient-list')


class PatientListView(FilterView, LoginRequiredMixin):
    model = Patient
    template_name = 'patient-list.html'
    filterset_class = PatientFilter
    ordering = ['-date_created']
    paginate_by = 5
    strict = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PatientFilter(self.request.GET, queryset=self.get_queryset())
        query = self.request.GET.copy()
        if 'page' in query:
            del query['page']
        context['queries'] = query
        return context


class PatientDetailView(DetailView):
    model = Patient
    template_name = 'patient-detail.html'
    pk_url_kwarg = 'id'


class PatientUpdateView(UpdateView, LoginRequiredMixin):
    model = Patient
    fields = ('first_name', 'middle_name', 'last_name', 'date_of_birth', 'address', 'gender', 'phone_number',
              'blood_group', 'genotype', 'record_status',)
    template_name = 'update-patient-form.html'
    pk_url_kwarg = 'id'
    slug_field = 'id'

    def get_form(self, **kwargs):
        form = super().get_form(**kwargs)
        form.fields['record_status'].label = "Treated and Discharged"
        return form

    def get_success_url(self):
        sweetify.success(self.request, title='Patient Updated', icon='success', button='Ok', timer=3000)
        return reverse_lazy('patient-detail', kwargs={'id': self.kwargs['id']})


class PatientDeleteView(DeleteView, LoginRequiredMixin):
    model = Patient
    template_name = 'patient-confirm-delete.html'

    def get_success_url(self):
        sweetify.success(self.request, title='Patient Deleted', icon='success', button='Ok', timer=3000)
        return reverse_lazy('patient-list')


class Trash(FilterView, LoginRequiredMixin):
    model = Patient
    template_name = 'patient-trash-list.html'
    filterset_class = PatientFilter
    ordering = ['-id']
    paginate_by = 2
    strict = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PatientFilter(self.request.GET, queryset=self.get_queryset())
        query = self.request.GET.copy()
        if 'page' in query:
            del query['page']
        context['queries'] = query
        return context

    def get_queryset(self):
        return Patient.objects.deleted_only().order_by('-id')


@login_required(login_url=reverse_lazy('login'))
def restore(request, id=None):
    # Gets the patient ID posted by (Admin/HR/Staff)
    patient = Patient.objects.deleted_only()
    patient = get_object_or_404(patient, pk=id)
    patient.undelete()
    sweetify.success(request, title='Patient Restored', icon='success', button='Ok', timer=3000)
    return HttpResponseRedirect(reverse_lazy('patient-trash-list'))


@login_required(login_url=reverse_lazy('login'))
def record_status_discharge(request, id=None):
    # Gets the the job posted by the logged in user(Admin/HR/Staff)
    patient = get_object_or_404(Patient, id=id)
    # Mark as record status as discharged
    patient.record_status = True
    patient.save()
    return redirect('patient-detail', id=id)


@login_required(login_url=reverse_lazy('login'))
def record_status_admit(request, id=None):
    # Gets the the job posted by the logged in user(Admin/HR/Staff)
    patient = get_object_or_404(Patient, id=id)
    # Mark as record status as discharged
    patient.record_status = False
    patient.save()
    return redirect('patient-detail', id=id)


class MedicalHistoryCreateView(LoginRequiredMixin, CreateView):
    model = MedicalHistory
    form_class = MedicalHistoryForm
    slug_url_kwarg = 'patient_id'
    slug_field = 'patient_id'
    template_name = 'medical-history-form.html'
    extra_context = {
        'title': 'Create Medical History'
    }

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        patient = get_object_or_404(Patient, id=self.kwargs['patient_id'])
        form.instance.user = self.request.user
        medicalhistory = form.save(commit=False)
        medicalhistory.patient = patient
        medicalhistory.save()
        return super(MedicalHistoryCreateView, self).form_valid(form)

    def get_success_url(self):
        sweetify.success(self.request, title='Medical Record Created', icon='success', button='Ok', timer=3000)
        return reverse_lazy('patient-detail', kwargs={'id': self.kwargs['patient_id']})


class MedicalHistoryListView(ListView, LoginRequiredMixin):
    model = MedicalHistory
    template_name = 'medical-history-list.html'
    context_object_name = 'medicalhistory'
    ordering = ['-created_on']
    paginate_by = 2

    def get_queryset(self):
        return MedicalHistory.objects.filter(patient_id=self.kwargs['patient_id']).distinct().order_by('-created_on')


class MedicalHistoryUpdateView(UpdateView, LoginRequiredMixin):
    model = MedicalHistory
    fields = ('medical_problem', 'allergies', 'medications', 'comment', 'updated_on')
    template_name = 'update-medical-history-form.html'
    slug_url_kwarg = 'patient_id'
    slug_field = 'patient_id'

    def get_form(self, **kwargs):
        form = super().get_form(**kwargs)
        return form

    def get_success_url(self):
        sweetify.success(self.request, title='Medical History Updated', icon='success', button='Ok', timer=3000)
        return reverse_lazy('medical-history-list', kwargs={'patient_id': self.kwargs['patient_id']})


class MedicalHistoryDeleteView(DeleteView, LoginRequiredMixin):
    model = MedicalHistory
    template_name = 'medical-history-confirm-delete.html'

    def get_success_url(self):
        sweetify.success(self.request, title='Record Deleted', icon='success', button='Ok', timer=3000)
        return reverse_lazy('patient-list')


class MedicalTrashList(ListView, LoginRequiredMixin):
    model = MedicalHistory
    template_name = 'medical-trash-list.html'
    paginate_by = 5
    context_object_name = 'medicalhistory'
    slug_url_kwarg = 'patient_id'
    slug_field = 'patient_id'

    def get_queryset(self):
        return MedicalHistory.objects.deleted_only().distinct().order_by('-created_on')


@login_required(login_url=reverse_lazy('login'))
def med_history_restore(request, id=None):
    # Gets the patient ID posted by (Admin/HR/Staff)
    med_history = MedicalHistory.objects.deleted_only()
    med_history = get_object_or_404(med_history, pk=id)
    med_history.undelete()
    sweetify.success(request, title='Medical History Restored', icon='success', button='Ok', timer=3000)
    return HttpResponseRedirect(reverse_lazy('medical-trash-list'))

