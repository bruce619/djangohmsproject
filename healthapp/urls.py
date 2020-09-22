from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from healthapp.views.patient import PatientCreateView, PatientListView, PatientDetailView, PatientUpdateView, \
    PatientDeleteView, Trash, restore, record_status_discharge, record_status_admit, MedicalHistoryCreateView, \
    MedicalHistoryListView, MedicalHistoryUpdateView, MedicalHistoryDeleteView, MedicalTrashList, med_history_restore
from healthapp.views.home import home


urlpatterns = [
    path('', home, name='home'),
    path('create-patient/', PatientCreateView.as_view(), name='create-patient'),
    path('patient-list/', PatientListView.as_view(), name='patient-list'),
    path('patient-detail/<int:id>/', PatientDetailView.as_view(), name='patient-detail'),
    path('patient/<int:id>/update/', PatientUpdateView.as_view(), name='patient-update'),
    path('patient/<int:pk>/delete/', PatientDeleteView.as_view(), name='patient-delete'),
    path('patient-trash-list/', Trash.as_view(), name='patient-trash-list'),
    path('patient-restore/<int:id>/', restore, name='patient-restore'),
    path('record-status-discharge/<int:id>/', record_status_discharge, name='record-status-discharge'),
    path('record-status-admit/<int:id>/', record_status_admit, name='record-status-admit'),
    path('patient/<int:patient_id>/medical-history/', MedicalHistoryCreateView.as_view(), name='create-medical-history'),
    path('medical/<int:patient_id>/history-list/', MedicalHistoryListView.as_view(), name='medical-history-list'),
    path('update-medical/<int:patient_id>/history/', MedicalHistoryUpdateView.as_view(), name='medical-history-update'),
    path('delete-medical/<int:pk>/history/', MedicalHistoryDeleteView.as_view(), name='medical-history-delete'),
    path('medical-trash-list/', MedicalTrashList.as_view(), name='medical-trash-list'),
    path('medical-history-restore/<int:id>/', med_history_restore, name='med-history-restore'),

]
#  Saves static files in static folder
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)