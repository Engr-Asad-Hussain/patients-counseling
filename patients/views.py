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
    """
    Endpoint to handle the retrieval and creation of patients.\n
    Args:
        - request (Request): The HTTP request object.
    """

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
    """
    Endpoint to retrieve, update, or delete a specific patient.\n
    Args:
        - request (Request): The HTTP request object.
        - uid (int): The unique identifier of the patient returns from url-params.
    Note:
        - Deletion will result in `in_active` state to `False`
    """

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
    """ API endpoints for interacting with Counsellors. """

    def get(self, request: Request) -> Response:
        """
        Get endpoint to retrieve a list of active counsellors.\n
        Args:
            - request (Request): The HTTP request object.
        """

        # Collect all counsellors from models
        counsellors = Counsellor.objects.filter(is_active=True)

        # Serialize Counsellors
        serializer = CounsellorSerializer(counsellors, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """
        Post endpoint to create a new counsellor.\n
        Args:
            - request (Request): The HTTP request object.
        """

        # Validate Schema
        request_body = request.data
        serializer = CreateCounsellorSerializer(data=request_body)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Commit Payload
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SpecificCounsellorApi(APIView):
    """ API endpoint for interacting with specific Counsellors. """

    def _get_counsellor(self, pk: int) -> Counsellor:
        """ Method to retrieve a specific counsellor by Primary-Key. """

        return Counsellor.objects.get(pk=pk)

    def get(self, request: Request, uid: int) -> Response:
        """
        Get endpoint to handle the retrieval of counsellor.\n
        Args:
            - request (Request): The HTTP request object.
            - uid (int): The unique identifier of the counsellor returns from url-params.
        """
        
        try:
            counsellor = self._get_counsellor(uid)
        except Counsellor.DoesNotExist:
            message = {"message": "Counsellor does not exists."}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        # Serialize Counsellor
        serializer = CounsellorSerializer(counsellor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, uid: int) -> Response:
        """
        Put endpoint to handle the update of counsellor.\n
        Args:
            - request (Request): The HTTP request object.
            - uid (int): The unique identifier of the counsellor returns from url-params.
        """

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
        """
        Delete endpoint to handle the deletion of counsellor.\n
        Args:
            - request (Request): The HTTP request object.
            - uid (int): The unique identifier of the counsellor returns from url-params.\n
        Note:
            - Deletion will result in `in_active` state to `False`
        """

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
    """ API endpoint for interacting with appointments. """

    def get(self, request: Request) -> Response:
        """
        Get endpoint to retrieve a list of appointments based on optional query parameters.\n
        Args:
            - request (Request): The HTTP request object.\n
        Query Parameters:
            - `patient_id`: Retrieve appointments for a specific patient.
            - `counsellor_id`: Retrieve appointments for a specific counsellor.
            - `start_date`: Filter appointments starting from the specified date.
            - `end_date`: Filter appointments until the specified date.
            - `sort`: Sort appointments by date in ascending/descending order.
        """

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
        """
        Post endpoint to create a new appointment.
        Args:
            - request (Request): The HTTP request object.
        """

        request_body = request.data
        serializer = CreateAppointmentSerializer(data=request_body)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SpecificAppointmentApi(APIView):
    """ API endpoint for interacting with specific Appointments. """

    def _get_appointment(self, pk: int) -> Appointment:
        """ Method to retrieve a specific appointment by Primary-Key. """

        return Appointment.objects.get(pk=pk)

    def get(self, request: Request, uid: int) -> Response:
        """
        Get endpoint to handle the retrieval of appointment.\n
        Args:
            - request (Request): The HTTP request object.
            - uid (int): The unique identifier of the appointment returns from url-params.
        """

        try:
            appointment = self._get_appointment(uid)
        except Appointment.DoesNotExist:
            message = {"message": "Appointment does not exists."}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        # Serialize Appointment
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    def delete(self, request: Request, uid: int) -> Response:
        """
        Delete endpoint to handle the deletion of a.\n
        Args:
            - request (Request): The HTTP request object.
            - uid (int): The unique identifier of the appointment returns from url-params.\n
        Note:
            - Deletion will result in `in_active` state to `False`
        """

        try:
            appointment = self._get_appointment(uid)
        except Appointment.DoesNotExist:
            message = {"message": "Appointment does not exists."}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        appointment.delete()
        message = {"message": "Appointment has been deleted."}
        return Response(message, status=status.HTTP_200_OK)
