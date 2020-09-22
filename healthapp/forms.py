from django import forms
from healthapp.models import Patient, MedicalHistory


class PatientForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(PatientForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['date_of_birth'].required = True
        self.fields['gender'].required = True
        self.fields['blood_group'].required = True
        self.fields['genotype'].required = True

    class Meta:
        model = Patient
        fields = ('first_name', 'middle_name', 'last_name', 'date_of_birth', 'address', 'gender', 'phone_number',
                  'blood_group', 'genotype', )
        labels = {
            'first_name': 'First Name',
            'middle_name': 'Middle Name',
            'last_name': 'Last Name',
            'date_of_birth': 'Date of Birth',
            'address': 'Residential Address',
            'gender': 'Gender',
            'phone_number': 'Phone Number',
            'blood_group': 'Blood Group',
            'genotype': 'Genotype',

        }


class MedicalHistoryForm(forms.ModelForm):

    class Meta:
        model = MedicalHistory
        fields = ('patient', 'medical_problem', 'allergies', 'medications', 'comment',)
        exclude = ('patient', 'created_on', 'updated_on',)
        labels = {
            'medical_problem': 'Medical Problems',
            'allergies': 'Allergies',
            'medications': 'Medications',
            'comment': 'Comments/Recommendations',
            'created_on': 'Created On',
            'updated_on': 'Updated On',
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)