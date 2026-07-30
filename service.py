# -*- coding: utf-8 -*-
import time
from jnius import autoclass
from plyer import notification

def start_monitoring():
    # Инициализируем Android-сервисы через jnius
    PythonService = autoclass('org.kivy.android.PythonService')
    service_context = PythonService.mService
    
    Context = autoclass('android.content.Context')
    power_service = service_context.getSystemService(Context.POWER_SERVICE)
    
    # Флаг триггера однократного срабатывания
    last_screen_state = True 

    while True:
        try:
            # Опрашиваем состояние экрана (ВКЛ/ВЫКЛ)
            is_interactive = power_service.isInteractive()
            
            # Умный триггер: переход из ВЫКЛ (False) в ВКЛ (True)
            if is_interactive and not last_screen_state:
                # Мгновенно отправляем ровно ОДИН пуш через plyer
                notification.notify(
                    title="Здоровье спины 🧘‍♂️",
                    message="Вы разблокировали телефон. Выпрямите осанку!",
                    app_name="osanka"
                )
            
            # Обновляем состояние для следующей секунды
            last_screen_state = is_interactive
            
        except Exception as e:
            print(f"Ошибка в службе Osanka: {str(e)}")
            
        time.sleep(1)

if __name__ == '__main__':
    PythonService = autoclass('org.kivy.android.PythonService')
    service = PythonService.mService
    
    # Включаем автоперезапуск службы
    service.setAutoRestartService(True)
    
    # Запускаем бесконечный цикл мониторинга
    start_monitoring()
