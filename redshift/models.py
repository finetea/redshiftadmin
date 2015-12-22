from __future__ import unicode_literals

from django.db import models

# Create your models here.


def getcolnames(cursor):
	return [col[0] for col in cursor.description]

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = getcolnames(cursor)
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]