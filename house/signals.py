from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Comment


@receiver(post_save, sender=Comment)
def notify_user_post(sender, instance, created, **kwargs):
    if created:
        post_author = instance.commentPost.author
        post_author.email_user(
            subject=f'Новый комментарий к вашему объявлению {instance.commentPost.title}',
            message=instance.textPost,
        )

    if instance.status:
        post_author = instance.commentPost.author
        post_author.email_user(
            subject=f'{instance.ad.author} принял ваш комментарий',
            message=f'Комментарий: {instance.textPost}',
        )

