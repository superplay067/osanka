# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.utils import platform
from kivy.graphics import Color, RoundedRectangle, Line

# Настраиваем глубокий матовый черный фон окна
Window.clearcolor = (0.05, 0.05, 0.05, 1)

class NeonButton(Button):
    def __init__(self, **kwargs):
        super(NeonButton, self).__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # Скрываем дефолтный фон
        self.text = "Подключить"
        self.font_size = "20sp"
        self.bold = True
        self.color = (1, 1, 1, 1)
        self.size_hint = (None, None)
        self.size = (220, 70)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            # Пастельно-коралловый цвет (RGBA)
            coral = (0.95, 0.5, 0.45)
            x, y, w, h = self.x, self.y, self.width, self.height
            r = [35]  # Скругление для овала

            # ТРЕХСЛОЙНОЕ НЕОНОВОЕ СВЕЧЕНИЕ
            for i, alpha in [(12, 0.1), (6, 0.2), (2, 0.4)]:
                Color(coral[0], coral[1], coral[2], alpha)
                Line(rounded_rectangle=(x-i, y-i, w+i*2, h+i*2, r[0]), width=i)

            # Основное тело овальной кнопки
            Color(coral[0], coral[1], coral[2], 1)
            RoundedRectangle(pos=(x, y), size=(w, h), radius=r)

class OsankaApp(App):
    def build(self):
        layout = BoxLayout()
        self.btn = NeonButton()
        self.btn.bind(on_release=self.toggle_service)
        layout.add_widget(self.btn)
        return layout

    def on_start(self):
        # Автоматический запрос разрешений на уведомления для Android 13+
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            # Передаем функцию обратного вызова, чтобы не запускать сервис раньше времени
            request_permissions([Permission.POST_NOTIFICATIONS], self.permission_callback)

    def permission_callback(self, permissions, grants):
        # Если разрешение на пуши получено — стартуем фоновый движок
        if grants and grants[0]:
            self.start_spine_service()

    def toggle_service(self, instance):
        if platform == 'android':
            self.start_spine_service()

    def start_spine_service(self):
        from android import mActivity
        from jnius import autoclass

        context = mActivity.getApplicationContext()
        
        # Получаем правильный Java-класс службы, сгенерированный python-for-android
        # Шаблон названия класса: org.kivy.android.project.Service[Имя_службы_с_большой_буквы]
        try:
            ServiceClass = autoclass('org.bro.osanka.ServiceSpine_service')
            Intent = autoclass('android.content.Intent')
            service_intent = Intent(context, ServiceClass)
            
            # Безопасный запуск Foreground Service под Android 14
            context.startForegroundService(service_intent)
        except Exception as e:
            print(f"Ошибка запуска службы: {str(e)}")

if __name__ == '__main__':
    OsankaApp().run()
