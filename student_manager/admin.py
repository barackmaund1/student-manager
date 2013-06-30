"""The admin page."""

from django.contrib import admin
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from student_manager.models import Student, Exercise


class ExercisesCompleteListFilter(admin.SimpleListFilter):
    title = _('exercises')
    parameter_name = 'points'

    def lookups(self, request, model_admin):
        return (('complete', _('Exercises complete')),
                ('incomplete', _('Exercises incomplete')))

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        total = Exercise.total_num_exercises()
        # find students who have completed all exercises:
        query = Exercise.objects.values('student').annotate(
            count=Count('student')).order_by().filter(count=total)
        completed_student_ids = [i['student'] for i in query]

        if self.value() == 'incomplete':
            return queryset.exclude(id__in=completed_student_ids)
        if self.value() == 'complete':
            return queryset.filter(id__in=completed_student_ids)

    
class StudentAdmin(admin.ModelAdmin):
    list_display = ('matrikel', 'last_name', 'first_name',
                    'number_of_exercises', 'total_points')
    list_filter = (ExercisesCompleteListFilter,)
    search_fields = ('matrikel', 'last_name', 'first_name')


class ExerciseNumberListFilter(admin.SimpleListFilter):
    title = _('number')
    parameter_name = 'number'

    def lookups(self, request, model_admin):
        total = Exercise.total_num_exercises()
        return [(str(i), str(i)) for i in range(1, total + 1)]

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        return queryset.filter(number=self.value)

    
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('number', 'points', 'student')
    list_filter = (ExerciseNumberListFilter,)
    search_fields = ('student__matrikel', 'student__last_name',
                     'student__first_name')


admin.site.register(Student, StudentAdmin)
admin.site.register(Exercise, ExerciseAdmin)
