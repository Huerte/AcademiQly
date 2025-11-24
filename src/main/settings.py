from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", cast=bool, default=False)

ALLOWED_HOSTS = ["*"] if DEBUG else ["*"]

INSTALLED_APPS = [
    'jazzmin',

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",

    "core",
    "user",
    "room",
    "dashboard",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",

    "user.middleware.AdminAccessMiddleware",
]

ROOT_URLCONF = "main.urls"
WSGI_APPLICATION = "main.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "room.context_processors.notification_context",
            ],
        },
    },
]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_DOMAIN = config("SITE_DOMAIN", default="http://localhost:8000")

SITE_ID = 1
LOGIN_URL = "/auth/login/"
LOGIN_REDIRECT_URL = "/auth/role-selection/"
LOGOUT_REDIRECT_URL = "/"

ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_SIGNUP_REDIRECT_URL = "/auth/role-selection/"

SOCIALACCOUNT_ADAPTER = "user.adapters.CustomSocialAccountAdapter"
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION = False
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
SOCIALACCOUNT_FORMS = {}
ACCOUNT_FORMS = {}

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "OAUTH_PKCE_ENABLED": True,
        "APP": {
            "client_id": config("GOOGLE_OAUTH2_CLIENT_ID", default=""),
            "secret": config("GOOGLE_OAUTH2_SECRET", default=""),
            "key": "",
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

JAZZMIN_SETTINGS = {
    "site_title": "AcademiQly Admin",
    "site_header": "AcademiQly",
    "site_brand": "AcademiQly",
    "welcome_sign": "Welcome to AcademiQly Admin",
    "copyright": "AcademiQly",
    "user_avatar": None,
    "search_model": [
        "room.Room",
        "room.Activity",
        "user.StudentProfile",
        "user.TeacherProfile",
    ],
    "topmenu_links": [
        {"app": "room"},
        {"app": "user"},
    ],
    "usermenu_links": [
        {"name": "My Rooms", "url": "/room/all/"},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": [
        "room",
        "user",
        "auth",
    ],
    "icons": {
        "room.Room": "bi bi-door-open",
        "room.Activity": "bi bi-journal-text",
        "room.Announcement": "bi bi-megaphone",
        "room.Submission": "bi bi-inbox",
        "user.StudentProfile": "bi bi-person",
        "user.TeacherProfile": "bi bi-mortarboard",
        "auth.user": "bi bi-people",
        "auth.Group": "bi bi-people",
    },
    "default_icon_parents": "bi bi-folder2",
    "default_icon_children": "bi bi-circle",
}

JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",
    "navbar": "navbar-dark navbar-primary",
    "sidebar": "sidebar-dark-primary",
    "sidebar_fixed": True,
    "theme_appearance": "dark",
    "footer_fixed": False,
    "actions_sticky_top": True,
    "actions_sticky_bottom": True,
    "button_classes": {
        "primary": "btn btn-primary",
        "secondary": "btn btn-outline-secondary",
    },
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = config("TIME_ZONE", default="UTC")
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

if not DEBUG:
    STATIC_ROOT = BASE_DIR / "staticfiles"
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
DEBUG_PROPAGATE_EXCEPTIONS = True


AGORA_APP_ID = config("AGORA_APP_ID", default="")

AGORA_APP_CERTIFICATE = config("AGORA_APP_CERTIFICATE", default="")

AGORA_TEMP_TOKEN = config("AGORA_TEMP_TOKEN", default="")

AGORA_TEMP_TOKEN = config("AGORA_TEMP_TOKEN", default="")


if DEBUG and AGORA_APP_ID:
    print(f"[DEBUG] Agora APP_ID loaded: {AGORA_APP_ID[:10]}...")
if DEBUG and not AGORA_APP_ID:
    print("[WARNING] AGORA_APP_ID not found in environment variables")

if DEBUG:
    CSRF_TRUSTED_ORIGINS = [
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "https://6ad370209bc2.ngrok-free.app",
    ]
else:
    CSRF_TRUSTED_ORIGINS = [config("SITE_DOMAIN")]

SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG