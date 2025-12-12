from django import forms
from .models import Guest, FamilyGroup

class FamilyGroupForm(forms.ModelForm):
    class Meta:
        model = FamilyGroup
        fields = ['family_name']
        widgets = {
            'family_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Family Name'}),
        }

class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['name', 'pin', 'confirmed', 'secret_friend', 'ideal_gift', 'family_group']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Guest Name'}),
            'pin': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'PIN'}),
            'confirmed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'secret_friend': forms.Select(attrs={'class': 'form-control'}),
            'ideal_gift': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ideal Gift'}),
            'family_group': forms.Select(attrs={'class': 'form-control'}),
        }