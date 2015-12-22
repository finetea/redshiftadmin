from django.shortcuts import render
from django.db import connections

#for model
import django_tables2 as tables


# Create your views here.

def show_tables(request):
	data = [
	    {"name": "Bradley"},
	    {"name": "Stevie"},
	]

	class NameTable(tables.Table):
	    name = tables.Column()

	table = NameTable(data)

	return render(request, 'show_tables.html', {'table':table})