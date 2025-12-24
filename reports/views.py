from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import MissingPersonReport, Sighting
from .forms import MissingPersonReportForm, SightingForm, ReportSearchForm

def home(request):
    recent_reports = MissingPersonReport.objects.filter(status='missing')[:6]
    total_missing = MissingPersonReport.objects.filter(status='missing').count()
    total_found = MissingPersonReport.objects.filter(status='found').count()
    
    context = {
        'recent_reports': recent_reports,
        'total_missing': total_missing,
        'total_found': total_found,
    }
    return render(request, 'reports/home.html', context)


def report_list(request):
    reports = MissingPersonReport.objects.all()
    form = ReportSearchForm(request.GET)
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        status = form.cleaned_data.get('status')
        
        if query:
            reports = reports.filter(
                Q(full_name__icontains=query) | 
                Q(case_number__icontains=query) |
                Q(last_seen_location__icontains=query)
            )
        
        if status:
            reports = reports.filter(status=status)
    
    context = {
        'reports': reports,
        'form': form,
    }
    return render(request, 'reports/report_list.html', context)


def report_detail(request, case_number):
    report = get_object_or_404(MissingPersonReport, case_number=case_number)
    sightings = report.sightings.all()
    
    if request.method == 'POST':
        sighting_form = SightingForm(request.POST)
        if sighting_form.is_valid():
            sighting = sighting_form.save(commit=False)
            sighting.report = report
            sighting.save()
            messages.success(request, 'Sighting reported successfully. Thank you for your help!')
            return redirect('report_detail', case_number=case_number)
    else:
        sighting_form = SightingForm()
    
    context = {
        'report': report,
        'sightings': sightings,
        'sighting_form': sighting_form,
    }
    return render(request, 'reports/report_detail.html', context)


def create_report(request):
    if request.method == 'POST':
        form = MissingPersonReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save()
            messages.success(request, f'Report submitted successfully. Case Number: {report.case_number}')
            return redirect('report_detail', case_number=report.case_number)
    else:
        form = MissingPersonReportForm()
    
    return render(request, 'reports/report_form.html', {'form': form})





