from django.urls import path

from .views import (
    all_patients,
    specific_patient,
    CounsellorApi,
    SpecificCounsellorApi,
    AppointmentApi,
    SpecificAppointmentApi,
)

urlpatterns = [
    path("patients/", all_patients),
    path("patients/<int:uid>/", specific_patient),
    path("counsellors/", CounsellorApi.as_view()),
    path("counsellors/<int:uid>/", SpecificCounsellorApi.as_view()),
    path("appointments/", AppointmentApi.as_view()),
    path("appointments/<int:uid>/", SpecificAppointmentApi.as_view()),
]
