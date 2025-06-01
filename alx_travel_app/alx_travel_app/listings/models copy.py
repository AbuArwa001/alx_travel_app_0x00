from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.role_name

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, phone_number=None, role=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            role=role
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, first_name, last_name, password=None):
        admin_role = Role.objects.get_or_create(role_name='admin')[0]
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role=admin_role
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    class Meta:
        # Add this to avoid reverse accessor clashes
        swappable = 'AUTH_USER_MODEL'
    username = None  # Remove username field, we'll use email instead
    user_id = models.AutoField(primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    password_hash = models.CharField(max_length=255)  # Will be handled by AbstractUser
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = UserManager()
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="custom_user_set",  # Changed from user_set
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_set",  # Changed from user_set
        related_query_name="user",
    )
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

class Property(models.Model):
    property_id = models.AutoField(primary_key=True)
    host = models.ForeignKey('listings.User', on_delete=models.CASCADE, related_name='properties')
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['host'], name='idx_property_host'),
        ]
    
    def __str__(self):
        return f"{self.name} in {self.location}"

class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELED = 'canceled', 'Canceled'
    
    booking_id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey('listings.User', on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        indexes = [
            models.Index(fields=['property'], name='idx_booking_property'),
            models.Index(fields=['user'], name='idx_booking_user'),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_date__lt=models.F('end_date')),
                name='check_start_date_before_end_date'
            ),
        ]
    
    def __str__(self):
        return f"Booking #{self.booking_id} for {self.property.name}"

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    payment_method = models.CharField(max_length=50)  # Could use choices like in previous example
    
    class Meta:
        indexes = [
            models.Index(fields=['booking'], name='idx_payment_booking'),
        ]
    
    def __str__(self):
        return f"Payment #{self.payment_id} for Booking #{self.booking.booking_id}"

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('listings.User', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        indexes = [
            models.Index(fields=['property'], name='idx_review_property'),
            models.Index(fields=['user'], name='idx_review_user'),
        ]
    
    def __str__(self):
        return f"Review by {self.user.email} for {self.property.name}"

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey('listings.User', on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey('listings.User', on_delete=models.CASCADE, related_name='received_messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        indexes = [
            models.Index(fields=['sender'], name='idx_message_sender'),
            models.Index(fields=['recipient'], name='idx_message_recipient'),
        ]
    
    def __str__(self):
        return f"Message from {self.sender.email} to {self.recipient.email}"