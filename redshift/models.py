from __future__ import unicode_literals

from django.db import models, connection
from django.contrib.postgres.fields.ranges import IsEmpty
from django.conf import settings

from redshift.controls import RedshiftDBController

import psycopg2
import psycopg2.extras
import pybatis
import pybatis.psycopg2_jinja2 as pg2
import logging

# Create your models here.

class DBConnection(models.Model):
	title = models.CharField(max_length=100, unique=True)
	user = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	dbname = models.CharField(max_length=100)
	host = models.CharField(max_length=200, default='localhost')
	port = models.PositiveIntegerField(default=5439)

	@staticmethod
	def isNotEmpty(s):
		return bool(s and s.strip())
    
	def get_conn_str(self):
		str = ' '
		if DBConnection.isNotEmpty(self.user):
			str = str + 'user={}'.format(self.user.strip())
		if DBConnection.isNotEmpty(self.password):
			str = str + ' password={}'.format(self.password.strip())
		if DBConnection.isNotEmpty(self.dbname):
			str = str + ' dbname={}'.format(self.dbname.strip())
		if DBConnection.isNotEmpty(self.host):
			str = str + ' host={}'.format(self.host.strip())
		if self.port > 0:
			str = str + ' port={}'.format(self.port)            
		return str
	#end of class DBConnection    

class DBQuery(models.Model):
	title = models.CharField(max_length=100, unique=True)
	desc = models.CharField(max_length=1024)
	query = models.TextField(max_length=4096)
	#end of class DBQuery

#returns tuple of colname list and result dictionary, error string when gets error
def get_result(connection_title, source):
	logging.getLogger().setLevel(logging.DEBUG)
	
	try:
		connobj = DBConnection.objects.get(title=connection_title)
	except Exception as e:
		return 'Set connection info first by Admin'
	
	conninfo = connobj.get_conn_str()
	if isinstance(conninfo, unicode):
		conninfo = conninfo.encode("UTF-8")
	
	logging.info("Connection info from get_result_table() [%s]" % conninfo)
	
	try:
		queryitem = DBQuery.objects.get(title=source)
	except Exception as e:
		return 'Set query first by Admin'
	
	try:
		conn = psycopg2.connect(conninfo)
	except Exception as e:
		return 'Connection is not established'
	
	SQL_MAP = pg2.SQLMap(conn, '', log_behaviour=pybatis.LOG_PER_CALL)
	SQL_MAP.begin()
	results = SQL_MAP.select(inline=queryitem.query, log=True)
	colnames = SQL_MAP.get_colnames()
	SQL_MAP.end()
	
	res = RedshiftDBController.make_result_dict(colnames, results)	
	cols = RedshiftDBController.make_column_dict(colnames)
	
	return (cols, res)
	#end of function get_result_table()