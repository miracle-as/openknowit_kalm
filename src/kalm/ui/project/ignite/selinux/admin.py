from django.contrib import admin
from .models import Selinux
from .models import SElinuxEvent
from .models import SetroubleshootEntry


admin.site.register(Selinux)
admin.site.register(SElinuxEvent)
admin.site.register(SetroubleshootEntry)



