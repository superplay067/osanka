[app]
title = osanka
package.name = osanka
package.domain = org.bro.osanka
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

requirements = python3,kivy,kivymd,jnius,plyer,android

orientation = portrait
fullscreen = 1
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Разрешения под Android 14
android.permissions = FOREGROUND_SERVICE, FOREGROUND_SERVICE_SPECIAL_USE, POST_NOTIFICATIONS

# Настройка Foreground Service (Тип specialUse прокинут напрямую в синтаксис p4a)
android.services = spine_service:service.py:foreground:foregroundServiceType=specialUse

# Метаданные для обоснования specialUse в Google Play
android.meta_data = android.app.PROPERTY_SPECIAL_USE_FGS_SUBTYPE=Posture control and screen state tracking for health purposes

# Версии SDK (NDK обновлен до 26b для стабильной сборки под API 34)
android.api = 34
android.minapi = 26
android.ndk = 26b
icon.filename = icon.png

[buildozer]
log_level = 2
warn_on_root = 1
