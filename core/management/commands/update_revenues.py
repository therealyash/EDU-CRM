from django.core.management.base import BaseCommand
from core.models import Campaign

class Command(BaseCommand):
    help = 'Update actual revenue for all campaigns'

    def handle(self, *args, **options):
        campaigns = Campaign.objects.all()
        for campaign in campaigns:
            campaign.update_actual_revenue()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Updated campaign "{campaign.name}": Actual Revenue = {campaign.actual_revenue}'
                )
            )
