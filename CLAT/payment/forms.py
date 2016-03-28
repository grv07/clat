from django import forms

class OrderForm(forms.Form):
    # cart order related fields
    txnid = forms.CharField()
    productinfo = forms.CharField()
    amount = forms.DecimalField(decimal_places = 2)

    # Student details
    firstname = forms.CharField(max_length = 30)
    email = forms.EmailField(max_length = 70)
    phone = forms.RegexField(regex = r'\d{10}', min_length = 10, max_length = 10)
