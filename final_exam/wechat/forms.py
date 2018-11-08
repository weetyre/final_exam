from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext, gettext_lazy as _

from final_exam.wechat.models import MyUser


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=50, widget=forms.EmailInput(attrs={'class': 'from-input'}))
    password = forms.CharField(label='Password', min_length=6, max_length=18,
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ChangeEmailForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=50, widget=forms.EmailInput(attrs={'class': 'from-input'}))
    
    def clean_email(self):
        email = self.cleaned_data['email']
        email_filter = MyUser.objects.filter(email=email)
        if len(email_filter) > 0:
            raise forms.ValidationError(
                _('email already taken.'), code='invalid email'
            )


class MyPasswordChangeForm(PasswordChangeForm):
    error_messages = {
        **PasswordChangeForm.error_messages,
        'password_incorrect': _("invalid password."),
    }

    def clean_old_password(self):
        super.old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(super.old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return super.old_password
