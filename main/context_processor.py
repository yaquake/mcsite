from .models import MottoEmailPhone


def get_motto(request):
    creds = MottoEmailPhone.objects.first()
    return {'creds': creds}

