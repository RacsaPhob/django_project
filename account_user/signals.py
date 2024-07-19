from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount


@receiver(user_signed_up)
def user_signed_up_handler(request, user, **kwargs):
    social_account = SocialAccount.objects.get(user=user)
    extra_data = social_account.extra_data

    for el in extra_data:
        print(el,'\n')
