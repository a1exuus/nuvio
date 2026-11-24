from django.db import models
from django.db.models import UniqueConstraint
from phonenumber_field.modelfields import PhoneNumberField
from tinymce.models import HTMLField


class Student(models.Model):
    name = models.CharField('ФИО', max_length=120)
    birth_date = models.DateField('Дата рождения')
    email = models.EmailField('Электронная почта', unique=True)
    phone_number = PhoneNumberField('Номер телефона', unique=True)
    description = HTMLField(
        'Описание ученика и его успехов',
        blank=True
    )

    groups = models.ManyToManyField(
        'Group',
        verbose_name='Группы',
        related_name='students',
        blank=True
    )

    modules = models.ManyToManyField(
        'Module',
        verbose_name='Модули',
        related_name='students',
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'


class Teacher(models.Model):
    name = models.CharField('ФИО', max_length=120)
    email = models.EmailField('Электронная почта', unique=True)
    phone_number = PhoneNumberField('Номер телефона', unique=True)
    description = HTMLField(
        'Описание преподавателя и его опыта',
        blank=True
    )

    groups = models.ManyToManyField(
        'Group',
        verbose_name='Группы',
        related_name='teachers',
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'


class Group(models.Model):
    name = models.CharField('Название группы', max_length=120)
    description = HTMLField('Описание группы', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Module(models.Model):
    name = models.CharField('Название модуля', max_length=120)
    description = HTMLField('Описание модуля', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'


class Step(models.Model):
    title = models.CharField('Название шага', max_length=120)
    description = HTMLField('Наполнение шага', blank=True)

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        verbose_name='Модуль',
        related_name='steps'
    )

    order = models.PositiveIntegerField('Порядок шага', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Шаг'
        verbose_name_plural = 'Шаги'
        ordering = ['order']


class StepProgress(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name='Ученик',
        related_name='step_progress'
    )

    step = models.ForeignKey(
        Step,
        on_delete=models.CASCADE,
        verbose_name='Шаг',
        related_name='progress'
    )

    is_completed = models.BooleanField('Завершен', default=False)

    completed_at = models.DateTimeField(
        'Дата завершения',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.student} — {self.step}'

    class Meta:
        verbose_name = 'Прогресс ученика'
        verbose_name_plural = 'Прогресс учеников'
        constraints = [
            UniqueConstraint(
                fields=['student', 'step'],
                name='unique_student_step_progress'
            )
        ]
