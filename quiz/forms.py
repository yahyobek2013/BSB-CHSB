from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re

class UzbRegisterForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=13,
        label="Telefon raqamingiz",
        widget=forms.TextInput(attrs={
            'placeholder': '+998901234567',
            'class': 'phone-input'
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('phone_number',)

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        # O'zbekiston raqami formati: +998 bilan boshlanishi va 13 ta belgi bo'lishi kerak
        pattern = r'^\+998\d{9}$'
        if not re.match(pattern, phone):
            raise forms.ValidationError("Telefon raqami +998XXXXXXXXX formatida bo'lishi shart!")
        return phone