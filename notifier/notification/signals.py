import json
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Notification
from config.pubsubmanager import PubSubManager

pubsubmanager = PubSubManager()
pubsubmanager.connect()

@receiver(post_save, sender=Notification)
def notify_user(sender, instance, created, **kwargs):
    if created:
        obj = {
            "title": instance.title,
            "message": instance.body,
        }
        pubsubmanager._publish(message=json.dumps(obj))
        print('Notification created')
