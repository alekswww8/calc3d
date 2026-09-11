[app]
# Название вашего приложения (будет отображаться на телефоне)
title = Calc3D

# Имя пакета
package.name = calc3d

# Домен пакета
package.domain = org.alekswww8

# Где искать исходный код (точка означает текущую папку)
source.dir = .

# Какие файлы включать в сборку
source.include_exts = py,png,jpg,kv,atlas

# Версия приложения
version = 0.1

# Библиотеки Python, которые использует ваш код
requirements = python3,kivy

# Ориентация экрана (portrait - вертикально, landscape - горизонтально)
orientation = portrait

# Архитектуры процессоров Android
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
# Уровень детализации логов
log_level = 2
warn_on_root = 1
