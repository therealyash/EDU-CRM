from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Campaign(models.Model):
    CAMPAIGN_TYPES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('social', 'Social Media'),
        ('mail', 'Direct Mail'),
        ('other', 'Other'),
    ]
    
    CAMPAIGN_STATUS = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='campaigns', null=True, blank=True)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50, choices=CAMPAIGN_TYPES, default='email')
    status = models.CharField(max_length=50, choices=CAMPAIGN_STATUS, default='draft')
    start_date = models.DateField()
    end_date = models.DateField()
    expected_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    actual_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    budgeted_cost = models.DecimalField(max_digits=10, decimal_places=2)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2)
    expected_response = models.PositiveIntegerField()
    numbers_sent = models.PositiveIntegerField()
    description = models.TextField()
    content = models.TextField(blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    sender_name = models.CharField(max_length=100, blank=True, null=True)
    sender_email = models.EmailField(blank=True, null=True)
    contacts = models.ManyToManyField(Contact, related_name='campaigns', blank=True)
    leads = models.ManyToManyField(Contact, related_name='lead_campaigns', blank=True)

    def update_actual_revenue(self):
        """Update actual revenue based on closed-won opportunities"""
        closed_won_revenue = self.opportunities.filter(stage='closed-won').aggregate(
            total=models.Sum('amount')
        )['total'] or 0
        self.actual_revenue = closed_won_revenue
        self.save()

    def get_revenue_percentage(self):
        """Calculate percentage of expected revenue achieved"""
        if self.expected_revenue:
            return (self.actual_revenue / self.expected_revenue) * 100
        return 0

    def get_budget_percentage(self):
        """Calculate percentage of budget used"""
        if self.budgeted_cost:
            return (self.actual_cost / self.budgeted_cost) * 100
        return 0

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.name

class Opportunity(models.Model):
    STAGES = [
        ('prospecting', 'Prospecting'),
        ('qualification', 'Qualification'),
        ('needs-analysis', 'Needs Analysis'),
        ('proposal', 'Proposal'),
        ('negotiation', 'Negotiation'),
        ('closed-won', 'Closed Won'),
        ('closed-lost', 'Closed Lost'),
    ]

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='opportunities')
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    probability = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    stage = models.CharField(max_length=50, choices=STAGES)
    close_date = models.DateField()
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update campaign revenue when opportunity is saved
        self.campaign.update_actual_revenue()

    def delete(self, *args, **kwargs):
        campaign = self.campaign
        super().delete(*args, **kwargs)
        # Update campaign revenue when opportunity is deleted
        campaign.update_actual_revenue()

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Opportunities'

    def __str__(self):
        return self.name
