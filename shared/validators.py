from rest_framework.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

def validate_title(value):
    if not value:
            raise ValidationError(
                {
                    'success': False,
                    'message': "Guruh uchun Task yaratildi"
                }
            )
    if value.isnumeric():
        raise ValidationError(
            {
                'success': False,
                    'message': "Task faqat raqamlardan iborat bo'lmasligi kerak"
            }
        )
    return value

def validate_deadline(value):
    if value < timezone.now():
        raise ValidationError(
            {
                'success': False,
                'message': "Deadline vaqti o'tgan bo'lmasligi kerak"
            }
        )
    if value > timedelta(days=365):
        raise ValidationError(
            {
                'success': False,
                'message': "Deadline muddati 1 yildam kam bo'lishi kerak"
            }
        )
    return value