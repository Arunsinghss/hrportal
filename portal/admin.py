from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Comment)
admin.site.register(Queries)
admin.site.register(Employee)
admin.site.register(Policy)
admin.site.register(Document)
admin.site.register(EffectiveDated)
