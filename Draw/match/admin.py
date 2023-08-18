from django.contrib import admin
from .models import MatchUser
from .forms import MatchBasedForm

# Register your models here.
admin.site.register(MatchUser)