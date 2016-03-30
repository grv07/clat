DEBUG = True
ALLOWED_HOSTS = ['*']
STATIC_ROOT = ""
RESTRICT_MODULE_TIME = 1
SITE_NAME = 'http://localhost:8000'
import os, sys
file_path = os.path.abspath(__file__)
DIR_NAME = os.path.dirname(os.path.dirname(file_path))
SITE_ID = 6

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'STORAGE_ENGINE': 'MyISAM / INNODB / ETC',
        'OPTIONS': {
            "init_command": "SET storage_engine=MyISAM",
            'read_default_file': DIR_NAME + '/mysql.cnf',
        },
    },
    #'city': {
     #   'NAME': 'city_data',
      #  'ENGINE': 'django.db.backends.mysql',
      #  'USER': 'root',
      #  'PASSWORD': 'root'
    #}
    # 'default': {
    # 'ENGINE': 'django.db.backends.sqlite3',
    # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
}