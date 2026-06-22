[app]
title = TckEscape
package.name = tckescape
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Требования (зависимости) приложения
requirements = python3,kivy

orientation = portrait
fullscreen = 1

# Настройки Android
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
