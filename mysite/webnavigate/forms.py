from django import forms

class RegisterWebsite(forms.Form):
    site_name = forms.CharField(max_length = 50, required = True,
    	widget=forms.TextInput(
    		attrs={'class' : 'form-control', 'placeholder' : 'Google',}))

    site_address = forms.URLField(max_length = 50, required = True,
    	widget=forms.URLInput(
    		attrs={'class' : 'form-control', 'placeholder' : 'https://google.com',}))
