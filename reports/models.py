from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

class MissingPersonReport(models.Model):
    STATUS_CHOICES = [
        ('missing', 'Missing'),
        ('found', 'Found'),
        ('investigating', 'Under Investigation'),
        ('closed', 'Case Closed'),
    ]
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('U', 'Prefer not to say'),
    ]
    
    # Personal Information
    full_name = models.CharField(max_length=200)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    height_cm = models.PositiveIntegerField(help_text="Height in centimeters")
    weight_kg = models.PositiveIntegerField(help_text="Weight in kilograms")
    eye_color = models.CharField(max_length=50)
    hair_color = models.CharField(max_length=50)
    distinguishing_features = models.TextField(blank=True, help_text="Scars, tattoos, birthmarks, etc.")
    
    # Photo
    photo = models.ImageField(upload_to='missing_persons/%Y/%m/', blank=True)
    
    # Missing Details
    last_seen_date = models.DateTimeField()
    last_seen_location = models.CharField(max_length=300)
    last_seen_wearing = models.TextField(help_text="Description of clothing")
    circumstances = models.TextField(help_text="Circumstances of disappearance")
    
    # Contact Information
    reporter_name = models.CharField(max_length=200)
    reporter_relationship = models.CharField(max_length=100, help_text="Relationship to missing person")
    reporter_phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid phone number")]
    )
    reporter_email = models.EmailField()
    
    # Case Management
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='missing')
    case_number = models.CharField(max_length=20, unique=True, editable=False)
    reported_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    police_notified = models.BooleanField(default=False)
    police_case_number = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-reported_date']
        verbose_name = "Missing Person Report"
        verbose_name_plural = "Missing Person Reports"
    
    def save(self, *args, **kwargs):
        if not self.case_number:
            # Generate case number: MP-YYYYMMDD-XXXXX
            from datetime import datetime
            date_str = datetime.now().strftime('%Y%m%d')
            last_case = MissingPersonReport.objects.filter(
                case_number__startswith=f'MP-{date_str}'
            ).order_by('-case_number').first()
            
            if last_case:
                last_num = int(last_case.case_number.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            
            self.case_number = f'MP-{date_str}-{new_num:05d}'
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.full_name} - {self.case_number}"
    
    def get_status_badge_class(self):
        badge_classes = {
            'missing': 'danger',
            'found': 'success',
            'investigating': 'warning',
            'closed': 'secondary',
        }
        return badge_classes.get(self.status, 'secondary')


class Sighting(models.Model):
    report = models.ForeignKey(MissingPersonReport, on_delete=models.CASCADE, related_name='sightings')
    sighting_date = models.DateTimeField()
    location = models.CharField(max_length=300)
    description = models.TextField(help_text="Description of the sighting")
    witness_name = models.CharField(max_length=200, blank=True)
    witness_contact = models.CharField(max_length=15, blank=True)
    verified = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-sighting_date']
    
    def __str__(self):
        return f"Sighting of {self.report.full_name} on {self.sighting_date}"


