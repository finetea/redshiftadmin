from __future__ import unicode_literals

import django_tables2 as tables

class RedshiftDBController:

	@staticmethod
	def define_table_class(table_name, columns):
	    attrs = dict((c, tables.Column()) for c in columns)
	    klass = type(table_name, (tables.Table,), attrs)
	    return klass

	@staticmethod
	def make_result_dict(colnames, results):
		"Return all rows from a cursor as a dict"
		if results == None or len(results) == 0:
			results = []
		return [
			dict(zip(colnames, row))
			for row in results
		]

	@staticmethod
	def make_column_dict(colnames):
		result = []
		for name in colnames:
			result.append({"title":name, "data":name})
		
		return result