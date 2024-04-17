from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class Role(models.Model):
    ACTIVE = 0
    INACTIVE = 1
    STATUS_CHOICES = (
        (ACTIVE, "Active"),
        (INACTIVE, "Inactive"),
    )
    role_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0)

    def __str__(self):
        return self.name


class User(AbstractUser):
    ACTIVE = 0
    INACTIVE = 1
    STATUS_CHOICES = (
        (ACTIVE, "Active"),
        (INACTIVE, "Inactive"),
    )
    mobile_number_errors = {
        "required": "Mobile number is required",
        "invalid": "Enter a valid 10 digit mobile number"
        + "without spaces, + or isd code.",
    }
    _mobile_regex_validator = RegexValidator(
        regex=r"^\d{10}$", message="Phone number must be 10 digits without + or spaces."
    )
    email_errors = {
        "required": "Email number is required",
        "invalid": "Enter a valid Email" + "without spaces",
    }
    _email_regex_validator = RegexValidator(
        regex=r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$",
        message="Email must be Valid",
    )

    user_id = models.AutoField(primary_key=True)
    email = models.CharField(
        "Email",
        max_length=50,
        validators=[_email_regex_validator],
        blank=False,
        null=False,
        unique=True,
        error_messages=email_errors,
    )
    mobile_phone = models.CharField(
        "Mobile Number",
        max_length=10,
        validators=[_mobile_regex_validator],
        blank=False,
        null=False,
        unique=True,
        error_messages=mobile_number_errors,
    )
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0)
    role_id = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "user_accounts"
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return self.username


class PasswordRule(models.Model):
    ACTIVE = 0
    INACTIVE = 1
    STATUS_CHOICES = (
        (ACTIVE, "Active"),
        (INACTIVE, "Inactive"),
    )
    minimumcharaters = models.PositiveSmallIntegerField(null=True, blank=True)
    maximumcharaters = models.PositiveSmallIntegerField(null=True, blank=True)
    specialcharaters = models.PositiveSmallIntegerField(null=True, blank=True)
    uppercase = models.PositiveSmallIntegerField(null=True, blank=True)
    lowercase = models.PositiveSmallIntegerField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0)
