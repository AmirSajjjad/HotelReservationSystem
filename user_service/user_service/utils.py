from rest_framework_simplejwt.tokens import RefreshToken
import random

def generate_otp(digits):
    if digits < 1:
        raise ValueError("Number of digits must be at least 1")
    
    lower_bound = 10**(digits - 1)
    upper_bound = 10**digits - 1
    
    otp = random.randint(lower_bound, upper_bound)
    
    return str(otp)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
