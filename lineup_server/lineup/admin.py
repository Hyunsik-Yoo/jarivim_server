from django.contrib import admin
from .models import *

admin.site.register(Restaurant)
admin.site.register(Vote)
admin.site.register(PredictProportion)
admin.site.register(Category)

# Register your models here.
# Model을 등록하여 admin페이지에서 데이터들을 볼 수 있다.
