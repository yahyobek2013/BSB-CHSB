# from django.contrib import admin
# from django.urls import path, include
# from django.contrib.auth import views as auth_views
# from quiz import views as quiz_views

# urlpatterns = [
#     # path('admin/', admin.site.urls),
    
#     # Login / Register (Django tayyor tizimidan foydalanamiz)
#     path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
#     path('logout/', quiz_views.logout_view, name='logout'),
#     path('register/', quiz_views.register, name='register'),
#     # Quiz yo'llari
#     # quiz_system/urls.py faylida
#     # quiz_system/urls.py faylida 20-qator atrofini toping
#     path('dashboard/', quiz_views.dashboard, name='dashboard'), # results_view o'rniga dashboard
#     path('', quiz_views.dashboard, name='home'),  # dashboard_view emas, dashboard bo'lishi kerak
#     path('result/<int:result_id>/', quiz_views.result_summary, name='result_summary'),
#     path('test/<int:subject_id>/<str:test_type>/', quiz_views.test_process, name='test_process'),
#     path('result/<int:result_id>/', quiz_views.result_summary, name='result_summary'),
#     path('', quiz_views.dashboard_view, name='home'),  # Asosiy sahifa
#     path('dashboard/', quiz_views.results_view, name='dashboard'), # Natijalar sahifasi
#     path('start-quiz/<int:subject_id>/', quiz_views.start_quiz, name='start_quiz'), # Testni boshlash
#     path('logout/', quiz_views.logout_view, name='logout'), # Chiqish
#     path('all-students/', quiz_views.all_students, name='all_students'),
#     path('admin/', admin.site.urls),
#     path('dashboard/', quiz_views.dashboard, name='dashboard'),
#     # ... boshqa url-lar
#     path('subjects/', quiz_views.subject_list, name='subjects'),
#     path('logout/', quiz_views.logout_view, name='logout'),
#     # SHU QATORNI QO'SHING:
#     path('upload-questions/', quiz_views.upload_questions, name='upload_questions'),
    
#     path('dashboard/', quiz_views.dashboard, name='dashboard'),
#     path('logout/', quiz_views.custom_logout, name='custom_logout'),
#     path('logout/', quiz_views.custom_logout, name='custom_logout'), # SHU QATORNI TEKSHIRING
#     path('dashboard/', quiz_views.dashboard, name='dashboard'),
#     path('quiz/<int:subject_id>/submit/', quiz_views.submit_quiz, name='submit_quiz'),
#     path('quiz/<int:subject_id>/submit/', quiz_views.submit_quiz, name='submit_quiz'),
#     # DIQQAT: Agar pastdagi qator bo'lsa, uni o'chirib tashlang:
#     # path('logout/', auth_views.LogoutView.as_view(), name='logout'), 
#     path('', quiz_views.subject_list, name='home'), 
#     # Yoki mavjud subjects yo'liga nom qo'shing:
#     path('subjects/', quiz_views.subject_list, name='subjects'),
#     # FAQAT mana shu qator qolishi kerak:
#     path('logout/', quiz_views.custom_logout, name='logout'),
#     # path('logout/', quiz_views.custom_logout, name='logout'), #
#     path('logout/', quiz_views.custom_logout, name='logout'),
#     path('', quiz_views.subject_list, name='subjects'),
#     path('quiz/<int:subject_id>/start/', quiz_views.start_quiz, name='start_quiz'),
#     path('quiz/<int:subject_id>/submit/', quiz_views.submit_quiz, name='submit_quiz'),
#     path('dashboard/', quiz_views.dashboard, name='dashboard'),
# ]





from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from quiz import views as quiz_views

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Avtorizatsiya (Login, Logout, Register)
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', quiz_views.logout_view, name='logout'),
    path('register/', quiz_views.register, name='register'),

    # Asosiy sahifa va Fanlar
    path('', quiz_views.subject_list, name='home'),
    path('subjects/', quiz_views.subject_list, name='subject_list'),

    # Test jarayoni
    path('test/<int:subject_id>/<str:test_type>/', quiz_views.test_process, name='test_process'),
    path('start-quiz/<int:subject_id>/', quiz_views.test_process, {'test_type': 'BSB'}, name='start_quiz'),
    path('result/<int:result_id>/', quiz_views.result_summary, name='result_summary'),

    # Statistika (O'quvchi uchun)
    path('my-dashboard/', quiz_views.dashboard, name='dashboard'),
    
    # Admin Paneli (Savollarni boshqarish va o'quvchilar natijalari)
    path('all-students/', quiz_views.all_students, name='all_students'),
    path('upload-questions/', quiz_views.upload_questions, name='upload_questions'),
    
    # Agar sizda admin_dashboard funksiyasi upload_questions bilan bir xil bo'lsa:
    path('admin-panel/', quiz_views.upload_questions, name='admin_dashboard'),
]

# quiz_system/urls.py faylini oching va urlpatterns qismini shunday yangilang:

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', quiz_views.logout_view, name='logout'),
    path('register/', quiz_views.register, name='register'),

    path('', quiz_views.subject_list, name='home'),
    path('subjects/', quiz_views.subject_list, name='subject_list'),
    path('all-subjects/', quiz_views.subject_list, name='subjects'), # BU QATORNI QO'SHING!
    # ESKI (xato berayotgan) qator:
    # path('test/submit/<int:subject_id>/', quiz_views.submit_quiz, name='submit_quiz'),
    # ESKI (xato berayotgan) qator:
# path('test/submit/<int:subject_id>/', quiz_views.submit_quiz, name='submit_quiz'),

# YANGI (to'g'ri) qator:
path('test/submit/<int:subject_id>/<str:test_type>/', quiz_views.test_process, name='submit_quiz'),
    path('test/submit/<int:subject_id>/<str:test_type>/', quiz_views.test_process, name='submit_quiz'),
    path('test/<int:subject_id>/<str:test_type>/', quiz_views.test_process, name='test_process'),
    path('start-quiz/<int:subject_id>/', quiz_views.test_process, {'test_type': 'BSB'}, name='start_quiz'),
    path('result/<int:result_id>/', quiz_views.result_summary, name='result_summary'),
    path('test/submit/<int:subject_id>/', quiz_views.submit_quiz, name='submit_quiz'),
    path('my-dashboard/', quiz_views.dashboard, name='dashboard'),
    path('all-students/', quiz_views.all_students, name='all_students'),
    path('upload-questions/', quiz_views.upload_questions, name='upload_questions'),
    path('admin-dashboard/', quiz_views.upload_questions, name='admin_dashboard'),
]