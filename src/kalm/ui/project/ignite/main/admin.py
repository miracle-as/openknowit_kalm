from django.contrib import admin

# Register your models here.
from .models import project
from .models import service
from .models import maindata
from .models import user
from .models import group


admin.site.register(project)
admin.site.register(service)
admin.site.register(maindata)
admin.site.register(user)
admin.site.register(group)

