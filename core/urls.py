from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Home and Contact URLs
    path('', views.HomeView.as_view(), name='home'),
    path('contacts/', views.ContactListView.as_view(), name='contact_list'),
    path('contacts/create/', views.ContactCreateView.as_view(), name='contact_create'),
    path('contacts/<int:pk>/update/', views.ContactUpdateView.as_view(), name='contact_update'),
    path('contacts/<int:pk>/delete/', views.ContactDeleteView.as_view(), name='contact_delete'),
    path('contacts/bulk-upload/', views.bulk_contact_upload, name='bulk_contact_upload'),
    
    # Campaign URLs
    path('campaigns/', views.CampaignListView.as_view(), name='campaign_list'),
    path('campaigns/create/', views.CampaignCreateView.as_view(), name='campaign_create'),
    path('campaigns/<int:pk>/', views.CampaignDetailView.as_view(), name='campaign_detail'),
    path('campaigns/<int:pk>/update/', views.CampaignUpdateView.as_view(), name='campaign_update'),
    path('campaigns/<int:pk>/delete/', views.CampaignDeleteView.as_view(), name='campaign_delete'),
    path('campaigns/<int:campaign_id>/add-contacts/', views.add_campaign_contacts, name='add_campaign_contacts'),
    path('campaigns/<int:campaign_id>/add-leads/', views.add_campaign_leads, name='add_campaign_leads'),
    path('campaigns/<int:campaign_id>/remove-contact/<int:contact_id>/', views.remove_campaign_contact, name='remove_campaign_contact'),
    path('campaigns/<int:campaign_id>/remove-lead/<int:lead_id>/', views.remove_campaign_lead, name='remove_campaign_lead'),
    path('api/campaigns/<int:campaign_id>/update-cost/', views.update_campaign_cost, name='update_campaign_cost'),
    
    # Opportunity URLs
    path('campaigns/<int:campaign_id>/opportunities/', views.OpportunityListView.as_view(), name='opportunity_list'),
    path('campaigns/<int:campaign_id>/opportunities/add/', views.add_opportunity, name='add_opportunity'),
    path('opportunities/<int:pk>/update/', views.OpportunityUpdateView.as_view(), name='opportunity_update'),
    path('opportunities/<int:pk>/delete/', views.OpportunityDeleteView.as_view(), name='opportunity_delete'),
    
    # Marketing URLs
    path('email-marketing/', views.EmailMarketingView.as_view(), name='email_marketing'),
    path('whatsapp-marketing/', views.WhatsAppMarketingView.as_view(), name='whatsapp_marketing'),
    path('facebook-marketing/', views.FacebookMarketingView.as_view(), name='facebook_marketing'),
    path('email-templates/', views.email_templates, name='email_templates'),

]
