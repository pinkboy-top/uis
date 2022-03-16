"""
Django settings for uis project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import time
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$0m8kf!grqtt^528=hxxz+czs*#fuhw0dq1%15lz@6n+l00@uk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user',
    'corsheaders',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # 注册允许跨域中间件
    'check_data.middleware.CheckRequest'  # 检测文件上传大小中间件
]

ROOT_URLCONF = 'uis.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'uis.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# 设置日志记录的基本和日志文件路径
format_str = "{time:YYYY-MM-DD at HH:mm:ss}|{level}|{name}|{function}|{message}"
logger.add(f"{BASE_DIR}/log/" + "run_server_{time}.log", rotation='100KB', format=format_str, encoding="utf-8")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static_cdn")

# 配置 MEDIA_ROOT 作为你上传文件在服务器中的基本路径
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# 配置 MEDIA_URL 作为公用 URL，指向上传文件的基本路径
MEDIA_URL = '/media/'
# 支持上传的文件类型
FILE_TYPE = ['mp4', 'gif', 'jpeg', 'jpg', 'png']
# 设置文件上传的大小最大5M
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 允许全部来源
CORS_ORIGIN_ALLOW_ALL = True  # 如果为True，将不使用白名单，并且将接受所有来源。默认为False。

# 白名单
CORS_ORIGIN_WHITELIST = [
    "http://127.0.0.1"
]

# 允许跨域请求的方法
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Django DRF配置
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        # 默认访问权限
        'rest_framework.permissions.IsAdminUser',
    ],
    # 默认分页
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
}

# 自定义jwt_token配置
JWT_TOKEN = {
    "header": {"alg": "HS256", "typ": "JWT"},
    "payload": {
        # 过期时间默认是12小时
        "exp": time.time() + 60 * 60 * 12,
        # "exp": time.time() + 10,
        "nbf": time.time(),
        # 签发者
        "iss": "pink",
        "iat": "all",
        # 自定义数据区
        "data": {
            "uid": "000",
        }
    }
}


# 关闭服务器信息
SIMPLEUI_HOME_INFO = False
# 设置默认主题，指向主题css文件名。Element-ui风格
SIMPLEUI_DEFAULT_THEME = 'e-purple-pro.css'
SIMPLEUI_CONFIG = {
    # 是否使用系统默认菜单。
    'system_keep': False,

    # 用于菜单排序和过滤, 不填此字段为默认排序和全部显示。 空列表[] 为全部不显示.
    'menu_display': ['用户管理', '好友管理', '附件管理', '选项管理', '认证和权限'],

    # 设置是否开启动态菜单, 默认为False. 如果开启, 则会在每次用户登陆时刷新展示菜单内容。
    # 一般建议关闭。
    'dynamic': False,
    'menus': [
        {
            'app': 'auth',
            'name': '权限认证',
            'icon': 'fas fa-user-shield',
            'models': [
                {
                    'name': '用户列表',
                    'icon': 'fa fa-user',
                    'url': 'auth/user/'
                },
                {
                    'name': '用户组',
                    'icon': 'fa fa-th-list',
                    'url': 'auth/group/'
                }
            ]
        },

        {
            'name': '用户管理',
            'icon': 'fa fa-user',
            'models': [
                {
                    'name': '用户列表',
                    # 注意url按'/admin/应用名小写/模型名小写/'命名。
                    'url': '/ylz/user/user/',
                    'icon': 'fa fa-user-check'
                },
                {
                    'name': '用户信息',
                    # 注意url按'/admin/应用名小写/模型名小写/'命名。
                    'url': '/ylz/user/userinfo/',
                    'icon': 'fas fa-user-shield'
                },
            ]
        },

        {
            'name': '好友管理',
            'icon': 'fa fa-users',
            'models': [
                {
                    'name': '好友列表',
                    # 注意url按'/admin/应用名小写/模型名小写/'命名。
                    'url': '/ylz/user/friend/',
                    'icon': 'fas fa-user-friends'
                },
                {
                    'name': '好友请求',
                    # 注意url按'/admin/应用名小写/模型名小写/'命名。
                    'url': '/ylz/user/friendrequest/',
                    'icon': 'fas fa-user-plus'
                },
            ]
        },

        {
            'name': '附件管理',
            'icon': 'fas fa-folder',
            'models': [
                {
                    'name': '图片列表',
                    # 注意url按'/admin/应用名小写/模型名小写/'命名。
                    'url': '/ylz/user/img/',
                    'icon': 'fas fa-image'
                },

                {
                    'name': '图片类型',
                    # 注意url按'/admin/应用名小写/模型名小写/'命名。
                    'url': '/ylz/user/imgtype/',
                    'icon': 'fas fa-images'
                },
            ]
        },

        {
            'name': '选项管理',
            'icon': 'fas fa-cogs',
            'models': [
                {
                    'name': '选项列表',
                    # 注意url按'/admin/应用名小写/模型名小写/'命名。
                    'url': '/ylz/user/option/',
                    'icon': 'fas fa-cog'
                },

                {
                    'name': '选项类型',
                    # 注意url按'/admin/应用名小写/模型名小写/'命名。
                    'url': '/ylz/user/optiontype/',
                    'icon': 'fas fa-tools'
                },
            ]
        },

    ]
}
