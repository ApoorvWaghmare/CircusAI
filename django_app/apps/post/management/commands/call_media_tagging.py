import time
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
import requests

#----------#

from apps.post.config import Config
from apps.post.models.mongo_models import Prompt, MediaTags
from apps.post.models.mysql_models import GenMediaRef


#======================================================================================================================#
# Command
#======================================================================================================================#

# @reboot cd /home/azureuser/CircusAI/application/backend/django_app && /home/azureuser/anaconda3/envs/circusaibackendv2/bin/python manage.py media_tagging >> /home/azureuser/CircusAI/application/backend/django_app/cron_log.log 2>&1

class Command(BaseCommand):
    help = 'Calls another server for 5 minutes, then pauses for 5 minutes, continuously'

    def handle(self, *args, **options):
        while True:
            start_time = timezone.now()
            end_time = start_time + timezone.timedelta(minutes=5)

            self.stdout.write(self.style.SUCCESS(f'Starting 5-minute active period at {start_time}'))

            while timezone.now() < end_time:
                try:
                    # Get all gen_media_refs and post_ids from MySQL
                    gen_media_refs_with_post_ids = dict(GenMediaRef.objects.values_list('gen_media_ref', 'post_id'))
                    # Get all gen_media_refs from MySQL
                    gen_media_refs = set(gen_media_refs_with_post_ids.keys())
                    # Get all tagged media_refs from MongoDB
                    tagged_gen_media_refs = set(MediaTags.objects.values_list('media_ref', flat=True))
                    # Find gen_media_refs in MySQL that are not in MongoDB
                    non_tagged_gen_media_refs = list(gen_media_refs - tagged_gen_media_refs)
                    # Create a dictionary with non-tagged gen_media_refs and their post_ids
                    non_tagged_gen_media_refs_with_post_ids = {
                        ref: gen_media_refs_with_post_ids[ref]
                        for ref in non_tagged_gen_media_refs
                    }
                    self.stdout.write(self.style.SUCCESS(f'data = {non_tagged_gen_media_refs_with_post_ids}'))

                    # Here you would typically make your server call
                    # response = requests.get('https://other-server.com/api/endpoint')
                    # self.stdout.write(self.style.SUCCESS(f'Successfully called server at {timezone.now()}'))
                    
                    # Process the response as needed
                    # ...

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))

                # Wait for a short interval before the next iteration
                time.sleep(10)  # Wait for 10 seconds

            self.stdout.write(self.style.SUCCESS(f'Completed 5-minute active period at {timezone.now()}'))
            self.stdout.write(self.style.SUCCESS('Starting 5-minute pause'))
            
            # Pause for 5 minutes
            time.sleep(300)

            self.stdout.write(self.style.SUCCESS(f'Resuming after pause at {timezone.now()}'))

#======================================================================================================================#
# End of Command
#======================================================================================================================#
