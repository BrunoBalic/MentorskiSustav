from django.urls import path

from . import views

urlpatterns = [
    path('courses/', views.CoursesView.as_view(), name='courses'),
    path('course-detail2/<pk>', views.CourseDetailView2.as_view(), name='course-detail2'),
    path('course-detail3/<pk>', views.CourseDetailView3.as_view(), name='course-detail3'),
    # path('course-edit/<int:course_id>', views.CourseEditView.as_view(), name='course-edit'),
    path('course-edit/<pk>', views.CourseEditView.as_view(), name='course-edit'),
    path('course-create/', views.CourseCreateView.as_view(), name='course-create'),
    # ova dva rade samo treba prolagodit template jer je ime u contextu drugacije...
    path('course-detail/<int:course_id>', views.CourseDetailView.as_view(), name='course-detail'),
    path('course-detail4/<int:course_id>', views.CourseDetailView4.as_view(), name='course-detail4'),
]
