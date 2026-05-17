# # from django.db import models
# # from django.contrib.auth.models import User

# # class Subject(models.Model):
# #     name = models.CharField(max_length=100, verbose_name="Fan nomi")
# #     description = models.TextField(blank=True, null=True, verbose_name="Fan haqida ma'lumot")

# #     def __str__(self):
# #         return self.name

# #     class Meta:
# #         verbose_name = "Fan "
# #         verbose_name_plural = "Fanlar"

# # class Question(models.Model):
# #     TEST_TYPES = (
# #         ('BSB', 'BSB (Baho nazorat)'),
# #         ('CHSB', 'CHSB (Choraklik nazorat)'),
# #     )

# #     subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions', verbose_name="Fan")
# #     text = models.TextField(verbose_name="Savol matni")
    
# #     option_a = models.CharField(max_length=255, verbose_name="A varianti")
# #     option_b = models.CharField(max_length=255, verbose_name="B varianti")
# #     option_c = models.CharField(max_length=255, verbose_name="C varianti")
    
# #     correct_answer = models.CharField(
# #         max_length=1, 
# #         choices=(('a', 'A'), ('b', 'B'), ('c', 'C')), 
# #         verbose_name="To'g'ri javob"
# #     )
    
# #     test_type = models.CharField(max_length=5, choices=TEST_TYPES, default='BSB', verbose_name="Test turi")
# #     created_at = models.DateTimeField(auto_now_add=True)

# #     def __str__(self):
# #         return f"{self.subject.name} - {self.text[:50]}..."

# #     class Meta:
# #         verbose_name = "Savol "
# #         verbose_name_plural = "Savollar"
# #         unique_together = ('subject', 'text') # Bir xil savol takrorlanmasligi uchun

# # class QuizResult(models.Model):
# #     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results', verbose_name="O'quvchi")
# #     subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Fan")
# #     test_type = models.CharField(max_length=10, verbose_name="Test turi")
# #     total_questions = models.IntegerField(verbose_name="Jami savollar")
# #     correct_count = models.IntegerField(verbose_name="To'g'ri javoblar")
# #     wrong_count = models.IntegerField(verbose_name="Xato javoblar")
# #     score_percentage = models.FloatField(verbose_name="Natija (%)")
# #     date_taken = models.DateTimeField(auto_now_add=True, verbose_name="Topshirilgan vaqt")

# #     class Meta:
# #         verbose_name = "Natija "
# #         verbose_name_plural = "Natijalar"
# #         ordering = ['-date_taken']

# # class QuizSettings(models.Model):
# #     name = models.CharField(max_length=50, default="Test Sozlamalari")
# #     is_bsb_active = models.BooleanField(default=False, verbose_name="BSB testlarini yoqish")
# #     is_chsb_active = models.BooleanField(default=False, verbose_name="CHSB testlarini yoqish")

# #     def __str__(self):
# #         return self.name
    


# # from django.db import models
# # from django.contrib.auth.models import User

# # class Subject(models.Model):
# #     name = models.CharField(max_length=100)

# #     def __str__(self):
# #         return self.name

# # class Question(models.Model):
# #     subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions')
# #     text = models.TextField()
# #     option_a = models.CharField(max_length=255)
# #     option_b = models.CharField(max_length=255)
# #     option_c = models.CharField(max_length=255)
# #     correct_answer = models.CharField(max_length=1) # a, b, c
# #     test_type = models.CharField(max_length=10, choices=[('BSB', 'BSB'), ('CHSB', 'CHSB')], default='BSB')

# # class QuizResult(models.Model):
# #     user = models.ForeignKey(User, on_delete=models.CASCADE)
# #     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
# #     test_type = models.CharField(max_length=10)
# #     score_percentage = models.FloatField()
# #     date_taken = models.DateTimeField(auto_now_add=True)
# #     correct_count = models.IntegerField(default=0)
# #     wrong_count = models.IntegerField(default=0)

# # class QuizSettings(models.Model):
# #     is_bsb_active = models.BooleanField(default=False, verbose_name="BSB yoqilgan")
# #     is_chsb_active = models.BooleanField(default=False, verbose_name="CHSB yoqilgan")

# #     class Meta:
# #         verbose_name = "Test Sozlamasi"
# #         verbose_name_plural = "Test Sozlamalari"


# # from django.db import models

# # class Subject(models.Model):
# #     name = models.CharField(max_length=100)
# #     description = models.TextField(null=True, blank=True)

# #     def __clstr__(self):
# #         return self.name

# # class Question(models.Model):
# #     subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions')
# #     text = models.TextField()
# #     option_a = models.CharField(max_length=200)
# #     option_b = models.CharField(max_length=200)
# #     option_c = models.CharField(max_length=200)
# #     correct_answer = models.CharField(max_length=1) # a, b, c
# #     test_type = models.CharField(max_length=10, default='BSB') # BSB yoki CHSB

# #     def __str__(self):
# #         return f"{self.subject.name} - {self.text[:20]}"


# # from django.db import models
# # from django.contrib.auth.models import User

# # # 1. Avval Subject (Chunki boshqalar bunga bog'lanadi)
# # class Subject(models.Model):
# #     name = models.CharField(max_length=100)
# #     description = models.TextField(null=True, blank=True)

# #     def __str__(self):
# #         return self.name

# # # 2. Keyin Question
# # class Question(models.Model):
# #     subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions')
# #     text = models.TextField()
# #     option_a = models.CharField(max_length=200)
# #     option_b = models.CharField(max_length=200)
# #     option_c = models.CharField(max_length=200)
# #     correct_answer = models.CharField(max_length=1)
# #     test_type = models.CharField(max_length=10, default='BSB')

# # # 3. Va QuizResult
# # class QuizResult(models.Model):
# #     user = models.ForeignKey(User, on_delete=models.CASCADE)
# #     subject = models.ForeignKey(Subject, on_delete=models.CASCADE) # SHU YERDA XATO BERAYOTGAN EDI
# #     test_type = models.CharField(max_length=10)
# #     score_percentage = models.FloatField()
# #     date_taken = models.DateTimeField(auto_now_add=True)
# #     correct_count = models.IntegerField(default=0)
# #     wrong_count = models.IntegerField(default=0)

# # class Subject(models.Model):
# #     name = models.CharField(max_length=100)
# #     # ... boshqa maydonlar ...

# #     def has_bsb_questions(self):
# #         # Shu fanga tegishli BSB turidagi savollar bormi?
# #         return self.question_set.filter(test_type='BSB').exists()

# #     def has_chsb_questions(self):
# #         # Shu fanga tegishli CHSB turidagi savollar bormi?
# #         return self.question_set.filter(test_type='CHSB').exists()
    
# # def has_bsb_questions(self):
# #     return self.question_set.filter(test_type='BSB').exists()

# # def has_chsb_questions(self):
# #     return self.question_set.filter(test_type='CHSB').exists()




# # class Question(models.Model):
# #     # 'Subject' so'zini qo'shtirnoq ichida yozing
# #     subject = models.ForeignKey('Subject', on_delete=models.CASCADE) 
# #     # ... boshqa qismlar ...

# # class QuizResult(models.Model):
# #     # Bu yerda ham qo'shtirnoq ishlating
# #     subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
# #     # ... boshqa qismlar ...



# from django.db import models
# from django.contrib.auth.models import User

# # 1. Subject (Fanlar) modeli
# class Subject(models.Model):
#     name = models.CharField(max_length=100, verbose_name="Fan nomi")
#     description = models.TextField(blank=True, null=True, verbose_name="Fan haqida ma'lumot")

#     def __str__(self):
#         return self.name

#     # HTML sahifada tugmalar chiqishini tekshirish uchun mantiq
#     def has_bsb_questions(self):
#         return self.questions.filter(test_type='BSB').exists()

#     def has_chsb_questions(self):
#         return self.questions.filter(test_type='CHSB').exists()

#     class Meta:
#         verbose_name = "Fan"
#         verbose_name_plural = "Fanlar"


# # 2. Question (Savollar) modeli
# class Question(models.Model):
#     TEST_TYPES = (
#         ('BSB', 'BSB (Baho nazorat)'),
#         ('CHSB', 'CHSB (Choraklik nazorat)'),
#     )

#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions', verbose_name="Fan")
#     text = models.TextField(verbose_name="Savol matni")
    
#     option_a = models.CharField(max_length=255, verbose_name="A varianti")
#     option_b = models.CharField(max_length=255, verbose_name="B varianti")
#     option_c = models.CharField(max_length=255, verbose_name="C varianti")
    
#     CHOICES = (('a', 'A'), ('b', 'B'), ('c', 'C'))
#     correct_answer = models.CharField(max_length=1, choices=CHOICES, verbose_name="To'g'ri javob")
    
#     test_type = models.CharField(max_length=10, choices=TEST_TYPES, default='BSB', verbose_name="Test turi")
#     created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

#     def __str__(self):
#         return f"{self.subject.name} - {self.text[:50]}..."

#     class Meta:
#         verbose_name = "Savol"
#         verbose_name_plural = "Savollar"
#         unique_together = ('subject', 'text')


# # 3. QuizResult (Natijalar) modeli
# class QuizResult(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results', verbose_name="O'quvchi")
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Fan")
#     test_type = models.CharField(max_length=10, verbose_name="Test turi")
    
#     # Views.py'da ishlatilgan barcha maydonlar shu yerda
#     total_questions = models.IntegerField(default=0, verbose_name="Jami savollar")
#     correct_count = models.IntegerField(default=0, verbose_name="To'g'ri javoblar")
#     wrong_count = models.IntegerField(default=0, verbose_name="Xato javoblar")
#     score_percentage = models.FloatField(default=0.0, verbose_name="Natija (%)")
#     date_taken = models.DateTimeField(auto_now_add=True, verbose_name="Topshirilgan vaqt")

#     def __str__(self):
#         return f"{self.user.username} - {self.subject.name} ({self.test_type})"

#     class Meta:
#         verbose_name = "Natija"
#         verbose_name_plural = "Natijalar"
#         ordering = ['-date_taken']


# # 4. QuizSettings (Sozlamalar) modeli
# class QuizSettings(models.Model):
#     name = models.CharField(max_length=50, default="Test Sozlamalari", verbose_name="Sozlama nomi")
#     is_bsb_active = models.BooleanField(default=False, verbose_name="BSB yoqilgan")
#     is_chsb_active = models.BooleanField(default=False, verbose_name="CHSB yoqilgan")

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = "Test Sozlamasi"
#         verbose_name_plural = "Test Sozlamalari"

# class Question(models.Model):
#     text = models.TextField()
#     option_a = models.CharField(max_length=200)
#     option_b = models.CharField(max_length=200)
#     option_c = models.CharField(max_length=200)
#     # MANA SHU YERDA TO'G'RI JAVOB NOMI BOR:
#     correct_answer = models.CharField(max_length=1) # Balki nomi 'correct_answer'dir?

# # quiz/models.py

# from django.db import models

# class Subject(models.Model):
#     name = models.CharField(max_length=255)
#     # boshqa maydonlar...

# class Question(models.Model):
#     # MUHIM: Mana shu yerda subject bog'liqligi bo'lishi shart!
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions')
#     text = models.TextField()
#     option_a = models.CharField(max_length=255)
#     option_b = models.CharField(max_length=255)
#     option_c = models.CharField(max_length=255)
#     # Agar sizda test_type ham filterda bo'lsa, uni ham qo'shing
#     test_type = models.CharField(max_length=50, default='BSB') 
#     correct_answer = models.CharField(max_length=1)

#     def __str__(self):
#         return self.text
    
# # quiz/models.py ichida

# class QuizResult(models.Model):
#     # 'Subject' deb qo'shtirnoq ichida yozish model tartibi buzilgan bo'lsa ham yordam beradi
#     subject = models.ForeignKey('Subject', on_delete=models.CASCADE) 
#     # ... boshqa maydonlar

# # TO'G'RI TARTIB:

# class Subject(models.Model):
#     name = models.CharField(max_length=200)
#     # ...

# class Question(models.Model):
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     # ...

# class QuizResult(models.Model):
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     # ...

# from django.db import models
# from django.contrib.auth.models import User

# class QuizResult(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
#     test_type = models.CharField(max_length=10)
#     score_percentage = models.FloatField()
#     correct_count = models.IntegerField()
#     wrong_count = models.IntegerField()
#     date_taken = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.subject.name}"
























































from django.db import models
from django.contrib.auth.models import User

# 1. Subject (Fanlar) modeli
class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Fan nomi")
    description = models.TextField(blank=True, null=True, verbose_name="Fan haqida ma'lumot")

    def __str__(self):
        return self.name

    # HTML sahifada tugmalar chiqishini tekshirish uchun mantiq
    def has_bsb_questions(self):
        return self.questions.filter(test_type='BSB').exists()

    def has_chsb_questions(self):
        return self.questions.filter(test_type='CHSB').exists()

    class Meta:
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"


# 2. Question (Savollar) modeli
class Question(models.Model):
    TEST_TYPES = (
        ('BSB', 'BSB (Baho nazorat)'),
        ('CHSB', 'CHSB (Choraklik nazorat)'),
    )
    CHOICES = (('a', 'A'), ('b', 'B'), ('c', 'C'))

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions', verbose_name="Fan")
    text = models.TextField(verbose_name="Savol matni")
    
    option_a = models.CharField(max_length=255, verbose_name="A varianti")
    option_b = models.CharField(max_length=255, verbose_name="B varianti")
    option_c = models.CharField(max_length=255, verbose_name="C varianti")
    
    correct_answer = models.CharField(max_length=1, choices=CHOICES, verbose_name="To'g'ri javob")
    test_type = models.CharField(max_length=10, choices=TEST_TYPES, default='BSB', verbose_name="Test turi")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.subject.name} - {self.text[:50]}..."

    class Meta:
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"
        unique_together = ('subject', 'text')


# 3. QuizResult (Natijalar) modeli
class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results', verbose_name="O'quvchi")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Fan")
    test_type = models.CharField(max_length=10, verbose_name="Test turi")
    
    total_questions = models.IntegerField(default=0, verbose_name="Jami savollar")
    correct_count = models.IntegerField(default=0, verbose_name="To'g'ri javoblar")
    wrong_count = models.IntegerField(default=0, verbose_name="Xato javoblar")
    score_percentage = models.FloatField(default=0.0, verbose_name="Natija (%)")
    date_taken = models.DateTimeField(auto_now_add=True, verbose_name="Topshirilgan vaqt")

    def __str__(self):
        return f"{self.user.username} - {self.subject.name} ({self.test_type})"

    class Meta:
        verbose_name = "Natija"
        verbose_name_plural = "Natijalar"
        ordering = ['-date_taken']


# 4. QuizSettings (Sozlamalar) modeli
class QuizSettings(models.Model):
    name = models.CharField(max_length=50, default="Test Sozlamalari", verbose_name="Sozlama nomi")
    is_bsb_active = models.BooleanField(default=False, verbose_name="BSB yoqilgan")
    is_chsb_active = models.BooleanField(default=False, verbose_name="CHSB yoqilgan")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Test Sozlamasi"
        verbose_name_plural = "Test Sozlamalari"