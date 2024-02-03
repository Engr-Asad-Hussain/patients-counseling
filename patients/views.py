from pprint import pprint
from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework.request import Request

from .serializers import (
    PatientSerializer,
    CreatePatientSerializer,
    CounsellorSerializer,
    CreateCounsellorSerializer,
    AppointmentSerializer,
    CreateAppointmentSerializer,
)
from .models import Counsellor, Patient, Appointment


@api_view(["GET", "POST"])
def all_patients(request: Request):
    if request.method == "GET":
        # Collect all patients from models
        patients = Patient.objects.filter(is_active=True)

        # Serialize Patients
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "POST":
        # Validate Schema
        request_body = request.data
        serializer = CreatePatientSerializer(data=request_body)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Commit Payload
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def specific_patient(request: Request, uid: int):
    try:
        patient = Patient.objects.get(pk=uid)
    except Patient.DoesNotExist:
        message = {"message": "Patient does not exists."}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        serializer = PatientSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "PUT":
        request_body = request.data
        serializer = PatientSerializer(patient, data=request_body, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Commit Payload
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "DELETE":
        patient.is_active = False
        patient.save()
        message = {"message": "Patient has been inactivated."}
        return Response(message, status=status.HTTP_200_OK)


class CounsellorApi(APIView):
    def get(self, request: Request) -> Response:
        # Collect all counsellors from models
        counsellors = Counsellor.objects.filter(is_active=True)

        # Serialize Counsellors
        serializer = CounsellorSerializer(counsellors, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        # Validate Schema
        request_body = request.data
        serializer = CreateCounsellorSerializer(data=request_body)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Commit Payload
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SpecificCounsellorApi(APIView):
    def _get_counsellor(self, pk: int) -> Counsellor:
        return Counsellor.objects.get(pk=pk)

    def get(self, request: Request, uid: int) -> Response:
        try:
            counsellor = self._get_counsellor(uid)
        except Counsellor.DoesNotExist:
            message = {"message": "Counsellor does not exists."}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        # Serialize Counsellor
        serializer = CounsellorSerializer(counsellor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, uid: int) -> Response:
        try:
            counsellor = self._get_counsellor(uid)
        except Counsellor.DoesNotExist:
            message = {"message": "Counsellor does not exists."}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        request_body = request.data
        serializer = CounsellorSerializer(counsellor, data=request_body, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Commit Payload
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, uid: int) -> Response:
        try:
            counsellor = self._get_counsellor(uid)
        except Counsellor.DoesNotExist:
            message = {"message": "Counsellor does not exists."}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        counsellor.is_active = False
        counsellor.save()
        message = {"message": "Counsellor has been inactivated."}
        return Response(message, status=status.HTTP_200_OK)


class AppointmentApi(APIView):
    def get(self, request: Request) -> Response:
        patient_id = request.query_params.get("patient_id")
        counsellor_id = request.query_params.get("counsellor_id")
        if patient_id is not None:
            appointments = Appointment.objects.filter(patient=patient_id)
        elif counsellor_id is not None:
            appointments = Appointment.objects.filter(counsellor=counsellor_id)
        else:
            appointments = Appointment.objects.all()

        # Filter appointments between the specified date range
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        try:
            start_date = (
                datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
                if start_date
                else None
            )
            end_date = (
                datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S") if end_date else None
            )
        except (TypeError, ValueError):
            return Response(
                {
                    "message": "Please provide datetime in valid format (%Y-%m-%dT%H:%M:%S)"
                }
            )

        if start_date is not None:
            appointments = appointments.filter(appointment_date__gte=start_date)

        if end_date is not None:
            appointments = appointments.filter(appointment_date__lte=end_date)

        # Sort appointments by date in descending order
        sort = request.query_params.get("sort", "-appointment_date")
        if sort in ("-appointment_date", "appointment_date"):
            appointments = appointments.order_by(sort)
        else:
            return Response(
                {"message": "Sort can be '-appointment_date' or 'appointment_date'"}
            )

        # Serialize Response
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        request_body = request.data
        serializer = CreateAppointmentSerializer(data=request_body)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SpecificAppointmentApi(APIView):
    def _get_appointment(self, pk: int) -> Appointment:
        return Appointment.objects.get(pk=pk)

    def get(self, request: Request, uid: int) -> Response:
        try:
            appointment = self._get_appointment(uid)
        except Appointment.DoesNotExist:
            message = {"message": "Appointment does not exists."}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        # Serialize Appointment
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    def delete(self, request: Request, uid: int) -> Response:
        try:
            appointment = self._get_appointment(uid)
        except Appointment.DoesNotExist:
            message = {"message": "Appointment does not exists."}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        appointment.delete()
        message = {"message": "Appointment has been deleted."}
        return Response(message, status=status.HTTP_200_OK)
