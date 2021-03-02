from django.shortcuts import redirect

# my mixins

class LogoutRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        # print("my LogoutRequiredMixin", request.user.username, request.user.email, request.user.user_role,
        # request.user.password)
        if request.user.is_authenticated:
            if request.user.user_role == 'MENTOR':
                return redirect('students')
            elif request.user.user_role == 'STUDENT':
                return redirect('enrollment')
        return super().dispatch(request, *args, **kwargs)

class MentorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.user_role != 'MENTOR':
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class StudentRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.user_role != 'STUDENT':
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
