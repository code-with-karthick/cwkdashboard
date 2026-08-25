from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Course URLs
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.course_add, name='course_add'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('courses/<int:pk>/update/', views.course_update, name='course_update'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),
    
    # Student URLs
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_add, name='student_add'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/update/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    
    # Faculty URLs
    path('faculty/', views.faculty_list, name='faculty_list'),
    path('faculty/add/', views.faculty_add, name='faculty_add'),
    path('faculty/<int:pk>/', views.faculty_detail, name='faculty_detail'),
    path('faculty/<int:pk>/update/', views.faculty_update, name='faculty_update'),
    path('faculty/<int:pk>/delete/', views.faculty_delete, name='faculty_delete'),
    
    # Payment URLs
    path('payments/', views.payment_list, name='payment_list'),
    path('payments/add/', views.payment_add, name='payment_add'),
    path('payments/<int:pk>/', views.payment_detail, name='payment_detail'),
    path('payments/<int:pk>/update/', views.payment_update, name='payment_update'),
    path('payments/<int:pk>/delete/', views.payment_delete, name='payment_delete'),
    
    # Reports and Settings
    path('reports/', views.reports_view, name='reports'),
    path('settings/', views.settings_view, name='settings'),
]