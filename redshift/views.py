# coding: utf-8

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from redshift.models import DBConnection, DBQuery, get_result_table, get_result
from redshift.controls import RedshiftDBController

DEFAULT_CONNECTION		= 'none'
DEFAULT_VIEW			= 'datatable'
DEFAULT_DATASOURCE		= 'table_info'
SESSIONKEY_CONNECTION	= 'SELECTED_CONNECTION'
SESSIONKEY_VIEW			= 'SELECTED_VIEW'
SESSIONKEY_DATASOURCE	= 'SELECTED_DATASOURCE'

# Create your views here.

def view_page_old(request, view, datasource):
	#menu part
	request.session[SESSIONKEY_VIEW] = view
	request.session[SESSIONKEY_DATASOURCE] = datasource
	if not request.session.has_key(SESSIONKEY_CONNECTION):
		request.session[SESSIONKEY_CONNECTION] = DBConnection.objects.all()[0].title
	
	ds = DBQuery.objects.get(title=datasource)
	pagetitle = 'Description: [%s] view of datasource [%s], %s' %(view, datasource, ds.desc)	
	conns = DBConnection.objects.all()
	views = ['datatable','pivottable']
	datasources = DBQuery.objects.all()
	#content part
	table = get_result_table(request.session[SESSIONKEY_CONNECTION], datasource)
	error = None
	if isinstance(table, basestring):
		error = 'Error: %s'%table
	return render(request, 'view_page_old.html', {'pagetitle':pagetitle, 'connections':conns, 'views':views, 'datasources':datasources, 'error':error, 'table':table})

def view_page(request, view, datasource):
	#menu part
	request.session[SESSIONKEY_VIEW] = view
	request.session[SESSIONKEY_DATASOURCE] = datasource
	
	ds = DBQuery.objects.get(title=datasource)
	pagetitle = 'Description: [%s] view of datasource [%s], %s' %(view, datasource, ds.desc)	
	conns = DBConnection.objects.all()
	views = ['datatable']
	datasources = DBQuery.objects.all()
	#content part
	return render(request, 'view_page.html', {'pagetitle':pagetitle, 'connections':conns, 'views':views, 'datasources':datasources, 'data':datasource})


def view_page_default(request):
	selected_view = request.session.get(SESSIONKEY_VIEW, DEFAULT_VIEW)
	selected_datasource = request.session.get(SESSIONKEY_DATASOURCE, DEFAULT_DATASOURCE)
	request.session[SESSIONKEY_VIEW] = selected_view
	request.session[SESSIONKEY_DATASOURCE] = selected_datasource	
	
	return view_page(request, selected_view, selected_datasource)
	
	
def set_connection(request, connection):
	print "Connection is set to [%s]"%connection
	request.session[SESSIONKEY_CONNECTION] = connection
	return view_page_default(request)


def get_data(request, datasource):
	result = get_result(request.session[SESSIONKEY_CONNECTION], datasource)
	dic = {}
	error = None
	if isinstance(result, basestring):
		error = result
	else:
		(cols, res) = result
		dic["columns"] = cols
		dic["data"] = res

	return JsonResponse(dic)
