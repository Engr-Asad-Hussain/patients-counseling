from django.db import models
from django.core.validators import RegexValidator


class Patient(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(
        max_length=256,
        validators=[
            RegexValidator(
                regex=r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$",
                message="Use 8 or more characters with a mix of letters, numbers & special characters.",
            )
            # 3 Types of Validation
            # Field Level, Object Level, and Models Validators
        ],
        # RegexValidator validates with re.search()
        # Raise ValidationError with custom message and code (if provided)
    )
    is_active = models.BooleanField(default=True)


class Counsellor(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(
        max_length=256,
        validators=[
            RegexValidator(
                regex=r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$",
                message="Use 8 or more characters with a mix of letters, numbers & special characters.",
            )
        ],
    )
    is_active = models.BooleanField(default=True)


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    counsellor = models.ForeignKey(Counsellor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
