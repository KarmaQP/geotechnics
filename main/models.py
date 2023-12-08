import os
from django.db import models


# Create your models here.


class FilesManagement(models.Model):
  gmsh_file = models.FileField(upload_to='data', null=True)

  def __str__(self):
    return self.gmsh_file.name

  def delete(self, *args, **kwargs):
    os.remove(self.gmsh_file.name)
    super(FilesManagement, self).delete(*args, **kwargs)
