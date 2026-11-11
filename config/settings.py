"""
Postavke Django projekta „Vječna spomen”.

Sve tajne i vrijednosti koje ovise o okruženju (računalo, hosting) čitaju se
iz datoteke .env. Primjer je u .env.example.
"""

import sys
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")


# Aplikacije

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # vanjski paketi
    "django_tailwind_cli",
    "django_htmx",
    # naše aplikacije
    "korisnici",
    "jezgra",
    "pristup",
    "mediji",
    "knjiga",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Baza podataka (adresa baze dolazi iz .env)

DATABASES = {"default": env.db("DATABASE_URL")}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Korisnici i lozinke

AUTH_USER_MODEL = "korisnici.Korisnik"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# SAMO u testovima: brzi hasher, da testovi ne troše sekunde na svaku lozinku.
# Na poslužitelju se ova grana nikad ne izvršava (tamo se ne pokreće "manage.py test").
if "test" in sys.argv[1:2]:
    PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]


# Jezik i vrijeme

LANGUAGE_CODE = "hr"
TIME_ZONE = "Europe/Zagreb"
USE_I18N = True
USE_TZ = True


# Statičke datoteke (CSS, JavaScript, slike)

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Tailwind: ulaz.css pišemo mi, izlaz.css generira Tailwind (nije u Gitu).
TAILWIND_CLI_SRC_CSS = "tailwind/ulaz.css"
TAILWIND_CLI_DIST_CSS = "css/izlaz.css"
TAILWIND_CLI_VERSION = "4.3.4"  # ista verzija za oba člana tima


# Učitane datoteke (lokalno u mapi media/, koja nije u Gitu; u produkciji R2, P-26)

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"


# Ograničenja medija (odluke 12 i 18). Mijenjaju se samo ovdje.

MEDIJI_MAX_SLIKA_PO_GROBU = 300
MEDIJI_MAX_VIDEO_SEKUNDI_PO_GROBU = 20 * 60
MEDIJI_MAX_BAJTOVA_PO_GROBU = 2 * 1024**3
MEDIJI_MAX_VIDEO_SEKUNDI = 5 * 60
MEDIJI_MAX_VIDEO_BAJTOVA = 1024**3
MEDIJI_MAX_SLIKA_BAJTOVA = 30 * 1024**2  # tehnička odluka: dovoljno za HEIC/JPEG s mobitela
MEDIJI_MAX_STRANICA_SLIKE_PX = 2048


# Ograničenje pogrešnih pokušaja (odluka 5, pristup/ogranicenja.py).
# vrsta: (najviše po IP adresi za isti cilj, prozor u minutama,
#         najviše po cilju s bilo koje adrese, prozor u minutama)

OGRANICENJA_POKUSAJA = {
    "lozinka": (5, 15, 30, 60),
}

# Na hostingu je aplikacija iza posrednika (proxyja), pa se IP adresa posjetitelja
# čita iz zaglavlja X-Forwarded-For. Lokalno mora ostati False.
IZA_PROXYJA = env.bool("IZA_PROXYJA", default=False)


# QR kodovi: početak linka na pločici, VELIKIM slovima (odluka 18).
# Lokalno IP adresa računala u kućnoj mreži, da mobitel može otvoriti kod.

QR_BAZNI_URL = env("QR_BAZNI_URL", default="HTTP://LOCALHOST:8000/G/").upper()


# E-mail: lokalno se poruke ispisuju u terminal umjesto da se šalju

MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
    },
}
