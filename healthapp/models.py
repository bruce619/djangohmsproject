from django.db import models
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE
from django.utils import timezone

GENDER = (
    ('male', 'Male'),
    ('male', 'Female'),
    ('unisex', 'Unisex'),
)

BLOOD_GROUP = (
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
)


class Patient(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(default=timezone.now)
    address = models.CharField(max_length=300)
    gender = models.CharField(choices=GENDER, max_length=20)
    phone_number = models.CharField(max_length=15)
    blood_group = models.CharField(choices=BLOOD_GROUP, max_length=10)
    genotype = models.CharField(max_length=50)
    record_status = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.first_name + " " + self.last_name


class MedicalHistory(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)
    medical_problem = models.CharField(max_length=50)
    allergies = models.CharField(max_length=50)
    medications = models.CharField(max_length=50)
    comment = models.CharField(max_length=50)

    def __unicode__(self):
        return self.patient.name

