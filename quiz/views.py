# import random
# import openpyxl
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import login, logout
# from django.contrib import messages
# from django.utils import timezone
# from .models import Subject, Question, QuizResult
# from .forms import UzbRegisterForm

# # 1. Ro'yxatdan o'tish
# def register(request):
#     if request.method == 'POST':
#         form = UzbRegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('subjects')
#     else:
#         form = UzbRegisterForm()
#     return render(request, 'registration/register.html', {'form': form})

# # 2. Tizimdan chiqish
# def custom_logout(request):
#     logout(request)
#     return redirect('login')

# # 3. Fanlar ro'yxati (Xatolik tuzatildi: questions)
# @login_required
# def subject_list(request):
#     # Subject modelida related_name='questions' bo'lgani uchun 'questions__isnull' ishlatiladi
#     subjects = Subject.objects.filter(questions__isnull=False).distinct()
#     return render(request, 'quiz/subjects.html', {'subjects': subjects})

# # 4. Testni boshlash
# @login_required
# def start_quiz(request, subject_id):
#     subject = get_object_or_404(Subject, id=subject_id)
#     test_type = request.GET.get('type', 'BSB') # URL orqali kelayotgan test turi
    
#     questions_query = Question.objects.filter(subject=subject, test_type=test_type)
    
#     if not questions_query.exists():
#         questions_query = Question.objects.filter(subject=subject)
        
#     questions = list(questions_query)
#     random.shuffle(questions)
    
#     request.session['quiz_start_time'] = str(timezone.now())
    
#     return render(request, 'quiz/test_process.html', {
#         'subject': subject,
#         'questions': questions,
#         'test_type': test_type
#     })

# # 5. Testni topshirish va Natija (Biriktirildi va xatosiz)
# @login_required
# def submit_quiz(request, subject_id):
#     subject = get_object_or_404(Subject, id=subject_id)
    
#     if request.method == 'POST':
#         test_type = request.POST.get('test_type', 'BSB')
#         questions = Question.objects.filter(subject=subject, test_type=test_type)
        
#         if not questions.exists():
#             questions = Question.objects.filter(subject=subject)

#         results_details = []
#         correct_count = 0
#         total_questions = questions.count()
        
#         for q in questions:
#             user_answer = request.POST.get(f'q{q.id}')
#             # Modelda 'correct_answer' borligi aniqlandi
#             is_correct = (user_answer == q.correct_answer)
            
#             if is_correct:
#                 correct_count += 1
                
#             results_details.append({
#                 'question': q,
#                 'user_answer': user_answer if user_answer else "Belgilanmagan",
#                 'correct_answer': q.get_correct_answer_display(), 
#                 'is_correct': is_correct
#             })
        
#         # Natijalarni hisoblash
#         score = int((correct_count / total_questions * 100)) if total_questions > 0 else 0
#         wrong_count = total_questions - correct_count
        
#         # Bazaga saqlash
#         QuizResult.objects.create(
#             user=request.user,
#             subject=subject,
#             test_type=test_type,
#             total_questions=total_questions,
#             correct_count=correct_count,
#             wrong_count=wrong_count,
#             score_percentage=score
#         )
        
#         context = {
#             'subject': subject,
#             'score': score,
#             'total': total_questions,
#             'correct': correct_count,
#             'wrong': wrong_count,
#             'results_details': results_details,
#         }
        
#         return render(request, 'quiz/result_summary.html', context)
    
#     return redirect('subject_list')

# # 6. Excel orqali yuklash
# @login_required
# def upload_questions(request):
#     if not request.user.is_staff:
#         messages.error(request, "Sizda bunday huquq yo'q!")
#         return redirect('subjects')

#     if request.method == "POST" and request.FILES.get('excel_file'):
#         excel_file = request.FILES['excel_file']
#         subject_id = request.POST.get('subject')
        
#         try:
#             current_subject = Subject.objects.get(id=subject_id)
#             wb = openpyxl.load_workbook(excel_file)
#             sheet = wb.active

#             count = 0
#             for row in sheet.iter_rows(min_row=2, values_only=True):
#                 if not row or not row[1]: # Savol matni bo'sh bo'lsa o'tkazib yuborish
#                     continue

#                 obj, created = Question.objects.get_or_create(
#                     subject=current_subject,
#                     text=row[1], # Excelda 2-ustun savol matni deb olindi
#                     defaults={
#                         'option_a': row[2],
#                         'option_b': row[3],
#                         'option_c': row[4],
#                         'correct_answer': str(row[5]).lower(), # a, b, c
#                         'test_type': row[6] if len(row) > 6 else 'BSB'
#                     }
#                 )
#                 if created:
#                     count += 1
            
#             messages.success(request, f"Baza yangilandi! {count} ta yangi savol qo'shildi.")
#         except Exception as e:
#             messages.error(request, f"Xatolik yuz berdi: {e}")
            
#         return redirect('subject_list')
    
#     return render(request, 'quiz/upload.html', {'subjects': Subject.objects.all()})

# # 7. Dashboard
# @login_required
# def dashboard(request):
#     results = QuizResult.objects.filter(user=request.user).order_by('-date_taken')
#     return render(request, 'quiz/dashboard.html', {'results': results})

# def custom_logout(request):
#     logout(request)
#     return redirect('login')


# @login_required
# def subject_list(request):
#     # Savoli bor fanlarni olamiz
#     subjects = Subject.objects.filter(questions__isnull=False).distinct()
    
#     # Admin sozlamalarini olamiz (is_bsb_active, is_chsb_active)
#     from .models import QuizSettings
#     settings = QuizSettings.objects.first()
    
#     # Har bir fan uchun o'quvchi topshirganmi yoki yo'qmi tekshiramiz
#     for subject in subjects:
#         # O'quvchi ushbu fandan BSB topshirganmi?
#         subject.user_has_bsb = QuizResult.objects.filter(
#             user=request.user, subject=subject, test_type='BSB'
#         ).exists()
        
#         # O'quvchi ushbu fandan CHSB topshirganmi?
#         subject.user_has_chsb = QuizResult.objects.filter(
#             user=request.user, subject=subject, test_type='CHSB'
#         ).exists()

#     context = {
#         'subjects': subjects,
#         'settings': settings,
#     }
#     return render(request, 'quiz/subjects.html', context)

# @login_required
# def upload_questions(request):
#     if not request.user.is_staff:
#         return redirect('subjects')
#     # Savol yuklash mantiqi bu yerda bo'ladi...
#     return render(request, 'quiz/add.html', {'subjects': Subject.objects.all()})

# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .models import Subject, Question, QuizResult, QuizSettings
# from django.db.models import Sum

# @login_required
# def subject_list(request):
#     subjects = Subject.objects.filter(questions__isnull=False).distinct()
#     settings = QuizSettings.objects.first()
    
#     # Har bir fan uchun topshirilganlik holatini tekshirish
#     for subject in subjects:
#         subject.user_has_bsb = QuizResult.objects.filter(
#             user=request.user, subject=subject, test_type='BSB'
#         ).exists()
#         subject.user_has_chsb = QuizResult.objects.filter(
#             user=request.user, subject=subject, test_type='CHSB'
#         ).exists()

#     return render(request, 'quiz/subjects.html', {
#         'subjects': subjects,
#         'settings': settings
#     })

# @login_required
# def dashboard(request):
#     results = QuizResult.objects.filter(user=request.user).order_by('-date_taken')
#     total_correct_sum = results.aggregate(Sum('correct_count'))['correct_count__sum'] or 0
    
#     avg_score = 0
#     if results.exists():
#         avg_score = sum(r.score_percentage for r in results) / results.count()

#     return render(request, 'quiz/dashboard.html', {
#         'results': results,
#         'total_correct_sum': total_correct_sum,
#         'total_average_percentage': avg_score
#     })

# @login_required
# def upload_questions(request):
#     if not request.user.is_staff:
#         return redirect('subjects')
#     # Excel yuklash mantiqi shu yerda bo'ladi
#     return render(request, 'quiz/add.html', {'subjects': Subject.objects.all()})


# def subject_list(request):
#     subjects = Subject.objects.all()
#     settings = QuizSettings.objects.last()
#     return render(request, 'quiz/subjects.html', {
#         'subjects': subjects,
#         'quiz_settings': settings # 'settings' so'zi o'rniga 'quiz_settings' ishlating, Django sozlamalari bilan adashmaslik uchun
#     })

# import pandas as pd
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .models import Subject, Question

# def upload_questions(request):
#     if not request.user.is_staff:
#         return redirect('subjects')

#     if request.method == 'POST':
#         upload_type = request.POST.get('upload_type')
#         subject_id = request.POST.get('subject')
#         subject = Subject.objects.get(id=subject_id)

#         # 1. EXCEL ORQALI YUKLASH
#         if upload_type == 'excel' and request.FILES.get('excel_file'):
#             file = request.FILES['excel_file']
#             try:
#                 df = pd.read_excel(file)
#                 # Excel ustunlari: Savol, A, B, C, Javob, Tur (BSB/CHSB)
#                 count = 0
#                 for _, row in df.iterrows():
#                     Question.objects.create(
#                         subject=subject,
#                         text=row[0],
#                         option_a=row[1],
#                         option_b=row[2],
#                         option_c=row[3],
#                         correct_answer=str(row[4]).upper(),
#                         test_type=row[5] if len(row) > 5 else 'BSB'
#                     )
#                     count += 1
#                 messages.success(request, f"Muvaffaqiyatli: {count} ta savol bazaga qo'shildi!")
#             except Exception as e:
#                 messages.error(request, f"Xatolik yuz berdi: {e}")

#         # 2. QO'LDA QO'SHISH
#         elif upload_type == 'manual':
#             Question.objects.create(
#                 subject=subject,
#                 text=request.POST.get('text'),
#                 option_a=request.POST.get('option_a'),
#                 option_b=request.POST.get('option_b'),
#                 option_c=request.POST.get('option_c'),
#                 correct_answer=request.POST.get('correct_answer'),
#                 test_type=request.POST.get('test_type')
#             )
#             messages.success(request, "Savol qo'lda muvaffaqiyatli qo'shildi!")

#     subjects = Subject.objects.all()
#     questions = Question.objects.all().order_by('-id')[:10] # Oxirgi 10 ta savol
#     return render(request, 'quiz/upload-questions.html', {
#         'subjects': subjects,
#         'questions': questions
#     })

# import pandas as pd
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .models import Subject, Question

# def update_questions(request):
#     if not request.user.is_staff:
#         return redirect('subjects')

#     if request.method == "POST":
#         upload_type = request.POST.get('upload_type')

#         # 1. FANNI BAZAGA SAQLASH
#         if upload_type == 'add_subject':
#             name = request.POST.get('subject_name')
#             if name:
#                 # Direct create orqali bazaga yozamiz
#                 Subject.objects.create(
#                     name=name, 
#                     description=request.POST.get('description', '')
#                 )
#                 messages.success(request, f"'{name}' fani databasega muvaffaqiyatli yozildi!")

#         # 2. QO'LDA SAVOLNI BAZAGA SAQLASH
#         elif upload_type == 'manual':
#             sub_id = request.POST.get('subject')
#             Question.objects.create(
#                 subject_id=sub_id,
#                 text=request.POST.get('text'),
#                 option_a=request.POST.get('option_a'),
#                 option_b=request.POST.get('option_b'),
#                 option_c=request.POST.get('option_c'),
#                 correct_answer=request.POST.get('correct_answer'),
#                 test_type=request.POST.get('test_type')
#             )
#             messages.success(request, "Savol databasega saqlandi va ro'yxatga qo'shildi!")

#         # 3. EXCELNI BAZAGA O'TKAZISH
#         elif upload_type == 'excel':
#             subject_id = request.POST.get('subject')
#             excel_file = request.FILES.get('excel_file')
#             if excel_file:
#                 df = pd.read_excel(excel_file)
#                 # Bazaga bittalab yozib chiqish
#                 for _, row in df.iterrows():
#                     Question.objects.create(
#                         subject_id=subject_id,
#                         text=row[0],
#                         option_a=row[1],
#                         option_b=row[2],
#                         option_c=row[3],
#                         correct_answer=str(row[4]).lower(),
#                         test_type=row[5] if len(row) > 5 else 'BSB'
#                     )
#                 messages.success(request, "Exceldagi barcha savollar bazaga o'tkazildi!")

#         # SAQLASH TUGAGACH SAHIFANI YANGILASH (Double-submit oldini olish)
#         return redirect('update_questions')

#     # BAZADAGI MA'LUMOTLARNI EKRANGA CHIQARISH UCHUN O'QIYMIZ
#     all_subjects = Subject.objects.all().order_by('-id')
#     # select_related bazadan ma'lumotni tezroq va aniqroq o'qiydi
#     recent_questions = Question.objects.select_related('subject').all().order_by('-id')[:10]
    
#     return render(request, 'quiz/update-questions.html', {
#         'subjects': all_subjects,
#         'questions': recent_questions
#     })

# from django.shortcuts import render, redirect, get_object_or_404 # get_object_or_404 qo'shildi

# def upload_questions(request):
#     if not request.user.is_staff:
#         return redirect('subjects')

#     if request.method == 'POST':
#         upload_type = request.POST.get('upload_type')
#         subject_id = request.POST.get('subject')

#         # Agar subject_id kelsa, fanni bazadan qidiramiz
#         if subject_id:
#             subject = get_object_or_404(Subject, id=subject_id)
            
#             # Excel yuklash mantiqi
#             if upload_type == 'excel' and request.FILES.get('excel_file'):
#                 # ... (faylni yuklash kodi) ...
#                 messages.success(request, "Excel savollari bazaga qo'shildi!")

#             # Qo'lda qo'shish mantiqi
#             elif upload_type == 'manual':
#                 Question.objects.create(
#                     subject=subject,
#                     text=request.POST.get('text'),
#                     option_a=request.POST.get('option_a'),
#                     option_b=request.POST.get('option_b'),
#                     option_c=request.POST.get('option_c'),
#                     correct_answer=request.POST.get('correct_answer'),
#                     test_type=request.POST.get('test_type')
#                 )
#                 messages.success(request, "Savol muvaffaqiyatli saqlandi!")
        
#         # Fan qo'shish mantiqi (bu yerda subject_id shart emas)
#         elif upload_type == 'add_subject':
#             name = request.POST.get('subject_name')
#             Subject.objects.create(name=name)
#             messages.success(request, "Yangi fan qo'shildi!")

#         return redirect('upload_questions')

#     subjects = Subject.objects.all()
#     questions = Question.objects.all().order_by('-id')[:10]
#     return render(request, 'quiz/upload-questions.html', {'subjects': subjects, 'questions': questions})

# from django.contrib.auth.models import User
# from .models import QuizResult

# def all_students(request):
#     if not request.user.is_staff:
#         return redirect('subjects')
    
#     # Barcha natijalarni o'quvchi va fan bilan birga olamiz
#     results = QuizResult.objects.select_related('user', 'subject').all().order_by('-date_taken')
    
#     return render(request, 'quiz/all_students.html', {'results': results})


# from django.shortcuts import render
# from .models import Subject, QuizResult, QuizSettings
# from django.contrib.auth.models import User

# def subjects_view(request):
#     # 1. Barcha fanlarni bazadan olamiz
#     subjects = Subject.objects.all()
    
#     # 2. Admin uchun barcha o'quvchilar natijalarini bazadan olamiz
#     all_results = QuizResult.objects.select_related('user', 'subject').all().order_by('-date_taken')
    
#     # 3. Quiz sozlamalarini bazadan olamiz (masalan, vaqt yoki sarlavha)
#     # Agarda bazada sozlama bo'lmasa, xato bermasligi uchun .first() ishlatamiz
#     settings = QuizSettings.objects.first()

#     context = {
#         'subjects': subjects,
#         'all_results': all_results,
#         'settings': settings,
#     }
    
#     return render(request, 'quiz/subjects.html', context)

# def subject_list(request):
#     subjects = Subject.objects.all()
#     # first() ishlatish va settings mavjudligini tekshirish
#     settings = QuizSettings.objects.first()
    
#     # Agar sozlama hali yaratilmagan bo'lsa, xato bermasligi uchun
#     if not settings:
#         settings = {'is_bsb_active': False, 'is_chsb_active': False}
        
#     return render(request, 'quiz/subjects.html', {
#         'subjects': subjects,
#         'settings': settings,
#     })
# import pandas as pd
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .models import Subject, Question, QuizSettings

# def admin_dashboard(request):
#     subjects = Subject.objects.all()
#     # Oxirgi qo'shilgan 10 ta savolni jadvalda ko'rsatish
#     questions = Question.objects.all().order_by('-created_at')[:10]

#     if request.method == 'POST':
#         upload_type = request.POST.get('upload_type')

#         # 1. Yangi fan qo'shish
#         if upload_type == 'add_subject':
#             name = request.POST.get('subject_name')
#             desc = request.POST.get('description')
#             Subject.objects.get_or_create(name=name, defaults={'description': desc})
#             messages.success(request, f"{name} fani muvaffaqiyatli qo'shildi!")

#         # 2. Excel orqali ommaviy yuklash (Cheksiz savollar uchun)
#         elif upload_type == 'excel':
#             subject_id = request.POST.get('subject')
#             excel_file = request.FILES.get('excel_file')
            
#             try:
#                 df = pd.read_excel(excel_file)
#                 subject = Subject.objects.get(id=subject_id)
                
#                 for index, row in df.iterrows():
#                     Question.objects.get_or_create(
#                         subject=subject,
#                         text=row['savol'],
#                         defaults={
#                             'option_a': row['a'],
#                             'option_b': row['b'],
#                             'option_c': row['c'],
#                             'correct_answer': str(row['javob']).lower(),
#                             'test_type': request.POST.get('test_type_excel', 'BSB')
#                         }
#                     )
#                 messages.success(request, f"Excel'dagi {len(df)} ta savol bazaga yuklandi!")
#             except Exception as e:
#                 messages.error(request, f"Xatolik yuz berdi: {e}")

#         # 3. Yakka tartibda qo'shish
#         elif upload_type == 'manual':
#             subject_id = request.POST.get('subject')
#             Question.objects.create(
#                 subject_id=subject_id,
#                 text=request.POST.get('text'),
#                 option_a=request.POST.get('option_a'),
#                 option_b=request.POST.get('option_b'),
#                 option_c=request.POST.get('option_c'),
#                 correct_answer=request.POST.get('correct_answer'),
#                 test_type=request.POST.get('test_type')
#             )
#             messages.success(request, "Yangi savol muvaffaqiyatli saqlandi!")

#         return redirect('admin_dashboard')

#     return render(request, 'quiz/admin_dashboard.html', {
#         'subjects': subjects,
#         'questions': questions
#     })
# from django.contrib.auth import logout
# from django.shortcuts import redirect

# def logout_view(request):
#     logout(request)
#     return redirect('login') # yoki 'subjects'
# from django.shortcuts import render
# from .models import Subject, Result # Modellaringiz nomi har xil bo'lishi mumkin

# def home(request):
#     subjects = Subject.objects.all()
#     completed_tests = []

#     if request.user.is_authenticated:
#         # Foydalanuvchi topshirgan barcha natijalarni olamiz
#         # 'subject_id' va 'test_type' (BSB/CHSB) ustunlari bor deb hisoblaymiz
#         user_results = Result.objects.filter(user=request.user)
        
#         for res in user_results:
#             # Har bir natijani "ID_TUR" ko'rinishida saqlaymiz (masalan: "1_BSB")
#             completed_tests.append(f"{res.subject.id}_{res.test_type}")

#     context = {
#         'subjects': subjects,
#         'completed_tests': completed_tests, # Mana shu ro'yxat tugmalarni o'chiradi
#     }
#     return render(request, 'your_template.html', context)

# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from .models import Subject, Question, QuizResult, QuizSettings
# from django.db.models import Avg, Sum

# @login_required
# def test_process(request, subject_id, test_type):
#     # Fan va test turiga qarab savollarni olish
#     subject = get_object_or_404(Subject, id=subject_id)
#     questions = Question.objects.filter(subject=subject, test_type=test_type)

#     if request.method == 'POST':
#         correct_count = 0
#         total_questions = questions.count()

#         for question in questions:
#             # Foydalanuvchi tanlagan variant (a, b yoki c)
#             selected_option = request.POST.get(f'question_{question.id}')
            
#             # Modeldagi 'correct_answer' bilan solishtirish
#             if selected_option == question.correct_answer:
#                 correct_count += 1

#         # Natijalarni hisoblash
#         wrong_count = total_questions - correct_count
#         percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
        
#         # Sizning QuizResult modelingizga moslab saqlash
#         result = QuizResult.objects.create(
#             user=request.user,
#             subject=subject,
#             test_type=test_type,
#             total_questions=total_questions,
#             correct_count=correct_count,
#             wrong_count=wrong_count,
#             score_percentage=round(percentage, 1)
#         )

#         return redirect('result_summary', result_id=result.id)

#     return render(request, 'quiz/test_process.html', {
#         'subject': subject,
#         'questions': questions,
#         'test_type': test_type
#     })

# @login_required
# def result_summary(request, result_id):
#     # Natijani bazadan olish
#     result = get_object_or_404(QuizResult, id=result_id, user=request.user)
    
#     # 60% dan past ball uchun mantiq (Template-dagi JS uchun ham kerak bo'ladi)
#     is_passed = result.score_percentage >= 60

#     return render(request, 'quiz/result_summary.html', {
#         'result': result,
#         'is_passed': is_passed
#     })

# @login_required
# def dashboard(request):
#     # Foydalanuvchining barcha natijalari
#     user_results = QuizResult.objects.filter(user=request.user)
    
#     # Image_9fc7b0 dagi kabi umumiy statistika
#     total_tests = user_results.count()
#     total_correct = user_results.aggregate(Sum('correct_count'))['correct_count__sum'] or 0
    
#     # O'rtacha o'zlashtirish
#     avg_score = user_results.aggregate(Avg('score_percentage'))['score_percentage__avg'] or 0

#     return render(request, 'quiz/dashboard.html', {
#         'total_tests': total_tests,
#         'total_correct': total_correct,
#         'avg_score': round(avg_score, 1),
#         'results': user_results
#     })

# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from django.db.models import Sum, Avg
# from .models import Subject, Question, QuizResult, QuizSettings

# # 1. Test jarayoni (Savollarni chiqarish va javoblarni tekshirish)
# @login_required
# def test_process(request, subject_id, test_type):
#     subject = get_object_or_404(Subject, id=subject_id)
#     # Savollarni fan va test turi (BSB yoki CHSB) bo'yicha filterlash
#     questions = Question.objects.filter(subject=subject, test_type=test_type)

#     if request.method == 'POST':
#         correct_count = 0
#         total_questions = questions.count()

#         for question in questions:
#             # Formadan kelgan javobni olish
#             selected_option = request.POST.get(f'question_{question.id}')
            
#             # To'g'ri javobni models.py dagi 'correct_answer' bilan solishtirish
#             if selected_option == question.correct_answer:
#                 correct_count += 1

#         # Natijalarni hisoblash
#         wrong_count = total_questions - correct_count
#         percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
        
#         # 'QuizResult' modeliga saqlash
#         result = QuizResult.objects.create(
#             user=request.user,
#             subject=subject,
#             test_type=test_type,
#             total_questions=total_questions,
#             correct_count=correct_count,
#             wrong_count=wrong_count,
#             score_percentage=round(percentage, 1)
#         )

#         return redirect('result_summary', result_id=result.id)

#     return render(request, 'quiz/test_process.html', {
#         'subject': subject,
#         'questions': questions,
#         'test_type': test_type
#     })

# # 2. Natijalar xulosasi
# @login_required
# def result_summary(request, result_id):
#     result = get_object_or_404(QuizResult, id=result_id, user=request.user)
    
#     # 60% dan yuqori ball o'tish ko'rsatkichi
#     is_passed = result.score_percentage >= 60

#     return render(request, 'quiz/result_summary.html', {
#         'result': result,
#         'is_passed': is_passed
#     })

# # 3. Dashboard (Umumiy statistika)
# @login_required
# def dashboard(request):
#     results = QuizResult.objects.filter(user=request.user).order_by('-date_taken')
    
#     # Statistikani hisoblash
#     total_tests = results.count()
#     total_correct = results.aggregate(Sum('correct_count'))['correct_count__sum'] or 0
#     avg_score = results.aggregate(Avg('score_percentage'))['score_percentage__avg'] or 0

#     return render(request, 'quiz/dashboard.html', {
#         'results': results,
#         'total_tests': total_tests,
#         'total_correct': total_correct,
#         'avg_score': round(avg_score, 1)
#     })

# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from django.db.models import Sum, Avg
# from .models import Subject, Question, QuizResult, QuizSettings # QuizResult ishlatilishi shart

# @login_required
# def test_process(request, subject_id, test_type):
#     subject = get_object_or_404(Subject, id=subject_id)
#     questions = Question.objects.filter(subject=subject, test_type=test_type)

#     if request.method == 'POST':
#         correct_count = 0
#         total_questions = questions.count()

#         for question in questions:
#             selected_option = request.POST.get(f'question_{question.id}')
#             # Models.py dagi 'correct_answer' bilan solishtirish
#             if selected_option == question.correct_answer:
#                 correct_count += 1

#         wrong_count = total_questions - correct_count
#         score_percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
        
#         # Natijani QuizResult modelida saqlash
#         result = QuizResult.objects.create(
#             user=request.user,
#             subject=subject,
#             test_type=test_type,
#             total_questions=total_questions,
#             correct_count=correct_count,
#             wrong_count=wrong_count,
#             score_percentage=round(score_percentage, 1)
#         )
#         return redirect('result_summary', result_id=result.id)

#     return render(request, 'quiz/test_process.html', {
#         'subject': subject,
#         'questions': questions,
#         'test_type': test_type
#     })

# @login_required
# def result_summary(request, result_id):
#     result = get_object_or_404(QuizResult, id=result_id, user=request.user)
#     # 60% o'tish chegarasi
#     is_passed = result.score_percentage >= 60
#     return render(request, 'quiz/result_summary.html', {
#         'result': result,
#         'is_passed': is_passed
#     })

# @login_required
# def dashboard(request):
#     results = QuizResult.objects.filter(user=request.user).order_by('-date_taken')
#     total_tests = results.count()
#     total_correct = results.aggregate(Sum('correct_count'))['correct_count__sum'] or 0
#     avg_score = results.aggregate(Avg('score_percentage'))['score_percentage__avg'] or 0

#     return render(request, 'quiz/dashboard.html', {
#         'results': results,
#         'total_tests': total_tests,
#         'total_correct': total_correct,
#         'avg_score': round(avg_score, 1)
#     })










import random
import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Sum, Avg

# Modellarni va formalarni import qilish
from .models import Subject, Question, QuizResult, QuizSettings
from .forms import UzbRegisterForm

# --- 1. AUTHENTICATION ---
def register(request):
    if request.method == 'POST':
        form = UzbRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('subject_list')
    else:
        form = UzbRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


# --- 2. ASOSIY SAHIFA (FANLAR) ---
@login_required
def subject_list(request):
    subjects = Subject.objects.all()
    settings = QuizSettings.objects.first()
    
    if not settings:
        # Agar sozlamalar yaratilmagan bo'lsa, default qiymat
        settings = {'is_bsb_active': True, 'is_chsb_active': True}
    
    for subject in subjects:
        # Foydalanuvchi bu fandan oldin test topshirganmi yoki yo'qligini tekshirish
        subject.user_has_bsb = QuizResult.objects.filter(
            user=request.user, subject=subject, test_type='BSB'
        ).exists()
        subject.user_has_chsb = QuizResult.objects.filter(
            user=request.user, subject=subject, test_type='CHSB'
        ).exists()

    return render(request, 'quiz/subjects.html', {
        'subjects': subjects,
        'settings': settings
    })


# --- 3. TEST JARAYONI VA NATIJANI TOPSHIRISH ---
@login_required
def test_process(request, subject_id, test_type='BSB'):
    subject = get_object_or_404(Subject, id=subject_id)
    
    # POST - Test yakunlanganda natijani hisoblash
    if request.method == 'POST':
        questions = Question.objects.filter(subject=subject, test_type=test_type)
        correct_count = 0
        total_questions = questions.count()

        for question in questions:
            # HTML formadagi radio button nomi: name="q{{ question.id }}"
            user_answer = request.POST.get(f'q{question.id}')
            if user_answer and user_answer.strip().lower() == question.correct_answer.strip().lower():
                correct_count += 1

        wrong_count = total_questions - correct_count
        percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
        
        # Natijani bazaga saqlash
        result = QuizResult.objects.create(
            user=request.user,
            subject=subject,
            test_type=test_type,
            total_questions=total_questions,
            correct_count=correct_count,
            wrong_count=wrong_count,
            score_percentage=round(percentage, 1)
        )
        return redirect('result_summary', result_id=result.id)

    # GET - Savollarni ko'rsatish
    questions_list = list(Question.objects.filter(subject=subject, test_type=test_type))
    
    if not questions_list:
        messages.warning(request, f"{subject.name} fanidan {test_type} savollari hali yuklanmagan.")
        return redirect('subject_list')

    random.shuffle(questions_list) # Savollarni aralashtirish
    
    return render(request, 'quiz/test_process.html', {
        'subject': subject,
        'questions': questions_list,
        'test_type': test_type
    })


# --- 4. ADMIN: SAVOLLARNI BOSHQARISH ---
@login_required
def upload_questions(request):
    if not request.user.is_staff:
        messages.error(request, "Bu sahifa faqat adminlar uchun!")
        return redirect('subject_list')

    if request.method == "POST":
        upload_type = request.POST.get('upload_type')

        # Fan qo'shish
        if upload_type == 'add_subject':
            name = request.POST.get('subject_name')
            if name:
                Subject.objects.create(name=name, description=request.POST.get('description', ''))
                messages.success(request, f"'{name}' fani qo'shildi!")

        # Manual savol qo'shish
        elif upload_type == 'manual':
            Question.objects.create(
                subject_id=request.POST.get('subject'),
                text=request.POST.get('text'),
                option_a=request.POST.get('option_a'),
                option_b=request.POST.get('option_b'),
                option_c=request.POST.get('option_c'),
                correct_answer=request.POST.get('correct_answer'),
                test_type=request.POST.get('test_type')
            )
            messages.success(request, "Yangi savol bazaga qo'shildi!")

        # Excel orqali yuklash
        elif upload_type == 'excel' and request.FILES.get('excel_file'):
            subject_id = request.POST.get('subject')
            file = request.FILES['excel_file']
            try:
                df = pd.read_excel(file)
                count = 0
                for _, row in df.iterrows():
                    Question.objects.create(
                        subject_id=subject_id,
                        text=row.iloc[0],
                        option_a=row.iloc[1],
                        option_b=row.iloc[2],
                        option_c=row.iloc[3],
                        correct_answer=str(row.iloc[4]).strip().lower(),
                        test_type=row.iloc[5] if len(row) > 5 else 'BSB'
                    )
                    count += 1
                messages.success(request, f"Excel'dan {count} ta savol yuklandi!")
            except Exception as e:
                messages.error(request, f"Excel yuklashda xatolik: {e}")

        return redirect('upload_questions')

    context = {
        'subjects': Subject.objects.all().order_by('-id'),
        'questions': Question.objects.select_related('subject').all().order_by('-id')[:10]
    }
    return render(request, 'quiz/upload_questions.html', context)


# --- 5. STATISTIKA VA NATIJALAR ---
@login_required
def result_summary(request, result_id):
    result = get_object_or_404(QuizResult, id=result_id, user=request.user)
    return render(request, 'quiz/result_summary.html', {'result': result})

@login_required
def dashboard(request):
    results = QuizResult.objects.filter(user=request.user).order_by('-date_taken')
    total_tests = results.count()
    total_correct = results.aggregate(Sum('correct_count'))['correct_count__sum'] or 0
    avg_score = results.aggregate(Avg('score_percentage'))['score_percentage__avg'] or 0

    return render(request, 'quiz/dashboard.html', {
        'results': results,
        'total_tests': total_tests,
        'total_correct': total_correct,
        'avg_score': round(avg_score, 1)
    })

@login_required
def all_students(request):
    if not request.user.is_staff:
        return redirect('subject_list')
    results = QuizResult.objects.select_related('user', 'subject').all().order_by('-date_taken')
    return render(request, 'quiz/all_students.html', {'results': results})


@login_required
def submit_quiz(request, subject_id):
    # Bu funksiya shunchaki test_process funksiyasiga yo'naltirib yuboradi
    # Test turi default holatda 'BSB' deb olinadi
    return test_process(request, subject_id, test_type='BSB')

import pandas as pd
from django.contrib import messages
from .models import Subject, Question

def upload_excel_view(request):
    if request.method == "POST" and request.POST.get('upload_type') == 'excel':
        subject_id = request.POST.get('subject')
        test_type = request.POST.get('test_type')
        excel_file = request.FILES.get('excel_file')

        try:
            # Excelni o'qiymiz
            df = pd.read_excel(excel_file)
            subject = Subject.objects.get(id=subject_id)

            for index, row in df.iterrows():
                # Xatolikni oldini olish: get_or_create yoki update_or_create ishlatamiz
                Question.objects.update_or_create(
                    subject=subject,
                    text=str(row['Savol matni']).strip(), # Bir xil savol bormi tekshiradi
                    defaults={
                        'option_a': row['A javob'],
                        'option_b': row['B javob'],
                        'option_c': row['C javob'],
                        'correct_answer': str(row["Yo'g'ri javob"]).lower(),
                        'test_type': test_type
                    }
                )
            
            messages.success(request, "Exceldagi barcha savollar muvaffaqiyatli saqlandi (nusxalar yangilandi)!")
            
        except Exception as e:
            messages.error(request, f"Excel yuklashda xatolik: {e}")
            
    # Qolgan qismi...