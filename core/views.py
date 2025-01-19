from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django import forms
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Contact, Campaign, Opportunity
from .forms import ContactForm, BulkContactForm, CampaignForm, OpportunityForm
from django.utils.timezone import make_aware
from datetime import datetime,timedelta
import time
import csv
import io
from django.http import JsonResponse
import json
from decimal import Decimal
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
import smtplib
import ssl
from email.message import EmailMessage
from django.core.mail import send_mail
from core.models import Contact
from django.conf import settings
from background_task import background
import logging
import base64
from io import BytesIO

import pywhatkit as kit
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def send_whatsapp_message(request):
    print("Entered")
    message ="WhatsApp Automation Testing"
    contacts =["+917620169727"]# List of phone numbers in international format
    print(contacts)

    if not message or not contacts:
        messages.error(request, 'Fill Details')
        return redirect('core:whatsapp_marketing')

    try:
        for contact in contacts:
            # Calculate a time 1 minute in the future
            future_time = datetime.now() + timedelta(minutes=1)

            kit.sendwhatmsg_instantly(
                phone_no=contact,
                message=message,
                wait_time=10,  # Time to wait before sending in seconds
                tab_close=True  # Automatically close the browser tab
            )
        print("Executed")
        messages.success(request, f'Message sent successfully to {len(contacts)} contacts')
    except Exception as e:
        print(f"Error: {e}")
        messages.error(request, f"Failed to send message: {str(e)}")

    return redirect('core:whatsapp_marketing')


def email_templates(request):
    contacts = Contact.objects.all()
    return render(request,'core/emailTemplates.html')

def serialize_attachment(attachment):
    attachment_content = attachment.read()  # Read the file content
    return base64.b64encode(attachment_content).decode('utf-8')  # Base64 encode and return as string

# Deserialize the file (convert back to file object)
def deserialize_attachment(base64_content, attachment_name):
    attachment_content = base64.b64decode(base64_content)  # Decode base64 back to binary data
    return BytesIO(attachment_content)  # Return as a BytesIO object

@background(schedule=1)
def schedule_email_task(schedule_date,schedule_time,subject, message, recipient_emails,sender_email, attachment_base64, attachment_name):
        print("Schedule view")
        send_datetime_str = f"{schedule_date} {schedule_time}"
        send_datetime = datetime.strptime(send_datetime_str, "%Y-%m-%d %H:%M:%S")
        """Background task for scheduled emails"""

        while True:
            current_time = datetime.now()
            if current_time >= send_datetime:
                send_email(subject, message, recipient_emails,sender_email, attachment_base64, attachment_name)
                break
            #time.sleep(30)

def send_email(subject, message, recipient_email,sender_email, attachment_base64, attachment_name):
        """Send email using SMTP"""
        em = EmailMessage()
        print("----------")
        em['From'] = sender_email
        em['To'] =recipient_email
        em['Subject'] = subject
        em.set_content(message)

        if attachment_base64 and attachment_name:
            attachment = deserialize_attachment(attachment_base64, attachment_name)
            em.add_attachment(
            attachment.read(),
            filename=attachment_name,
            maintype='application',  # Default MIME type
            subtype='octet-stream'
        )

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender_email,'mvfr koeq nkwn kisd')
            smtp.sendmail(sender_email, recipient_email, em.as_string())


class AutomateEmailView(View):
    template_name = 'core/automate_email.html'

    def get(self, request):
        # Fetch contacts for email selection
        contacts = Contact.objects.all()
        return render(request, self.template_name, {'contacts': contacts})

    def post(self, request, *args, **kwargs):
            # Get form data
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        recipients = request.POST.getlist('recipients')
        attachment = request.FILES.get('image')
        scheduled_time = request.POST.get('schedule_time')
        parsed_datetime = datetime.fromisoformat(scheduled_time)
        # Extract date and time in the desired formats
        schedule_date = parsed_datetime.date().isoformat()  # '2025-01-17'
        schedule_time = parsed_datetime.time().strftime("%H:%M:%S")  # '15:54:00'
        print(schedule_time)
        print(schedule_date)
        '''schedule_date = "2025-01-17"  # YYYY-MM-DD
        schedule_time = "15:54:00"'''
        sender_email = 'varadpathak011@gmail.com'
        password = 'mvfr koeq nkwn kisd'

        attachment_base64 = None
        attachment_name = None
        if attachment:
            attachment_base64 = serialize_attachment(attachment)  # Serialize the file
            attachment_name = attachment.name  # Get the attachment name
            # Validate required fields
        if not all([subject, message, recipients]):
            messages.error(request, 'Please fill in all required fields')
            return redirect('core:automate_email')

            # Get recipient emails
        recipient_emails = list(Contact.objects.filter(
            id__in=recipients).values_list('email', flat=True))

        if not recipient_emails:
            messages.error(request, 'No valid recipients found')
            return redirect('core:automate_email')

            # Handle scheduled emails
        if scheduled_time:
            try:
                schedule_datetime = make_aware(
                    datetime.strptime(scheduled_time, '%Y-%m-%dT%H:%M'))
                    
                if schedule_datetime <= make_aware(datetime.now()):
                    messages.error(request, 'Schedule time must be in the future')
                    return redirect('core:automate_email')
                    
                schedule_email_task(schedule_date,schedule_time,subject, message, recipient_emails,sender_email, attachment_base64, attachment_name)
                messages.success(
                    request, f'Email scheduled for {schedule_datetime}')
            except ValueError:
                messages.error(request, 'Invalid schedule time format')
                return redirect('core:automate_email')
        else:
                # Send immediately
            send_email(subject, message, recipient_emails,sender_email, attachment_base64, attachment_name)
            messages.success(
                request, f'Email sent successfully to {len(recipient_emails)} recipients')

        return redirect('core:automate_email')
    

    #@background(schedule=60)
    


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Total Contacts
        context['total_contacts'] = Contact.objects.count()
        
        # Total Revenue (sum of all campaign actual revenues)
        context['total_revenue'] = Campaign.objects.aggregate(
            total_revenue=Sum('actual_revenue', default=0)
        )['total_revenue']
        
        # Total Cost (sum of all campaign actual costs)
        context['total_cost'] = Campaign.objects.aggregate(
            total_cost=Sum('actual_cost', default=0)
        )['total_cost']
        
        # Monthly Sales Overview (Dummy Data for now)
        context['monthly_sales'] = [
            {'month': 'Jan', 'sales': 15000},
            {'month': 'Feb', 'sales': 18500},
            {'month': 'Mar', 'sales': 22000},
            {'month': 'Apr', 'sales': 20000},
            {'month': 'May', 'sales': 25000},
            {'month': 'Jun', 'sales': 30000},
        ]
        
        return context

class ContactListView(ListView):
    model = Contact
    template_name = 'core/contact_list.html'
    context_object_name = 'contacts'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bulk_form'] = BulkContactForm()
        return context

class ContactCreateView(CreateView):
    model = Contact
    template_name = 'core/contact_form.html'
    success_url = reverse_lazy('core:contact_list')
    fields = ['name', 'email', 'phone']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        names = request.POST.getlist('name[]')
        emails = request.POST.getlist('email[]')
        phones = request.POST.getlist('phone[]')

        contacts_created = []
        for name, email, phone in zip(names, emails, phones):
            if name and email and phone:  # Only create if all fields are filled
                contact = Contact.objects.create(
                    name=name,
                    email=email,
                    phone=phone
                )
                contacts_created.append(contact)

        if contacts_created:
            messages.success(request, f'{len(contacts_created)} contact(s) created successfully.')
        else:
            messages.error(request, 'No contacts were created. Please check the form data.')

        return redirect(self.success_url)

def bulk_contact_upload(request):
    if request.method == 'POST':
        form = BulkContactForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['contacts_csv']
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            next(io_string)  # Skip header row
            
            success_count = 0
            error_count = 0
            
            for row in csv.reader(io_string):
                try:
                    Contact.objects.create(
                        name=row[0],
                        email=row[1],
                        phone=row[2]
                    )
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    continue
            
            if success_count > 0:
                messages.success(request, f'Successfully imported {success_count} contacts!')
            if error_count > 0:
                messages.warning(request, f'Failed to import {error_count} contacts due to errors.')
                
    return redirect('core:contact_list')

class ContactUpdateView(SuccessMessageMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'core/contact_form.html'
    success_url = reverse_lazy('core:contact_list')
    success_message = "Contact was updated successfully!"

class ContactDeleteView(SuccessMessageMixin, DeleteView):
    model = Contact
    template_name = 'core/contact_confirm_delete.html'
    success_url = reverse_lazy('core:contact_list')
    success_message = "Contact was deleted successfully!"

class ContactDetailView(DetailView):
    model = Contact
    template_name = 'core/contact_detail.html'
    context_object_name = 'contact'


class EmailMarketingView(View):
    template_name = 'core/email_marketing.html'

    def get(self, request):
        contacts = Contact.objects.all()
        return render(request, self.template_name, {'contacts': contacts})

    def post(self, request):
        try:
            # Get form data
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            recipients = request.POST.getlist('recipients')
            attachment = request.FILES.get('image')

            if not subject or not message or not recipients:
                messages.error(request, 'Please fill in all required fields')
                return redirect('core:email_marketing')

            # Get recipient emails
            recipient_emails = list(Contact.objects.filter(
                id__in=recipients).values_list('email', flat=True))

            # Create SMTP connection
            smtp_server = "smtp.gmail.com"
            port = 587
            context = ssl.create_default_context()

            server = smtplib.SMTP(smtp_server, port)
            server.starttls(context=context)
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            # Create and send email
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=recipient_emails,
            )
            email.content_subtype = "html"

            if attachment:
                email.attach(
                    attachment.name,
                    attachment.read(),
                    attachment.content_type
                )

            email.send(fail_silently=False)
            server.quit()

            messages.success(request, f'Email sent successfully to {len(recipient_emails)} recipients.')

        except smtplib.SMTPAuthenticationError:
            messages.error(request, 'Failed to authenticate with email server. Please check your email credentials.')
        except smtplib.SMTPException as e:
            messages.error(request, f'SMTP Error: {str(e)}')
        except Exception as e:
            messages.error(request, 'Failed to send email. Please check your settings and try again.')

        return redirect('core:email_marketing')
    
    def email_templates(request):
        return render(request,'core/emailTemplates.html')


class CampaignListView(ListView):
    model = Campaign
    template_name = 'core/campaign_list.html'
    context_object_name = 'campaigns'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_campaigns'] = self.model.objects.count()
        return context

    def get_queryset(self):
        # Optional: Add filtering or ordering if needed
        return super().get_queryset().order_by('-start_date')

class CampaignCreateView(CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'core/campaign_form.html'
    success_url = reverse_lazy('core:campaign_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Campaign created successfully!')
        if 'action' in self.request.POST and self.request.POST['action'] == 'save_and_new':
            return redirect('core:campaign_create')
        return response

class CampaignDetailView(DetailView):
    model = Campaign
    template_name = 'core/campaign_detail.html'
    context_object_name = 'campaign'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_contacts'] = Contact.objects.all()
        return context

def add_campaign_contacts(request, campaign_id):
    if request.method == 'POST':
        campaign = get_object_or_404(Campaign, pk=campaign_id)
        selected_contacts = request.POST.getlist('selected_contacts')
        campaign.contacts.set(selected_contacts)
        messages.success(request, 'Contacts added successfully!')
        return redirect('core:campaign_detail', pk=campaign_id)
    return redirect('core:campaign_detail', pk=campaign_id)

def add_campaign_leads(request, campaign_id):
    if request.method == 'POST':
        campaign = get_object_or_404(Campaign, pk=campaign_id)
        selected_leads = request.POST.getlist('selected_leads')
        campaign.leads.set(selected_leads)
        messages.success(request, 'Leads added successfully!')
        return redirect('core:campaign_detail', pk=campaign_id)
    return redirect('core:campaign_detail', pk=campaign_id)

def remove_campaign_contact(request, campaign_id, contact_id):
    if request.method == 'POST':
        campaign = get_object_or_404(Campaign, pk=campaign_id)
        contact = get_object_or_404(Contact, pk=contact_id)
        campaign.contacts.remove(contact)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def remove_campaign_lead(request, campaign_id, lead_id):
    if request.method == 'POST':
        campaign = get_object_or_404(Campaign, pk=campaign_id)
        lead = get_object_or_404(Contact, pk=lead_id)
        campaign.leads.remove(lead)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

class CampaignUpdateView(UpdateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'core/campaign_form.html'
    success_url = reverse_lazy('core:campaign_list')

class CampaignDeleteView(DeleteView):
    model = Campaign
    success_url = reverse_lazy('core:campaign_list')

class WhatsAppMarketingView(View):
    template_name = 'core/whatsapp_marketing.html'

    def get(self, request):
        contacts = Contact.objects.all()
        return render(request, self.template_name, {'contacts': contacts})

    def post(self, request):
        message = request.POST.get('message')
        recipients = request.POST.getlist('recipients')

        if not message or not recipients:
            messages.error(request, 'Please fill in all required fields')
            return redirect('core:whatsapp_marketing')

        # Logic to send WhatsApp messages
        messages.success(request, f'Message will be sent to {len(recipients)} recipients')
        return redirect('core:whatsapp_marketing')

class FacebookMarketingView(View):
    template_name = 'core/facebook_marketing.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        post_content = request.POST.get('postContent')
        image = request.FILES.get('image')

        if not post_content:
            messages.error(request, 'Please fill in all required fields')
            return redirect('core:facebook_marketing')

        # Logic to post to Facebook
        messages.success(request, 'Post will be published on Facebook')
        return redirect('core:facebook_marketing')

class OpportunityListView(ListView):
    model = Opportunity
    template_name = 'core/opportunity_list.html'
    context_object_name = 'opportunities'

    def get_queryset(self):
        campaign_id = self.kwargs.get('campaign_id')
        return Opportunity.objects.filter(campaign_id=campaign_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campaign'] = get_object_or_404(Campaign, pk=self.kwargs.get('campaign_id'))
        context['form'] = OpportunityForm()
        return context

def add_opportunity(request, campaign_id):
    campaign = get_object_or_404(Campaign, pk=campaign_id)
    
    if request.method == 'POST':
        form = OpportunityForm(request.POST)
        if form.is_valid():
            opportunity = form.save(commit=False)
            opportunity.campaign = campaign
            opportunity.save()
            messages.success(request, 'Opportunity added successfully!')
            return redirect('core:opportunity_list', campaign_id=campaign_id)
    else:
        form = OpportunityForm()
    
    return render(request, 'core/opportunity_list.html', {
        'form': form,
        'campaign': campaign,
        'opportunities': campaign.opportunities.all()
    })

class OpportunityUpdateView(UpdateView):
    model = Opportunity
    form_class = OpportunityForm
    template_name = 'core/opportunity_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campaign'] = self.object.campaign
        return context

    def get_success_url(self):
        return reverse_lazy('core:campaign_detail', kwargs={'pk': self.object.campaign.pk})

class OpportunityDeleteView(DeleteView):
    model = Opportunity
    template_name = 'core/opportunity_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('core:opportunity_list', kwargs={'campaign_id': self.object.campaign.id})

def campaign_detail(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    opportunities = campaign.opportunities.all()
    
    # Debug information
    print("Campaign:", campaign.name)
    print("Expected Revenue:", campaign.expected_revenue)
    print("Actual Revenue:", campaign.actual_revenue)
    print("\nOpportunities:")
    for opp in opportunities:
        print(f"- {opp.name}: Amount={opp.amount}, Stage='{opp.stage}'")
    
    context = {
        'campaign': campaign,
        'opportunities': opportunities,
    }
    return render(request, 'core/campaign_detail.html', context)

def update_campaign_cost(request, campaign_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            campaign = Campaign.objects.get(id=campaign_id)
            
            # Convert to Decimal for accurate calculation
            campaign.actual_cost = Decimal(str(data['actual_cost']))
            campaign.save()
            
            # Calculate budget percentage
            budget_percentage = campaign.get_budget_percentage()
            
            return JsonResponse({
                'success': True,
                'budget_percentage': float(budget_percentage),
                'actual_cost': float(campaign.actual_cost)
            })
        except Campaign.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Campaign not found'
            }, status=404)
        except (KeyError, ValueError, json.JSONDecodeError) as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    return JsonResponse({
        'success': False,
        'error': 'Method not allowed'
    }, status=405)



    '''  # Create email content
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=recipient_emails,
        )
        email.content_subtype = "html"

        if attachment:
            email.attach(
                attachment.name,
                attachment.read(),
                attachment.content_type
            )
'''