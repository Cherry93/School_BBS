from django.contrib.auth.forms import UserCreationForm
from .models import User



class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email","student_num","major","qq_num")


