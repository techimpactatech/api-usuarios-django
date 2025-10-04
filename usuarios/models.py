from django.db import models
from django.db.models.functions import Now

class Usuario(models.Model):
    # id INTEGER SERIAL (compatível com Java que você mudou para Integer)
    id = models.AutoField(primary_key=True)

    nome = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    data_criacao = models.DateTimeField(db_default=Now(), editable=False)

    class Meta:
        db_table = 'users'   # <- usa a tabela compartilhada
        ordering = ['id']
        managed = False      # <- Django NÃO cria/edita/drope essa tabela