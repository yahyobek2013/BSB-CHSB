from .models import QuizSettings

def quiz_status(request):
    # Eng oxirgi sozlamani olish yoki bo'sh obyekt yaratish
    settings = QuizSettings.objects.last()
    
    if not settings:
        return {
            'is_bsb_active': False,
            'is_chsb_active': False,
            'quiz_settings': None
        }
    
    return {
        'is_bsb_active': settings.is_bsb_active,
        'is_chsb_active': settings.is_chsb_active,
        'quiz_settings': settings
        # 'quiz_settings_name': settings.name  <-- BU QATORNI O'CHIRING (Chunki 'name' yo'q)
    }