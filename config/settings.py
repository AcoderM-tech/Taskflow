from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


def _load_env(path):
    if not path.exists():
        return
    for raw in path.read_text(encoding='utf-8').splitlines():
        line = raw.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, val = line.split('=', 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key not in os.environ or os.environ.get(key, '') == '':
            os.environ[key] = val


_load_env(BASE_DIR / '.env')


def _env_bool(name, default=False):
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.lower() in ('1', 'true', 'yes', 'on')


_raw_secret = os.getenv('SECRET_KEY', '')
if not _raw_secret:
    if os.getenv('DJANGO_ENV') == 'production':
        raise ValueError('SECRET_KEY must be set in production environment')
    _raw_secret = 'django-insecure-dev-only-change-me-in-production'

SECRET_KEY = _raw_secret

DEBUG = _env_bool('DEBUG', True)

_allowed_raw = os.getenv('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = (
    [h.strip() for h in _allowed_raw.split(',') if h.strip()]
    if _allowed_raw
    else (['127.0.0.1', 'localhost'] if DEBUG else [])
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mainapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Session: 15 daqiqa faol bo'lmasa avtomatik chiqib ketadi
SESSION_COOKIE_AGE = 60 * 15
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR / 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        },
    },
    {
        'NAME': 'mainapp.validators.CustomPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'mainapp.CustomUser'