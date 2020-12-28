from django import forms


class AddressForm(forms.Form):
    address = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class': 'address_input'}))
