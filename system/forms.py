from django import forms

class LoginForm(forms.Form):
    account = forms.CharField(
        label='Account', 
        max_length=50,
        required=True, 
        error_messages={'required': 'Please input your account.'}, 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Input your account.',
                'id': 'account',
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        label='Password', 
        max_length=50,
        required=True, 
        error_messages={'required': 'Please input your password.'}, 
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Input your password.',
                'id': 'password',
                'class': 'form-control'
            }
        )
    )

    def clean_account(self):
        account = self.cleaned_data['account']
        if account is None:
            raise forms.ValidationError('The account are required.')
        return account

    def clean_password(self):
        password = self.clean_password['password']
        if password is None:
            raise forms.ValidationError('The account are required.')
        return password


class RegisteForm(forms.Form):
    account = forms.CharField(
        label='Account', 
        max_length=50,
        required=True, 
        error_messages={'required': 'Please input your account.'}, 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Input your account',
                'id': 'account',
                'class': 'form-control'
            }
        )
    )
    email = forms.CharField(
        label='Email',
        max_length=50,
        required=False,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Input your email',
                'id': 'email',
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        label='Password', 
        max_length=50,
        required=True, 
        error_messages={'required': 'Please input your password.'}, 
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Input your password',
                'id': 'password',
                'class': 'form-control'
            }
        )
    )
    confirmpassword = forms.CharField(
        label='Password', 
        max_length=50,
        required=True, 
        error_messages={'required': 'Please input your password.'}, 
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm your password',
                'id': 'confirmpassword',
                'class': 'form-control'
            }
        )
    )

    def clean_password(self):
        password = self.cleaned_data['password']
        confirmpassword = self.cleaned_data['confirmpassword']
        if password and confirmpassword and password != confirmpassword:
            raise forms.ValidationError('Password confirm failed!')
        return confirmpassword

    def clean_account(self):
        account = self.cleaned_data['account']
        if account is None:
            raise forms.ValidationError('The account are required.')
        return account

    def cleaned_email(self):
        email = self.cleaned_data['email']
        return email
