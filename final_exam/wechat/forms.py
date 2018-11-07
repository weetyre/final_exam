from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=50, widget=forms.EmailInput(attrs={'class': 'from-input'}))
    password = forms.CharField(label='Password', min_length=6, max_length=18,
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class RegisterForm(LoginForm):
    password_confirm = forms.CharField(label='Password confirm', min_length=6,
                                       widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ChangeEmailForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=50, widget=forms.EmailInput(attrs={'class': 'from-input'}))
