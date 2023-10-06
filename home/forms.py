from django import forms
from .models import Slot

class CarForm(forms.Form):
    name = forms.ChoiceField(
         label='Select Vehicle Type',
         choices=[('sedan', 'Sedan'), ('suv', 'SUV'),('coupe','Coupe')],
        widget=forms.Select(attrs={'onchange': 'this.form.submit();', 'class': 'custom-select'})
    )

class BikeForm(forms.Form):
    name = forms.ChoiceField(
         label='Select Vehicle Type',
         choices=[('bmw', 'Bmw'), ('royalenfield', 'Royal Enfiled')],
        widget=forms.Select(attrs={'onchange': 'this.form.submit();', 'class': 'custom-select'})
    )
   


class SlotForm(forms.ModelForm):
    # date = forms.DateField(widget=forms.Select(attrs={'id': 'dateDropdown'}))
    class Meta:
        model = Slot
        # 'date',
        fields = ['timeslot']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date','id': 'dateDropdown'}),
            'timeslot': forms.Select(attrs={'class': 'custom-timeslot'}),
        }
        
        # {{ form.date.label_tag }} {{ form.date}}


class CouponForm(forms.Form):
    coupon_code = forms.CharField(max_length=20)
