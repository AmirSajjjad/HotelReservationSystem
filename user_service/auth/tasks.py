from celery import shared_task

@shared_task
def send_sms_otp(phone_number, otp):
    return "The OTP code has been sent via sms :)"
