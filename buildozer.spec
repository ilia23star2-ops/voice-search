[app]

# Название приложения
title = Голосовой поиск проб

# Имя пакета
package.name = voicesearch

# Домен пакета
package.domain = org.example

# Путь к исходникам
source.dir = .

# Включаемые расширения
source.include_exts = py,png,jpg,kv,atlas

# Версия приложения
version = 1.0

# Зависимости Python
requirements = python3,kivy==2.3.0,pyjnius,android,openpyxl==3.1.2

# Ориентация экрана
orientation = portrait

# Полноэкранный режим
fullscreen = 0

# Цвет presplash
android.presplash_color = #FFFFFF

# Разрешения Android
android.permissions = RECORD_AUDIO,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET

# API уровни
android.api = 33
android.minapi = 21
android.ndk_api = 21

# Архитектура
android.archs = arm64-v8a

# Bootstrap
p4a.bootstrap = sdl2

# Уровень логирования
log_level = 2

# Предупреждение при запуске от root
warn_on_root = 1

# Автоматическое принятие лицензий SDK
android.accept_sdk_license = True
