from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class EmployeeManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, full_name, password, **extra_fields)

class Employee(AbstractBaseUser, PermissionsMixin):
    class Department(models.TextChoices):
        CLOUD_DEVELOPMENT = 'CDD', 'Cloud Development'
        NETWORK_TEAM = 'NWT', 'Network Team'
        SECURITY_TEAM = 'STT', 'Security Team'
        CLOUD_OPERATION_TEAM = 'COT', 'Cloud Operation Team'
        HR = 'HR', 'Human Resources'
        MANAGEMENT = 'MGT', 'Management'
        SALES = 'SLS', 'Sales'

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    
    department = models.CharField(
        max_length=4, 
        choices=Department.choices, 
        default=Department.CLOUD_DEVELOPMENT
    )
    
    # Simplified Designation as a CharField for flexibility
    designation = models.CharField(max_length=100, blank=True)
    
    phone = models.CharField(max_length=20, blank=True, null=True) 
    is_staff = models.BooleanField(default=False) 
    is_active = models.BooleanField(default=True) 
    date_joined = models.DateTimeField(auto_now_add=True) 

    objects = EmployeeManager()

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return f"{self.full_name} ({self.email})"