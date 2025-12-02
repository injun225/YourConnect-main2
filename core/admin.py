# Register your models here.
from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(MentorSession)
admin.site.register(JobPost)
admin.site.register(JobApplication)
admin.site.register(JobBookmark)
admin.site.register(Experience)
admin.site.register(Membership)
admin.site.register(AiFeedback)
admin.site.register(Chat)
admin.site.register(ChatParticipant)
admin.site.register(ChatMessage)
