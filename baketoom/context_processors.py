from django.conf import settings # import the settings file

def reCAPTCHA_keys(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {
        'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY,
        'RECAPTCHA_PRIVATE_KEY': settings.RECAPTCHA_PRIVATE_KEY,
    }