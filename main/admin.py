from django.contrib import admin
from .models import Message, Answer


admin.site.register(Answer)
admin.site.register(Message)


'''
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("sender")
    list_filter = ()
    search_fields = ()
    ordering = ()


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender")
    list_filter = ()
    search_fields = ()
    ordering = ()
'''