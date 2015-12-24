# redshiftadmin

## Overview
AWS Redshift Administration Site (under construction)
by finetea@gmail.com (20151222)

## Usage
- Make an SSH tunnel to your Redshift endpoint from your localhost with port 54390
- Change CONNECTION_INFO in settings.py file
- Run server : python manage.py runserver
- Access by web browser : http://127.0.0.1:8000
- Admin page for the site : http://127.0.0.1:8000/admin
- Admin account: suser/suser



## Dependency
- PyBatis 1.5 : [link](https://github.com/manniwood/Pybatis)
- DataTables 1.10.10 : [link](https://www.datatables.net/)
- django-tables2-1.0.5

## Reference
- amazon-redshift-utils : [link](https://github.com/awslabs/amazon-redshift-utils)
