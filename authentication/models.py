from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomManager(BaseUserManager):
    """
    This is a user manager to add user details when user do google sign in.
    In this case we wont have user mobile number, gender hence need to use this
    manager
    """

    def create_user(self, email, password, first_name, last_name, **kwargs):
        # Handle missing fields in kwargs here
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            # Perform any additional logic or set default values for missing fields
            mobile_number="",
            gender="",
            **kwargs,
        )
        user.set_password(password)
        user.save()
        return user

    def get_or_create(self, email, password, first_name, last_name, **kwargs):
        try:
            user = self.get(email=email)  # Retrieve existing user with matching email
            setattr(user, "password", password)
            user.save()
            return user, False  # User already exists
        except self.model.DoesNotExist:
            return (
                self.create_user(email, password, first_name, last_name, **kwargs),
                True,
            )  # Create new user


class User(AbstractUser):
    gender_choice = [
        ("male", "Male"),
        ("female", "Female"),
        ("prefer_not_to_say", "Prefer Not To Say"),
    ]
    marital_status_choice = [
        ("married", "Married"),
        ("not_married", "Not Married"),
        ("prefer_not_to_say", "Prefer Not To Say"),
    ]
    email = models.EmailField(
        unique=True,
        verbose_name="User Email",
        help_text="User Email",
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name="User first name",
        help_text="User first name",
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name="User last name",
        help_text="User last name",
    )
    mobile_number = models.CharField(
        max_length=25,
        verbose_name="Mobile number of the user",
        help_text="Mobile number of the user",
    )
    birth_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="User birthdate",
        help_text="User birthdate",
    )
    gender = models.CharField(
        max_length=20,
        choices=gender_choice,
        verbose_name="User Gender",
        help_text="User Gender",
    )
    marital_status = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        choices=marital_status_choice,
        verbose_name="Marital Status",
        help_text="Marital Status",
    )
    address = models.CharField(
        blank=True,
        null=True,
        max_length=225,
        verbose_name="User Address",
        help_text="User Address",
    )
    otp = models.CharField(
        blank=True,
        null=True,
        max_length=10,
        verbose_name="Password reset OTP",
        help_text="Password reset OTP",
    )

    # this is for super user creation only via createsuperuser command
    REQUIRED_FIELDS = ["first_name", "last_name", "username", "mobile_number", "gender"]

    # For login using email
    # here username will refer to the email
    USERNAME_FIELD = "email"

    googlemanager = (
        CustomManager()
    )  # Custom manager for google to manage missing values

    def __str__(self):
        return f"{self.username}"

    # override save method to create hashed password
    def save(self, *args, **kwargs):
        self.email = self.email.lower()

        # here we will confirm that password has not been hashed.
        # if its hashed we wont do anything else we will hash it
        # if we create superuser via cmd/terminal then we dont need to create
        # hashable password its encrypted already.
        # TO DO: its patch at present need to look at it in future
        if (not self.check_password(self._password)) and (not self.is_superuser):
            self.set_password(self.password)

        # Call the original save method to save the object to the database
        super().save(*args, **kwargs)

    class Meta:
        base_manager_name = "objects"
        default_manager_name = "objects"
        db_table = "auth_user"
        verbose_name = "User"
        verbose_name_plural = "Users"