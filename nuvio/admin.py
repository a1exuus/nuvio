
from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Student,
    Teacher,
    Group,
    Module,
    Step,
    StepProgress,
)


# STUDENTS

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'phone_number',
        'birth_date',
        'groups_count',
        'modules_count',
    )

    list_display_links = ('name',)

    search_fields = (
        'name',
        'email',
        'phone_number',
    )

    list_filter = (
        'birth_date',
        'groups',
        'modules',
    )

    filter_horizontal = (
        'groups',
        'modules',
    )

    readonly_fields = ()

    fieldsets = (
        ('Основная информация', {
            'fields': (
                'name',
                'birth_date',
            )
        }),
        ('Контакты', {
            'fields': (
                'email',
                'phone_number',
            )
        }),
        ('Обучение', {
            'fields': (
                'groups',
                'modules',
            )
        }),
        ('Дополнительно', {
            'fields': ('description',),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Групп')
    def groups_count(self, obj):
        return obj.groups.count()

    @admin.display(description='Модулей')
    def modules_count(self, obj):
        return obj.modules.count()


# TEACHERS

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'phone_number',
        'groups_count',
    )

    list_display_links = ('name',)

    search_fields = (
        'name',
        'email',
        'phone_number',
    )

    list_filter = ('groups',)

    filter_horizontal = ('groups',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('name',)
        }),
        ('Контакты', {
            'fields': (
                'email',
                'phone_number',
            )
        }),
        ('Группы', {
            'fields': ('groups',)
        }),
        ('Дополнительно', {
            'fields': ('description',),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Групп')
    def groups_count(self, obj):
        return obj.groups.count()


# GROUPS

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'students_count',
        'teachers_count',
    )

    search_fields = ('name',)

    fieldsets = (
    ('Информация о группе', {
        'fields': (
            'name',
            'description',
        )
    }),
)

    @admin.display(description='Учеников')
    def students_count(self, obj):
        return obj.students.count()

    @admin.display(description='Преподавателей')
    def teachers_count(self, obj):
        return obj.teachers.count()


# MODULES

class StepInline(admin.TabularInline):
    model = Step
    extra = 1
    fields = (
        'title',
        'order',
    )
    ordering = ('order',)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'steps_count',
        'students_count',
    )

    search_fields = ('name',)

    inlines = (StepInline,)

    fieldsets = (
        ('Информация о модуле', {
            'fields': (
                'name',
                'description',
            )
        }),
    )

    @admin.display(description='Шагов')
    def steps_count(self, obj):
        return obj.steps.count()

    @admin.display(description='Учеников')
    def students_count(self, obj):
        return obj.students.count()


# STEPS

@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'module',
        'order',
    )

    list_display_links = ('title',)

    search_fields = (
        'title',
        'module__name',
    )

    list_filter = ('module',)

    ordering = (
        'module',
        'order',
    )

    list_editable = ('order',)


# STUDENT PROGRESS

@admin.register(StepProgress)
class StepProgressAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'step',
        'module_name',
        'status',
        'completed_at',
        'is_completed',
    )

    list_display_links = (
        'student',
        'step',
    )

    search_fields = (
        'student__name',
        'student__email',
        'step__title',
        'step__module__name',
    )

    list_filter = (
        'is_completed',
        'step__module',
        'completed_at',
    )

    list_editable = ('is_completed',)

    autocomplete_fields = (
        'student',
        'step',
    )

    readonly_fields = ('completed_at',)

    @admin.display(description='Модуль')
    def module_name(self, obj):
        return obj.step.module.name

    @admin.display(description='Статус', boolean=True)
    def status(self, obj):
        return obj.is_completed

    def save_model(self, request, obj, form, change):
        from django.utils import timezone

        if obj.is_completed and obj.completed_at is None:
            obj.completed_at = timezone.now()

        elif not obj.is_completed:
            obj.completed_at = None

        super().save_model(request, obj, form, change)
