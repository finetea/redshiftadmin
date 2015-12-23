from django.conf import settings
from django.shortcuts import render

#for model

from controls import RedshiftDBController

import psycopg2
import psycopg2.extras
import pybatis
import pybatis.psycopg2_jinja2 as pg2
import logging


# Create your views here.

def show_tables(request):
	logging.getLogger().setLevel(logging.DEBUG)

	conn = psycopg2.connect('user=postgres dbname=testdb password=testpass!! host=localhost port=54390')

	SQL_MAP = pg2.SQLMap(conn, settings.MAPPER_DIR, log_behaviour=pybatis.LOG_PER_CALL)
	SQL_MAP.begin()
	results = SQL_MAP.select(file='table_list.sql', log=True)  # this will log to logging
	print(results)
	colnames = SQL_MAP.get_colnames()
	print(colnames)
	SQL_MAP.end()
	res = RedshiftDBController.make_table(colnames, results)

	table = RedshiftDBController.define_table('tablename', colnames)(res)
	table.attrs['id'] = 'table_id'
	table.attrs['class'] = 'display'
	table.orderable = False

	return render(request, 'show_tables.html', {'table':table})
