import string
from core.models import Guest, FamilyGroup, SecretFriendAssignment
import random
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password, check_password

#Generate a random PIN
def generate_random_pin(length=6) -> str:
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(chars))

#Generate Username
def generate_username(name: str) -> str:
    base_username = ''.join(e for e in name if e.isalnum()).lower()
    unique_suffix = ''.join(random.choices(string.digits, k=4))
    return f"{base_username}{unique_suffix}"

# Service to assign hashed PINs to guests
def assign_username_and_hashed_pins():
    guests = Guest.objects.all()
    username = generate_username(guest.name)
    pin = generate_random_pin()

    for guest in guests:
        guest.username = generate_username(guest.name)
        guest.hashed_pin = make_password(pin)
        guest.save()
        print(f"Assigned {guest.hashed_pin} PIN to guest {guest.name}")