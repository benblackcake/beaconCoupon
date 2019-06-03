from django import forms

class NameForm(forms.Form):
    URL_IP=forms.CharField(label='Write IP',max_length=100,widget=forms.TextInput(
        attrs={
            'class' :'form-control',
            'placeholder':'Write IP'
        }
    ))
    functionName=forms.CharField(label='Write Function Name',max_length=100,widget=forms.TextInput(
        attrs={
            'class' :'form-control',
            'placeholder':'Write functionName'
        }
    ))
    UUID=forms.CharField(label='Write UUID',max_length=100,widget=forms.TextInput(
        attrs={
            'class' :'form-control',
            'placeholder':'Write UUID'
        }
    ))