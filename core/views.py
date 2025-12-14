from random import random
from django.http import HttpResponse #type: ignore
from django.views import View #type: ignore
from django.shortcuts import render, redirect #type: ignore
from django.conf import settings
from .forms import FamilyGroupForm, GuestForm
from .models import FamilyGroup, Guest #type: ignore
from .services.auth import validate_username_and_pin, validatePIN, validateAdminPIN
from .services.assigment import assign_username_and_hashed_pins
from .services.queries import get_confirmed_guests_by_family_group, get_guest_by_pin, confirm_guest_attendance, cancel_guest_attendance
import random

# New home view with PIN and username validation
def home(request):
    error = None
    if request.method == 'POST':

        # Validate the PIN using the auth service. Asign the result (return) to a variable.
        passed_pint = request.POST.get('pin', '').strip()
        passed_username = request.POST.get('username', '').strip()

        validation_result = validate_username_and_pin(passed_username, passed_pint)

        # Check if the PIN is valid based on the validation result
        if validation_result["is_pin_valid"] and validation_result["is_username_valid"]:
            print("Username and PIN validated successfully.")
            request.session['authenticated'] = True
            request.session['guest_id'] = validation_result['guest'].guest_id
            request.session['guest_name'] = validation_result['guest'].name
            request.session['family_group_id'] = validation_result['guest'].family_group.family_group_id if validation_result['guest'].family_group else None
            request.session['guest_confirmed'] = validation_result['guest'].confirmed
            request.session['guest_username'] = validation_result['guest'].username
            request.session['ideal_gift'] = validation_result['guest'].ideal_gift
            request.session['secret_friend_id'] = validation_result['guest'].secret_friend.guest_id if validation_result['guest'].secret_friend else None
            print(f"Session Data: {request.session.items()}")
            return redirect('dashboard')
        else:
            error = validation_result.get('error')

    # Render the home page with any error messages from the validation
    return render(request, 'core/index.html', {'error': error})

# Home view with PIN form
def homeOnlyPIN(request):
    error = None
    if request.method == 'POST':

        # Validate the PIN using the auth service. Asign the result (return) to a variable.
        validation_result = validatePIN(request.POST.get('pin', '').strip())

        # Check if the PIN is valid based on the validation result
        if validation_result["pin_valid"]:
            print("PIN validated successfully.")
            request.session['authenticated'] = True
            request.session['guest_id'] = validation_result['guest'].guest_id
            request.session['guest_name'] = validation_result['guest'].name
            request.session['family_group_id'] = validation_result['guest'].family_group.family_group_id if validation_result['guest'].family_group else None
            request.session['guest_confirmed'] = validation_result['guest'].confirmed
            print(f"Session Data: {request.session.items()}")
            return redirect('dashboard')
        else:
            print("PIN validation failed.")
            error = validation_result.get('error')

    # Render the home page with any error messages from the validation
    return render(request, 'core/index.html', {'error': error})


# Dashboard page view after successful authentication
def dashboard(request):
    if not request.session.get('authenticated'):
        return redirect('home')
    
    confirmed_family_groups = get_confirmed_guests_by_family_group()
    return render(request, 'core/dashboard.html', {'confirmed_family_groups': confirmed_family_groups})

#View to view secret friend
def view_secret_friend(request):    
    if not request.session.get('authenticated'):
        return redirect('home')
    return render(request, 'core/secret_friend.html')

# View to confirm assistance
def confirm_assistance(request):
    if not request.session.get('authenticated'):
        print("User not authenticated for confirmation. Redirecting to home.")
        return redirect('home')
    
    if request.method == 'GET':
        action = request.GET.get('action')
        print(f"Action received for confirmation: {action}")

        if action == 'confirm':
            if confirm_guest_attendance(request.session.get('guest_id')):
                request.session['guest_confirmed'] = True
                print(f"Guest with PIN {request.session.get('guest_id')} confirmed attendance.")
        elif action == 'cancel':
            print(f"Attempting to cancel attendance for Guest ID: {request.session.get('guest_id')}")
            if cancel_guest_attendance(request.session.get('guest_id')):
                request.session['guest_confirmed'] = False
                print(f"Guest with PIN {request.session.get('guest_id')} canceled attendance.")
        
    
    return render(request, 'core/confirmacion.html')

# Logout view to clear session
def logout(request):
    request.session.flush()
    return redirect('home')

# ADDING NEW VIEWS FOR ADMIN CONSOLE AND FAMILY GROUP #

# Validate access for Console
def console(request):
    if not request.session.get('authenticated'):
        print("User not authenticated for Console. Redirecting to home.")
        return redirect('home')
    
    print("User authenticated for Console")
    return render(request, 'core/console/console.html')

#Admin Console View
def admin_console(request):
    if not request.session.get('authenticated'):
        return redirect('home')
    
    # Function to generate a unique PIN
    def generar_pin_unico():
        while True:
            pin = str(random.randint(100000, 999999))
            if not Guest.objects.filter(pin=pin).exists():
                return pin
    
    # Function to get all Family Groups
    def getFamilyGroups():
        return FamilyGroup.objects.all()
    
    def getFamilyGuests():
        return Guest.objects.all()
    
    if request.method == 'GET':
        print("Admin Console accessed via GET request.")
        return render(request, 'core/console/admin.html', {'unique_random_pin': generar_pin_unico(), 'family_groups': getFamilyGroups(), 'family_guests': getFamilyGuests()})
    
    if request.method == 'POST':
        print("Admin Console accessed via POST request.")
        action = request.POST.get('action')
        print(f"Action: {action}")

        if action == 'admin_console':
            validation_panel = validateAdminPIN(request.POST.get('pin', '').strip())
            print(f"Admin PIN validation result: {validation_panel}")
    
            if validation_panel["is_pin_valid"]:
                print("PIN validated successfully for admin console.")   
                return render(request, 'core/console/admin.html', {'unique_random_pin': generar_pin_unico(), 'family_groups': getFamilyGroups(), 'family_guests': getFamilyGuests()})
            else:
                print("Admin PIN validation failed.")
                error = validation_panel.get('error')
                return render(request, 'core/console/console.html', {'error': error})
        
        if action == 'save_family_group':
            print(f"Action: {action}")
            return render(request, 'core/console/admin.html', {'unique_random_pin': generar_pin_unico(),'family_groups': getFamilyGroups(), 'family_guests': getFamilyGuests()})

# View to save Family Group
def save_family_group(request):
    if request.method == 'POST':
        form = FamilyGroupForm(request.POST)
        print("Form data received:", form.data)
        if form.is_valid(): 
            form.save()
            return redirect('admin_console')
        else:
            print("Form is invalid. Errors:", form.errors)

#View to add Guest to Family Group
def addGuest(request):
    if request.method == 'POST':
        form = GuestForm(request.POST)
        print("Form data received for Guest:", form.data)

        # Variables from form
        family_group = request.POST.get('family_group')
        name = request.POST.get('guest_name')
        pin = request.POST.get('pin')
        is_confirmed = request.POST.get('isConfirmed') == 'on'

        try:
            family_group = FamilyGroup.objects.get(family_group_id = family_group)
            new_guest = Guest(
                family_group=family_group,
                name=name,
                pin=pin,
                confirmed=is_confirmed
            )
            new_guest.save()
            print(f"New guest {name} added to family group {family_group.family_name}.")
            return redirect('admin_console')
        except FamilyGroup.DoesNotExist:
            print(f"Family Group with ID {family_group} does not exist.")
            return redirect('admin_console')
        
#View to confirm username and PIN assignment
def assigments(request):
    if not request.session.get('authenticated'):
        return redirect('home')
    
    action = request.GET.get('action')
    print(f"Action received for assignment: {action}")

    if action == 'assignPinUser':
        guest_id = request.session.get('guest_id')
        try:
            guest = Guest.objects.get(guest_id=guest_id)
            return render(request, 'core/username_pin_confirmation.html', {'guest': guest})
        except Guest.DoesNotExist:
            print(f"Guest with ID {guest_id} does not exist.")
            return redirect('home')
        
#view to save ideal gift
def save_gift_idea(request):
    if not request.session.get('authenticated'):
        return redirect('home')
    
    if request.method == 'GET':
        action = request.GET.get('action')
        gift_idea = request.GET.get('gift_idea', '').strip()
        print(f"Action received for saving gift idea: {action}")

        if action == 'save_gift_idea' and gift_idea:
            guest_id = request.session.get('guest_id')
            try:
                guest = Guest.objects.get(guest_id=guest_id)
                guest.ideal_gift = gift_idea
                guest.save()
                request.session['ideal_gift'] = gift_idea
                print(f"Guest with ID {guest_id} saved ideal gift: {gift_idea}")
            except Guest.DoesNotExist:
                print(f"Guest with ID {guest_id} does not exist.")
        
    return render(request, 'core/save_gift.html')