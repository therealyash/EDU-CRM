from django import forms
from .models import Contact, Campaign, Opportunity

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        }

class BulkContactForm(forms.Form):
    contacts_csv = forms.FileField(
        label='Upload CSV file',
        help_text='CSV file should have columns: name, email, phone',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'type', 'status', 'start_date', 'end_date', 'expected_revenue', 
                 'budgeted_cost', 'actual_cost', 'expected_response', 'numbers_sent', 
                 'description', 'content', 'subject', 'sender_name', 'sender_email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(choices=Campaign.CAMPAIGN_TYPES),
            'status': forms.Select(choices=Campaign.CAMPAIGN_STATUS),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expected_revenue': forms.NumberInput(attrs={'class': 'form-control'}),
            'budgeted_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'actual_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'expected_response': forms.NumberInput(attrs={'class': 'form-control'}),
            'numbers_sent': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'sender_name': forms.TextInput(attrs={'class': 'form-control'}),
            'sender_email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = ['name', 'company', 'amount', 'probability', 'stage', 'close_date', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter opportunity name'
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter amount'
            }),
            'probability': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter probability',
                'min': '0',
                'max': '100'
            }),
            'stage': forms.Select(attrs={
                'class': 'form-select'
            }, choices=Opportunity.STAGES),
            'close_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter description',
                'rows': 3
            })
        }
