from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password


# -------------------- PUBLIC SIGNUP --------------------
class Signup(models.Model):
    username = models.CharField(max_length=100, null=True)
    phoneno = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=255, null=True)
    conpass = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=100, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_admitted = models.BooleanField(default=False)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username


# -------------------- LOGIN MODEL --------------------
class Login(models.Model):
    phoneno = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)


# -------------------- COMPLAINT MODEL --------------------
class Complaint(models.Model):
    user = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    address = models.TextField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    complaint_type = models.CharField(max_length=100, null=True)
    description = models.TextField(max_length=500, null=True)
    file = models.FileField(upload_to='complaints/', blank=True, null=True)
    date_time = models.DateTimeField(default=timezone.now)
    supervisor_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.user} - {self.complaint_type}"


# -------------------- REQUEST MODEL --------------------
class Request(models.Model):
    REQUEST_TYPES = [
        ("Public Safety", "Public Safety"),
        ("Sanitation / Hygiene", "Sanitation / Hygiene"),
        ("Road / Traffic Issues", "Road / Traffic Issues"),
        ("Electricity / Water Supply", "Electricity / Water Supply"),
        ("Government Services", "Government Services"),
        ("Others", "Others"),
    ]

    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    request_type = models.CharField(max_length=50, choices=REQUEST_TYPES)
    other_type = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


# -------------------- POSTS / NOTIFICATIONS --------------------
class Post(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='posts/images/', null=True, blank=True)
    video = models.FileField(upload_to='posts/videos/', null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    deleted_by = models.TextField(blank=True, null=True, default="")    


    def __str__(self):
        return self.title or "Post"


# -------------------- ACHIEVEMENTS --------------------
class Achievement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    achieved_on = models.DateField(default=timezone.now)
    image = models.ImageField(upload_to='achievements/', blank=True, null=True)


# -------------------- TASK MODEL --------------------
class Task(models.Model):
    STATUS_CHOICES = (
        ('verified', 'Verified'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    assigned_date = models.DateField(default=timezone.now)
    due_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.title


# -------------------- ADMIN MODEL --------------------
class Admins(models.Model):
    username = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)


# -------------------- AREA MODEL --------------------
class Area(models.Model):
    name = models.CharField(max_length=100, unique=True)


# -------------------- EO USER --------------------
class EOUser(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username


# -------------------- EO LOGIN --------------------
from django.db import models
class EOLogin(models.Model):
    emp_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, null=True, blank=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.emp_id

    # def set_password(self, raw_password):
    #     self.password = make_password(raw_password)
    #     self.save()

    # def check_password(self, raw_password):
    #     return check_password(raw_password, self.password)


# -------------------- SUPERVISOR MODEL --------------------
from django.db import models

class Supervisor(models.Model):
    supervisor_id = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    # def set_password(self, raw_password):
    #     self.password = make_password(raw_password)
    #     self.save()

    # def check_password(self, raw_password):
    #     return check_password(raw_password, self.password)

    def __str__(self):
        return self.supervisor_id



