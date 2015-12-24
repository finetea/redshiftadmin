# coding: utf-8

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection


#for model

from controls import RedshiftDBController

import psycopg2
import psycopg2.extras
import pybatis
import pybatis.psycopg2_jinja2 as pg2
import logging


# Create your views here.

def get_result_table(source):
	logging.getLogger().setLevel(logging.DEBUG)

	conn = psycopg2.connect(settings.CONNECTION_INFO)

	SQL_MAP = pg2.SQLMap(conn, settings.MAPPER_DIR, log_behaviour=pybatis.LOG_PER_CALL)
	SQL_MAP.begin()
	sqlfilename = source + '.sql'
	results = SQL_MAP.select(file=sqlfilename, log=True)  # this will log to logging
	colnames = SQL_MAP.get_colnames()
	SQL_MAP.end()
	res = RedshiftDBController.make_table(colnames, results)

	if isinstance(source, unicode):
		source = source.encode("UTF-8")
	table = RedshiftDBController.define_table_class(source, colnames)(res)
	table.attrs['id'] = 'table_id'
	table.attrs['class'] = 'display'
	table.orderable = False
	return table

def show_table_info(request):
	table = get_result_table('table_info')
	return render(request, 'table_info.html', {'table':table})

def view_page(request, page):
	table = get_result_table(page)
	return render(request, 'view_page.html', {'table':table})

def get_json_data(request, source):
	print("get_data=[%s]"%source)
	
	logging.getLogger().setLevel(logging.DEBUG)

	conn = psycopg2.connect(settings.CONNECTION_INFO)

	SQL_MAP = pg2.SQLMap(conn, settings.MAPPER_DIR, log_behaviour=pybatis.LOG_PER_CALL)
	SQL_MAP.begin()
	sqlfilename = source + '.sql'
	results = SQL_MAP.select(file=sqlfilename, log=True)
	SQL_MAP.end()

	return JsonResponse(dict(data=results))
	