from __future__ import unicode_literals

import django_tables2 as tables


class RedshiftDBController:

	@staticmethod
	def define_table_class(table_name, columns):
	    attrs = dict((c, tables.Column()) for c in columns)
	    klass = type(table_name, (tables.Table,), attrs)
	    return klass

	@staticmethod
	def make_table(colnames, results):
	    "Return all rows from a cursor as a dict"
	    return [
	        dict(zip(colnames, row))
	        for row in results
	    ]
