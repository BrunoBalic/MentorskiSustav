from django.contrib.auth.forms import UserCreationForm

from users.models import Users

# cini mi se da je ovo najbolji nacin za formu za kreiranje novog usera
# nasljedim UserCreationForm i override-am Meta podatke, tj. postavim svoj model Korisnici
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = Users
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            # "user_role",
            "status",
        )

    # ako hocu nesto dodatno napravit onda override-am save()
    def save(self, commit=True):
        user = super(MyUserCreationForm, self).save(commit=False)
        user.user_role = "STUDENT"
        if commit:
            user.save()
        return user
