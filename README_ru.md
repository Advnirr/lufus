# Lufus

<img src="lufus.svg" align="right" width="180" alt="Lufus Logo">

**[English](README.md) | Русский**

Минималистичный, универсальный и функциональный инструмент с графическим интерфейсом для создания загрузочных устройств на ОС Linux. Поддерживает как образы ISOHybrid, так и образы Windows. Основано на Python, GTK4, и Libadwaita.

<p align="left">
  <a href="https://github.com/Advnirr/lufus/releases">
    <img src="https://img.shields.io/github/v/release/Advnirr/lufus?style=flat-square&color=007EC6" alt="Release">
  </a>
  <a href="https://github.com/Advnirr/lufus/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Advnirr/lufus?style=flat-square&color=FF5722" alt="License">
  </a>
</p>

---

## ⚙️ Возможности

* **Поддержка Windows:** Автоматически определяет Windows ISO и применяет корректную схему разметки (GPT/FAT32 для UEFI, или MBR/NTFS для Legacy BIOS).
* **Обработка больших WIM-файлов:** Автоматически обнаруживает непрерывные `.esd` архивы и `.wim` файлы размером более 4ГБ, разделяя или преобразуя их на лету для обхода ограничений FAT32.
* **Поддержка Linux / Isohybrid:** Использует прямое побитовое копирование блоков с помощью команды `dd` для гарантированной загрузки дистрибутивов Linux.
* **Нативность:** Интерфейс GTK4/Adwaita.

## 📦 Зависимости

Для запуска Lufus, вам потребуются следующие системные пакеты:
`python-gobject`, `gtk4`, `libadwaita`, `wimlib` (для wimlib-imagex), `rsync`, `parted`, `polkit` (для pkexec), `libarchive` (для bsdtar).

## 🚀 Установка

### Arch Linux / CachyOS (Рекомендовано)
Поскольку Lufus предоставляет `PKGBUILD`, установка на Arch и его производных дистрибутивах (CachyOS, EndeavourOS, т.п) следующая:
```bash
git clone https://github.com/Advnirr/lufus.git
cd lufus
makepkg -si
```

### Ручной запуск (Любой дистрибутив)
Вы можете запустить Lufus прямо из исходного кода без установки:
```bash
git clone https://github.com/Advnirr/lufus.git
cd lufus
python main.py
```

## Лицензия
Проект лицензирован GNU General Public License v3.0 (GPL-3.0). Ознакомьтесь с [LICENSE](LICENSE) для получения дополнительной информации.
