[app]
title = osanka
package.name = osanka
package.domain = org.bro.osanka
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,kivymd,jnius,plyer
orientation = portrait
fullscreen = 1
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Разрешения для Android 14
android.permissions = FOREGROUND_SERVICE, FOREGROUND_SERVICE_SPECIAL_USE, POST_NOTIFICATIONS

# Настройка Foreground Service
android.services = spine_service:service.py:foreground

# Добавляем тип specialUse в манифест
android.manifest.service_attributes = android:foregroundServiceType="specialUse"
android.manifest.xml = """
<meta-data android:name="android.app.PROPERTY_SPECIAL_USE_FGS_SUBTYPE" android:value="Posture control and screen state tracking for health purposes"/>
"""

# Версии SDK под требования Google
android.api = 34
android.minapi = 26
android.ndk = 27c
icon.filename = icon.png

[buildozer]
log_level = 2
warn_on_root = 1
