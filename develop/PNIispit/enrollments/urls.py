from django.urls import path

from . import views

urlpatterns = [
    # path('upisni-list', views.EnrollmentView.as_view(), name='enrollment'),
    # path('upisni-list/<int:url_student_id>', views.EnrollmentView.as_view(), name='enrollment_param'),
    # novo
    path('upisni-list', views.EnrollmentStudentView.as_view(), name='enrollment'),
    path('upisni-list/<int:url_student_id>', views.EnrollmentMentorView.as_view(), name='enrollment_param'),

    # zadaci
    path('custom1', views.View1.as_view(), name='custom1'),
    path('custom2', views.View2.as_view(), name='custom2'),
    path('custom2d/<str:s>', views.View2detail.as_view(), name='custom2d'),
]
