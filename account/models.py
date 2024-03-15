from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

# Todo: Skills should be added to user

class User(AbstractUser):

    class Gender(models.TextChoices):
        FEMALE = 'F', 'Female'
        MALE = 'M', 'Male'
        OTHER = 'O', 'Other'

    is_author = models.BooleanField(default=False)
    cellphone_numer = models.CharField(max_length=30, unique=True, null=True, blank=True)
    email_active_code = models.CharField(max_length=150, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=Gender.choices, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    vip_due_date = models.DateTimeField(default=timezone.now)
    # programming_skill = models.ManyToManyField('ProgrammingSkills', null=True, blank=True)
    # language_skill = models.ManyToManyField('LanguageSkill', null=True, blank=True)

    def is_vip_due_date(self):
        if self.vip_due_date > timezone.now():
            return True
        else:
            return False

    # instead of showing False/True in admin panel, Tick or Cross shapes will be displayed
    is_vip_due_date.boolean = True
    is_vip_due_date.short_description = 'VIP'


# class ProgrammingSkill(models.Model):
#     language = models.CharField(max_length=30, unique=True, null=True, blank=True)
#     rate_field = models.DecimalField(max_digits=3, validators=PERCENTAGE_VALIDATOR)
#
#
# class languageSkill(models.Model):
#     language = models.CharField(max_length=30, unique=True, null=True, blank=True)
#     rate_field = models.DecimalField(max_digits=3, validators=PERCENTAGE_VALIDATOR)
