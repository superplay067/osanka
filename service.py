# -*- coding: utf-8 -*-
import time
from jnius import autoclass

# Заранее инициализируем все необходимые Android-классы (экономим батарею)
PythonService = autoclass('org.kivy.android.PythonService')
service_context = PythonService.mService

Context = autoclass('android.content.Context')
Intent = autoclass('android.content.Intent')
PendingIntent = autoclass('android.content.PendingIntent')
NotificationManager = autoclass('android.app.NotificationManager')
NotificationChannel = autoclass('android.app.NotificationChannel')
NotificationCompat = autoclass('androidx.core.app.NotificationCompat') or autoclass('android.app.Notification$Builder')
Build = autoclass('android.os.Build')

def setup_foreground_notification():
    """Создает постоянное уведомление, обязательное для Foreground Service под Android 14"""
    channel_id = "osanka_service_channel"
    channel_name = "Мониторинг осанки (Фон)"
    
    # Сначала создаем канал уведомлений (для Android 8.0+)
    if Build.VERSION.SDK_INT >= 26:
        importance = NotificationManager.IMPORTANCE_LOW
        channel = NotificationChannel(channel_id, channel_name, importance)
        notification_manager = service_context.getSystemService(Context.NOTIFICATION_SERVICE)
        notification_manager.createNotificationChannel(channel)
    
    # Строим постоянное уведомление службы
    if Build.VERSION.SDK_INT >= 26:
        builder = autoclass('android.app.Notification$Builder')(service_context, channel_id)
    else:
        builder = autoclass('android.app.Notification$Builder')(service_context)
        
    builder.setContentTitle("OSANKA запущена")
    builder.setContentText("Контролируем спину при разблокировке экрана")
    # Используем дефолтную системную иконку, чтобы не упасть, если кастомная не подгрузилась
    builder.setSmallIcon(service_context.getApplicationInfo().icon)
    builder.setOngoing(True)
    
    # 101 — уникальный ID нашей фоновой службы
    service_context.startForeground(101, builder.build())

def send_trigger_notification():
    """Отправляет нативный пуш 'Выпрямите осанку' без использования plyer"""
    channel_id = "osanka_alerts_channel"
    channel_name = "Напоминания об осанке"
    notification_id = 202
    
    notification_manager = service_context.getSystemService(Context.NOTIFICATION_SERVICE)
    
    if Build.VERSION.SDK_INT >= 26:
        importance = NotificationManager.IMPORTANCE_HIGH
        channel = NotificationChannel(channel_id, channel_name, importance)
        notification_manager.createNotificationChannel(channel)
        builder = autoclass('android.app.Notification$Builder')(service_context, channel_id)
    else:
        builder = autoclass('android.app.Notification$Builder')(service_context)
        
    builder.setContentTitle("Здоровье спины 🧘‍♂️")
    builder.setContentText("Вы разблокировали телефон. Выпрямите осанку!")
    builder.setSmallIcon(service_context.getApplicationInfo().icon)
    builder.setAutoCancel(True)
    
    # Пробиваем приоритет для старых версий Android
    if Build.VERSION.SDK_INT < 26:
        builder.setPriority(1) # HIGH
        
    notification_manager.notify(notification_id, builder.build())

def start_monitoring():
    power_service = service_context.getSystemService(Context.POWER_SERVICE)
    
    # Флаг триггера однократного срабатывания
    last_screen_state = True 

    while True:
        try:
            # Опрашиваем состояние экрана (ВКЛ/ВЫКЛ)
            is_interactive = power_service.isInteractive()
            
            # Умный триггер: переход из ВЫКЛ (False) в ВКЛ (True)
            if is_interactive and not last_screen_state:
                send_trigger_notification()
            
            # Обновляем состояние для следующей секунды
            last_screen_state = is_interactive
            
        except Exception as e:
            print(f"Ошибка в цикле мониторинга Osanka: {str(e)}")
            
        time.sleep(1)

if __name__ == '__main__':
    # Включаем автоперезапуск службы при убийстве системой
    service_context.setAutoRestartService(True)
    
    # Срочно активируем постоянное уведомление, чтобы Android 14 не убил процесс
    try:
        setup_foreground_notification()
    except Exception as e:
        print(f"Ошибка инициализации Foreground Service: {str(e)}")
        
    # Запускаем бесконечный цикл мониторинга
    start_monitoring()
