# from django.contrib import admin

# # Register your models here.
# ============ reports/admin.py ============
from django.contrib import admin
from .models import MissingPersonReport, Sighting

@admin.register(MissingPersonReport)
class MissingPersonReportAdmin(admin.ModelAdmin):
    list_display = ['case_number', 'full_name', 'age', 'status', 'last_seen_date', 'reported_date']
    list_filter = ['status', 'gender', 'reported_date']
    search_fields = ['full_name', 'case_number', 'last_seen_location']
    readonly_fields = ['case_number', 'reported_date', 'updated_date']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('full_name', 'age', 'gender', 'height_cm', 'weight_kg', 
                      'eye_color', 'hair_color', 'distinguishing_features', 'photo')
        }),
        ('Missing Details', {
            'fields': ('last_seen_date', 'last_seen_location', 'last_seen_wearing', 'circumstances')
        }),
        ('Reporter Information', {
            'fields': ('reporter_name', 'reporter_relationship', 'reporter_phone', 'reporter_email')
        }),
        ('Case Management', {
            'fields': ('status', 'case_number', 'police_notified', 'police_case_number', 
                      'reported_date', 'updated_date')
        }),
    )


@admin.register(Sighting)
class SightingAdmin(admin.ModelAdmin):
    list_display = ['report', 'sighting_date', 'location', 'verified', 'created_date']
    list_filter = ['verified', 'sighting_date']
    search_fields = ['report__full_name', 'location', 'description']
