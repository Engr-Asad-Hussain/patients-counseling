from typing import Any
from rest_framework import serializers
from .models import Patient, Counsellor, Appointment
from collections import OrderedDict


class CreatePatientSerializer(serializers.ModelSerializer):
    """Serializer for POST request - to make name, email, password as required."""

    class Meta:
        model = Patient
        fields = "__all__"


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for GET/PUT - to return specific properties in response."""

    class Meta:
        model = Patient
        fields = ["id", "name", "email", "is_active"]
        read_only_fields = ["email"]
        # read_only_fields prevent field(s) from being changed in an update(PUT)


class CreateCounsellorSerializer(serializers.ModelSerializer):
    """Serializer for POST request - to make name, email, password as required."""

    class Meta:
        model = Counsellor
        fields = "__all__"


class CounsellorSerializer(serializers.ModelSerializer):
    """Serializer for GET/PUT - to return specific properties in response."""

    class Meta:
        model = Counsellor
        fields = ["id", "name", "email", "is_active"]
        read_only_fields = ["email"]


class CreateAppointmentSerializer(serializers.ModelSerializer):
    """Serializer for POST request - to make counsellor/patient's id as required."""

    class Meta:
        model = Appointment
        fields = "__all__"

    def validate(self, attrs: OrderedDict[Any, Any]):
        # Check if the appointment with the same patient and counsellor already exists
        patient = attrs["patient"]
        counsellor = attrs["counsellor"]
        existing_appointment = Appointment.objects.filter(
            patient=patient, counsellor=counsellor, is_active=True
        ).first()
        if existing_appointment is not None:
            message = "Active appointment with the same patient and counsellor already exists."
            raise serializers.ValidationError({"appointment": message})

        # Check if the patient and counsellor are active
        if not patient.is_active:
            raise serializers.ValidationError(
                {"patient": f"The patient ({patient.email}) is not active."}
            )
        if not counsellor.is_active:
            raise serializers.ValidationError(
                {"counsellor": f"The counsellor ({counsellor.email}) is not active."}
            )

        return attrs


class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for GET - to return specific properties in response."""

    patient = PatientSerializer()
    counsellor = CounsellorSerializer()

    class Meta:
        model = Appointment
        fields = "__all__"
