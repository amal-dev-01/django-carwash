from django import forms
from .models import UserDetails
import re



class EditUserForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ('first_name', 'last_name', 'email', 'phone_number')
        
        
class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True,
    )

    class Meta:
        model = UserDetails
        fields=('first_name','last_name','email','phone_number','password','confirm_password') 
        
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.fields["first_name"].widget.attrs["placeholder"] = "First Name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Last Name"
        self.fields["email"].widget.attrs["placeholder"] = "Email"
        self.fields["phone_number"].widget.attrs["placeholder"] = "Phone Number"
        self.fields["password"].widget.attrs["placeholder"] = "Password"
        self.fields["confirm_password"].widget.attrs["placeholder"] = "Confirm Password"
        
        
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control form-outline mb-4"  
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        phone_number = cleaned_data.get('phone_number')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        if len(password)<3:
            raise forms.ValidationError('password must be atleast 5 length long')

        return cleaned_data
    
    def clean_name(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        
        if not re.match(r'^[a-zA-Z]+$', first_name) or not re.match(r'^[a-zA-Z]+$', last_name):
            raise forms.ValidationError('First name and last name must contain only alphabetic characters.')

        return cleaned_data