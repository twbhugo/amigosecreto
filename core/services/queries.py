from django.db.models import Prefetch
from core.models import Guest, FamilyGroup

# Get all confirmed guests by family group
def get_confirmed_guests_by_family_group():
    confirmed_guests = Guest.objects.filter(confirmed=True)
    family_groups = FamilyGroup.objects.prefetch_related(
        Prefetch('guests', queryset=confirmed_guests)
    )
    return family_groups

# Get Guest by username
def get_guest_by_username(username):
    try:
        guest = Guest.objects.get(username=username)
        return guest
    except Guest.DoesNotExist:
        return None

# Get PIN by username
def get_pin_by_username(username):
    guest = get_guest_by_username(username)
    if guest:
        return guest.pin
    return None

# Get Guest by PIN
def get_guest_by_pin(pin):
    try:
        guest = Guest.objects.get(pin=pin)
        return guest
    except Guest.DoesNotExist:
        return None
    
# Get Guest by ID
def get_guest_by_id(guest_id):
    try:
        guest = Guest.objects.get(guest_id=guest_id)
        return guest
    except Guest.DoesNotExist:
        return None
    
# Confirm Guest attendance by PIN
def confirm_guest_attendance(id):
    guest = get_guest_by_id(guest_id=id)
    if guest:
        guest.confirmed = True
        guest.save()
        return True
    return False

# Cancel Guest attendance by ID
def cancel_guest_attendance(id):
    guest = get_guest_by_id(guest_id=id)
    if guest:
        guest.confirmed = False
        guest.save()
        return True
    return False

# Reset is_locked status for specific Guest after successful authentication
def reset_guest_lock_status(guest_id):
    guest = get_guest_by_id(guest_id=guest_id)
    if guest:
        guest.is_locked = False
        guest.failed_attempts = 0
        guest.locked_until = None
        guest.save()
        return True
    return False

# Increment failed login attempts for specific Guest
def increment_failed_login_attempts(guest_id):
    guest = get_guest_by_id(guest_id=guest_id)
    if guest:
        guest.failed_attempts += 1
        guest.save()
        return True
    return False

# Lock Guest account
def lock_guest_account(guest_id):
    guest = get_guest_by_id(guest_id=guest_id)
    if guest:
        guest.is_locked = True
        guest.save()
        return True
    return False

# Unlock Guest account
def unlock_guest_account(guest_id): 
    guest = get_guest_by_id(guest_id=guest_id)
    if guest:
        guest.is_locked = False
        guest.failed_attempts = 0
        guest.locked_until = None
        guest.save()
        return True
    return False

# Return Guest's secret friend
def get_secret_friend(guest):
    try:
        secret_friend = guest.secret_friend
        return secret_friend
    except Guest.DoesNotExist:
        return None
    
# Update Guest's gift idea
def update_guest_gift_idea(guest_id, gift_idea):
    guest = get_guest_by_id(guest_id=guest_id)
    if guest:
        guest.gift_idea = gift_idea
        guest.save()
        return True
    return False