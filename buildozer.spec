[app]
title = osanka
package.name = osanka
package.domain = org.bro.osanka
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Добавлен обязательный модуль android для работы с правами и jnius
requirements = python3,kivy,kivymd,jnius,plyer,android

orientation = portrait
fullscreen = 1
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Разрешения для Android 14 (добавлена базовая служба)
android.permissions = FOREGROUND_SERVICE, FOREGROUND_SERVICE_SPECIAL_USE, POST_NOTIFICATIONS

# Настройка Foreground Service с жестким указанием типа foregroundServiceType через двоеточие
# Формат: имя:путь_к_скрипту:тип:параметры
android.services = spine_service:service.py:foreground:foregroundServiceType=specialUse

# Официальный способ прокинуть <meta-data> внутрь тега <application> без ломания XML
android.meta_data = android.app.PROPERTY_SPECIAL_USE_FGS_SUBTYPE=Posture control and screen state tracking for health purposes

# Версии SDK под жесткие требования Google Play
android.api = 34
android.minapi = 26
android.ndk = 25b
icon.filename = icon.png

[buildozer]
log_level = 2
warn_on_root = 1
