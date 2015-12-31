# coding: utf-8

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from redshift.models import DBConnection, DBQuery, get_result
from redshift.controls import RedshiftDBController

DEFAULT_CONNECTION		= 'none'
DEFAULT_VIEW			= 'datatable'
DEFAULT_DATASOURCE		= 'table_info'
SESSIONKEY_CONNECTION	= 'SELECTED_CONNECTION'
SESSIONKEY_VIEW			= 'SELECTED_VIEW'
SESSIONKEY_DATASOURCE	= 'SELECTED_DATASOURCE'

# Create your views here.

def view_page(request, view, datasource):
	request.session[SESSIONKEY_VIEW] = view
	request.session[SESSIONKEY_DATASOURCE] = datasource
	
	ds = None
	desc = None
	try:
		ds = DBQuery.objects.get(title=datasource)
		desc = ds.desc
	except Exception as e:
		desc = 'Error: No datasource found.'
		
	pagetitle = 'Description: [%s] view of datasource [%s], %s' %(view, datasource, desc)	
	conns = DBConnection.objects.all()
	views = ['datatable', 'pivottable']
	datasources = DBQuery.objects.order_by('title')
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
	if isinstance(result, basestring):
		dic["error"] = result #gets error message
	else:
		(cols, res) = result
		dic["columns"] = cols
		dic["data"] = res

	return JsonResponse(dic)
