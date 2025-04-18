from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """Manager for CustomUser model with phone number login"""
    
    def create_user(self, phone, password=None, **extra_fields):
        """Create and return a regular user with phone number"""
        if not phone:
            raise ValueError("The Phone Number field is required")
        # Automatically assign a unique pass_key if not provided
        extra_fields.setdefault('pass_key', str(uuid.uuid4()))  # Generate a unique UUID for pass_key
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        """Create and return a superuser with phone number"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Automatically assign a unique pass_key if not provided
        extra_fields.setdefault('pass_key', str(uuid.uuid4()))  # Generate a unique UUID for pass_key

        return self.create_user(phone, password, **extra_fields)


# Custom User Model
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pass_key = models.CharField(max_length=500, unique=True,blank=True,null=True)
    phone = models.CharField(max_length=15, unique=True, verbose_name=_("Phone Number"))
    
    gm = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='gm_tag',
        limit_choices_to={"groups__name": "GM"}  # Limit to users in GM group
    )

    secretary = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='secretary_tag',
        limit_choices_to={"groups__name": "SECRETARY"}  # Limit to users in GM group
    )

    USERNAME_FIELD = 'phone'  # Use phone as the unique identifier
    username = None  # Disable default username field
    REQUIRED_FIELDS = []  # Remove username from required fields

    # Custom manager
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
    
        if self.first_name:
            self.first_name = self.first_name.upper()
        if self.last_name:
            self.last_name = self.last_name.upper()
        super().save(*args, **kwargs)

    class Meta:
            db_table = "user_table"
            
    def __str__(self):
        first_name = self.first_name if self.first_name else "N/A"
        last_name = self.last_name if self.last_name else "N/A"

        # User ke first group ka naam lena
        first_group = self.groups.first()  # Pehla group le rahe hain
        group_name = first_group.name if first_group else "No Group"

        return f"{first_name} {last_name} ({group_name})"
