from django.conf import settings


def get_unhandled_message(ex):
    if settings.DEBUG:
        return str(ex)
    else:
        return "Something went wrong. Please try later."