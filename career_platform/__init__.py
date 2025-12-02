import pymysql

# MySQLdb 대신 pymysql을 사용하도록 등록
pymysql.install_as_MySQLdb()

from core.celery import app as celery_app

__all__ = ('celery_app',)
