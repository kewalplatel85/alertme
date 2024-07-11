from django import forms
import re
from django.core.exceptions import ValidationError

def phone_number_validator(value):
    pattern = re.compile(r'^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$')
    match = pattern.match(value)
    if not match:
        raise ValidationError("Invalid phone number format.")
    
    cleaned_value = ''.join(match.groups(''))
    return cleaned_value

class PackageForm(forms.Form):
    mailbox_number = forms.CharField(label='Mailbox Number', max_length=100)
    num_packages = forms.IntegerField(label='Number of Packages', min_value=1)

def get_tracking_form(mailbox_number, num_packages):
    class TrackingForm(forms.Form):

        def __init__(self,  *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.init_mailbox_number = mailbox_number
            self.init_tracking_numbers = ''
            for i in range(num_packages):
                self.fields[f'tracking_number_{i+1}'] = forms.CharField(label=f'Tracking Number {i+1}', max_length=100)
            # self.mailbox_number = forms.CharField(widget=forms.HiddenInput())
            # self.tracking_numbers = forms.CharField(widget=forms.HiddenInput())
            # # print(self.tracking_numbers)

            # for i in range(num_packages):
            #     self.fields[f'tracking_number_{i+1}'] = forms.CharField(label=f'Tracking Number {i+1}', max_length=100)
        
    return TrackingForm


class ReplyForm(forms.Form):
    to_number = forms.CharField(label='To', max_length=15, validators=[phone_number_validator])
    body = forms.CharField(label='Message', max_length=160, widget=forms.Textarea)


class CustomSMSForm(forms.Form):
    to_number = forms.CharField(label='To', max_length=15, validators=[phone_number_validator])
    body = forms.CharField(label='Message', max_length=160, widget=forms.Textarea)