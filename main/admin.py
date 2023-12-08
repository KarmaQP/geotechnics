from django.contrib import admin
from .models import FilesManagement

# Register your models here.


class FilesManagementAdmin(admin.ModelAdmin):
  list_display = ('gmsh_file',)


admin.site.register(FilesManagement, FilesManagementAdmin)
