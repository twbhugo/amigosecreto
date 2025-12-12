from django.conf import settings
from core.models import Guest
from core.services.queries import get_guest_by_pin, get_guest_by_username, get_pin_by_username, reset_guest_lock_status, increment_failed_login_attempts, lock_guest_account

# Validate Username and PIN
def validate_username_and_pin(username: str, pin: str) -> dict:

    print(f"Extracting Username: {username} and PIN: '{pin}'")
    if not username or not check_pin_format(pin):
        print("Username or PIN not provided.")
        return {"is_username_valid": False, "is_pin_valid": False, "error": "Username o PIN Incorrecto, por favor intenta de nuevo."}
    else:
        guest = get_guest_by_username(username)

        if not guest:
            print("No guest found with the provided username.")
            return {"is_username_valid": False, "is_pin_valid": False, "error": "Username o PIN Incorrecto, por favor intenta de nuevo."}
        else:
            print("Guest found. Name:", guest.name, "PIN", guest.pin, " - Validating locked status and PIN format.")
            sotored_pin = get_pin_by_username(username)

            # Check if the guest is locked
            if guest.is_locked:
                print("Guest account is locked.")
                return {"is_username_valid": False, "is_pin_valid": False, "error": "Tu acceso está bloqueado. Por favor contacta al administrador."}
            

        if int(sotored_pin) != int(pin):
            print(f"Comparing provided PIN ({pin}) with stored PIN ({sotored_pin}).")
            print("PIN does not match.")

            total_failed_attempts = guest.failed_attempts + 1
            print(f"Total failed attempts: {total_failed_attempts}")
            # Increment failed login attempts
            increment_failed_login_attempts(guest.guest_id)

            # Lock the account if failed attempts exceed limit
            if total_failed_attempts >= settings.MAX_FAILED_LOGIN_ATTEMPTS:
                lock_guest_account(guest.guest_id)
                print("Guest account has been locked due to too many failed attempts.")
                return {"is_username_valid": False, "is_pin_valid": False, "error": "Tu acceso está bloqueado debido a múltiples intentos fallidos. Por favor contacta al administrador."}

            return {"is_username_valid": True, "is_pin_valid": False, "error": "PIN Incorrecto, por favor intenta de nuevo."}

    # If all checks pass, the Username and PIN are valid
    print("Username and PIN validated successfully. Resetting lock status if necessary.")
    reset_guest_lock_status(guest.guest_id)
    return {"is_pin_valid": True, "is_username_valid": True, "guest": guest}

# Validate PIN
def validatePIN(pin: str) -> dict:

    print(f"Validating General Access PIN: '{pin}'")
    
    pint_format = check_pin_format(pin)
    if not pint_format["pin_valid"]:
        return pint_format
    
    guest = get_guest_by_pin(pin)
    if not guest:
        return {"pin_valid": False, "error": "PIN Incorrecto, por favor intenta de nuevo."}

    # If all checks pass, the PIN is valid
    return {"pin_valid": True, "guest": guest}


# Generic helper function to check PIN format
def check_pin_format(pin: str) -> dict:
    # Check if PIN is provided
    if not pin:
        return False

    if not pin.isdigit():
        return False
    
    if len(pin) != 6:
        return False
    
    return True


# Validate Admin PIN
def validateAdminPIN(pin: str) -> dict:

    print(f"Validating Admin PIN: '{pin}'")
    
    pint_format = check_pin_format(pin)
    
    if not pint_format or pin.strip() != settings.ADMIN_AUTH_PIN:
        return {"is_pin_valid": False, "error": "Incorrect Admin PIN. Please try again."}
    
    # If all checks pass, the Admin PIN is valid
    return {"is_pin_valid": True}