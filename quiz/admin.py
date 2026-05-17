# from django.contrib import admin
# from django.urls import path
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .models import Subject, Question, QuizResult, QuizSettings
# import pandas as pd  # Excel bilan ishlash uchun

# @admin.register(Subject)
# class SubjectAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')
#     search_fields = ('name',)

# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     # Eslatma: list_display dagi maydonlar models.py dagi Question klassida bo'lishi shart!
#     # Agar 'test_type' Question modelida bo'lmasa, uni bu yerdan olib tashlaymiz
#     list_display = ('text', 'subject') 
#     list_filter = ('subject',)
#     search_fields = ('text',)
    
#     # Excel import tugmasini admin panelga qo'shish
#     change_list_template = "admin/question_change_list.html"

#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path('import-excel/', self.admin_site.admin_view(self.import_excel), name='excel_import'),
#         ]
#         return custom_urls + urls

#     def import_excel(self, request):
#         if request.method == "POST":
#             excel_file = request.FILES.get('excel_file')
#             subject_id = request.POST.get('subject')
            
#             if not excel_file:
#                 messages.error(request, "Fayl tanlanmadi!")
#                 return redirect("..")

#             if not excel_file.name.endswith(('.xlsx', '.xls')):
#                 messages.error(request, "Faqat Excel fayllarini yuklang!")
#                 return redirect("..")

#             try:
#                 df = pd.read_excel(excel_file)
#                 subject = Subject.objects.get(id=subject_id)
                
#                 questions_created = 0
#                 for _, row in df.iterrows():
#                     # Model maydonlariga mos ravishda create qilish
#                     Question.objects.create(
#                         subject=subject,
#                         text=row['savol_matni'],
#                         option_a=row['variant_a'],
#                         option_b=row['variant_b'],
#                         option_c=row['variant_c'],
#                         option_d=row['variant_d'],
#                         correct_answer=str(row['togri_javob']).lower().strip()
#                     )
#                     questions_created += 1
                
#                 messages.success(request, f"{questions_created} ta savol muvaffaqiyatli qo'shildi!")
#                 return redirect("admin:quiz_question_changelist")
            
#             except Exception as e:
#                 messages.error(request, f"Xatolik yuz berdi: {e}")
#                 return redirect("..")

#         subjects = Subject.objects.all()
#         return render(request, "admin/excel_import.html", {"subjects": subjects})

# @admin.register(QuizResult)
# class QuizResultAdmin(admin.ModelAdmin):
#     # 'student' o'rniga 'user' ishlatildi (Sizning koddagi to'g'irlangan modelga asosan)
#     list_display = ('user', 'subject', 'test_type', 'score_percentage', 'date_taken')
#     list_filter = ('subject', 'test_type', 'date_taken')
#     search_fields = ('user__username', 'subject__name')
#     readonly_fields = ('user', 'subject', 'test_type', 'total_questions', 'correct_count', 'wrong_count', 'score_percentage', 'date_taken')

#     def has_add_permission(self, request):
#         return False

# @admin.register(QuizSettings)
# class QuizSettingsAdmin(admin.ModelAdmin):
#     list_display = ('name', 'is_bsb_active', 'is_chsb_active')
#     list_editable = ('is_bsb_active', 'is_chsb_active')

#     def has_add_permission(self, request):
#         return QuizSettings.objects.count() == 0
    

# from django.contrib import admin
# from .models import Subject, Question, QuizResult, QuizSettings

# # Agar avvalroq ro'yxatdan o'tgan bo'lsa, xatolik bermasligi uchun tekshiruv bilan
# @admin.register(Subject)
# class SubjectAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')
#     search_fields = ('name',)

# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ('text', 'subject', 'test_type', 'correct_answer')
#     list_filter = ('subject', 'test_type')
#     search_fields = ('text',)

# @admin.register(QuizResult)
# class QuizResultAdmin(admin.ModelAdmin):
#     list_display = ('user', 'subject', 'test_type', 'score_percentage', 'correct_count', 'date_taken')
#     readonly_fields = ('user', 'subject', 'test_type', 'score_percentage', 'correct_count', 'wrong_count', 'date_taken')
#     list_filter = ('test_type', 'subject', 'date_taken')

# @admin.register(QuizSettings)
# class QuizSettingsAdmin(admin.ModelAdmin):
#     # Modelda 'name' yo'qligi uchun faqat bor maydonlarni chiqaramiz
#     list_display = ('is_bsb_active', 'is_chsb_active')

#     def has_add_permission(self, request):
#         # Faqat bitta sozlama bo'lishi uchun
#         return not QuizSettings.objects.exists()

# from django.contrib import admin
# from .models import Subject, Question, QuizResult, QuizSettings

# @admin.register(Subject)
# class SubjectAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')
#     search_fields = ('name',)

# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ('text', 'subject', 'test_type', 'correct_answer')
#     list_filter = ('subject', 'test_type')
#     search_fields = ('text',)

# @admin.register(QuizResult)
# class QuizResultAdmin(admin.ModelAdmin):
#     list_display = ('user', 'subject', 'test_type', 'score_percentage', 'correct_count', 'date_taken')
#     readonly_fields = ('user', 'subject', 'test_type', 'score_percentage', 'correct_count', 'wrong_count', 'date_taken')
#     list_filter = ('test_type', 'subject', 'date_taken')

# @admin.register(QuizSettings)
# class QuizSettingsAdmin(admin.ModelAdmin):
#     list_display = ('is_bsb_active', 'is_chsb_active')
#     def has_add_permission(self, request):
#         return not QuizSettings.objects.exists()
    

# from django.contrib import admin
# from .models import Question

# # Avval tekshiramiz, agar ro'yxatdan o'tgan bo'lsa, o'chirib yuboramiz
# if admin.site.is_registered(Question):
#     admin.site.unregister(Question)

# # Endi qaytadan, bitta joyda ro'yxatga olamiz
# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ('id', 'text')

# from django.contrib import admin
# from .models import Subject, Question, QuizResult

# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     # list_display ichida 'text' borligini tekshiring
#     list_display = ('id', 'text', 'subject', 'correct_answer') 

# @admin.register(QuizResult)
# class QuizResultAdmin(admin.ModelAdmin):
#     # Modelda bor bo'lgan ustunlarni yozamiz
#     list_display = ('user', 'subject', 'test_type', 'score_percentage', 'correct_count', 'date_taken')
#     list_filter = ('test_type', 'subject', 'date_taken')
#     readonly_fields = ('user', 'subject', 'test_type', 'score_percentage', 'correct_count', 'wrong_count', 'date_taken')

# from django.contrib import admin
# from .models import Subject, Question, QuizResult

# # AGAR OLDINROQ admin.site.unregister(Question) BO'LSA O'CHIRING

# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ('id', 'text', 'subject', 'correct_answer')

# @admin.register(Subject)
# class SubjectAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')

# @admin.register(QuizResult)
# class QuizResultAdmin(admin.ModelAdmin):
#     list_display = ('user', 'subject', 'score_percentage', 'date_taken')

# # DIQQAT: Faylning oxirida admin.site.register(...) degan yozuvlar bo'lsa, 
# # ularni hammasini o'chirib tashlang! Chunki tepada @admin.register ishlatdik.





from django.contrib import admin
from .models import Subject, Question, QuizResult, QuizSettings

# 1. Subject Admin
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# 2. Question Admin
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    # Siz xohlagan barcha ustunlar birlashtirildi
    list_display = ('id', 'text', 'subject', 'test_type', 'correct_answer')
    list_filter = ('subject', 'test_type')
    search_fields = ('text',)

# 3. QuizResult Admin
@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    # Bu yerda barcha muhim ustunlar jamlangan
    list_display = ('user', 'subject', 'test_type', 'score_percentage', 'correct_count', 'date_taken')
    # Faqat o'qish uchun rejim (xatolik bermasligi uchun modelda borligini tekshiring)
    readonly_fields = ('user', 'subject', 'test_type', 'score_percentage', 'correct_count', 'wrong_count', 'date_taken')
    list_filter = ('test_type', 'subject', 'date_taken')

# 4. QuizSettings Admin
@admin.register(QuizSettings)
class QuizSettingsAdmin(admin.ModelAdmin):
    list_display = ('is_bsb_active', 'is_chsb_active')
    
    def has_add_permission(self, request):
        # Faqat bitta sozlama yaratishga ruxsat berish
        return not QuizSettings.objects.exists()