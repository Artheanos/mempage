from django import forms


class UploadFileForm(forms.Form):
    header = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Title'
    }))

    file = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'custom-file-input',
        'id': 'file_input',
        'accept': 'image/*'
    }))
