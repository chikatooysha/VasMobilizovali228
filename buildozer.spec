[app]
title = TckEscape
package.name = tckescape
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Зависимости приложения
requirements = python3,kivy==2.3.0,pillow

orientation = portrait
fullscreen = 1

# Настройки Android SDK/API
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Автоматически принимать лицензии SDK внутри buildozer
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
