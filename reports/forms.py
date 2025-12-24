from django import forms
from .models import MissingPersonReport, Sighting
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column

class MissingPersonReportForm(forms.ModelForm):
    class Meta:
        model = MissingPersonReport
        fields = [
            'full_name', 'age', 'gender', 'height_cm', 'weight_kg',
            'eye_color', 'hair_color', 'distinguishing_features', 'photo',
            'last_seen_date', 'last_seen_location', 'last_seen_wearing',
            'circumstances', 'reporter_name', 'reporter_relationship',
            'reporter_phone', 'reporter_email', 'police_notified',
            'police_case_number'
        ]
        widgets = {
            'last_seen_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'circumstances': forms.Textarea(attrs={'rows': 4}),
            'last_seen_wearing': forms.Textarea(attrs={'rows': 3}),
            'distinguishing_features': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.add_input(Submit('submit', 'Submit Report', css_class='btn-primary btn-lg'))


class SightingForm(forms.ModelForm):
    class Meta:
        model = Sighting
        fields = ['sighting_date', 'location', 'description', 'witness_name', 'witness_contact']
        widgets = {
            'sighting_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit Sighting', css_class='btn-warning'))


class ReportSearchForm(forms.Form):
    query = forms.CharField(max_length=200, required=False, 
                           widget=forms.TextInput(attrs={'placeholder': 'Search by name or case number...'}))
    status = forms.ChoiceField(choices=[('', 'All Statuses')] + MissingPersonReport.STATUS_CHOICES, 
                              required=False)
