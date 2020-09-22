import django_filters
from .models import Patient, MedicalHistory


class PatientFilter(django_filters.FilterSet):

    class Meta:
        model = Patient
        fields = ('id',)
        labels = {
            'id': 'Patient ID',
        }


class MedicalFilter(django_filters.FilterSet):

    class Meta:
        model = MedicalHistory
        fields = ('patient_id',)
