import os

# Locals s s s
def get_locale_dict():
    lang = os.environ.get('LANG', '')
    if lang.startswith('ru'):
        return {
# russian locals
            "prep": "Подготовка накопителя...",
            "copy_base": "Копирование базовых файлов...",
            "copy_wim": "Прямое копирование WIM...",
            "split_wim": "Разделение WIM-образа...",
            "conv_lzx": "Конвертация в LZX (Solid архив)...",
            "sync": "Синхронизация ввода-вывода (sync)..."
        }
    return {
# english locals
        "prep": "Preparing drive...",
        "copy_base": "Copying base files...",
        "copy_wim": "Directly copying WIM...",
        "split_wim": "Splitting WIM image...",
        "conv_lzx": "Converting to LZX (Solid archive)...",
        "sync": "Syncing I/O (sync)..."
    }

def get_windows_script(iso_path, dev_path, scheme="gpt"):
    T = get_locale_dict()
    
    # schemes
    if scheme == "gpt":
        part_cmds = f"""
parted -s {dev_path} mklabel gpt
parted -s {dev_path} mkpart primary fat32 1MiB 100%
parted -s {dev_path} set 1 msftdata on
sleep 2
mkfs.vfat -F 32 -n "WINUSB" {dev_path}1
"""
    else:
        part_cmds = f"""
parted -s {dev_path} mklabel msdos
parted -s {dev_path} mkpart primary ntfs 1MiB 100%
parted -s {dev_path} set 1 boot on
sleep 2
mkfs.ntfs -f -L "WINUSB" {dev_path}1
"""

    script = f"""#!/bin/bash
set -e

echo "STATUS: {T['prep']}"
umount {dev_path}* 2>/dev/null || true
wipefs -a {dev_path}

# applying schemes
{part_cmds}

sleep 2
mkdir -p /tmp/w_iso /tmp/w_usb
mount -o loop,ro "{iso_path}" /tmp/w_iso
mount {dev_path}1 /tmp/w_usb

echo "STATUS: {T['copy_base']}"
# Copying
rsync -rlptD --no-owner --no-group --info=progress2 --exclude='sources/install.wim' --exclude='sources/install.esd' /tmp/w_iso/ /tmp/w_usb/

TF=""
[ -f "/tmp/w_iso/sources/install.wim" ] && TF="/tmp/w_iso/sources/install.wim"
[ -f "/tmp/w_iso/sources/install.esd" ] && TF="/tmp/w_iso/sources/install.esd"

if [ -n "$TF" ]; then
    FS=$(stat -c%s "$TF")
    
    # cuz of fat32 file size limit if we use MBR (NTFS) or file size < 4 GB, theeeeeen copying.
    if [ "$FS" -lt 4000000000 ] || [ "{scheme}" == "mbr" ]; then
        echo "STATUS: {T['copy_wim']}"
        cp "$TF" "/tmp/w_usb/sources/"
    else
        # if file > 4 GB and filesystem is FAT32 (GPT), then using wimlib
        echo "STATUS: {T['split_wim']}"
        set +e
        wimlib-imagex split "$TF" "/tmp/w_usb/sources/install.swm" 3800 2>&1
        RES=$?
        set -e
        
        # Code 68 I'm lazy
        if [ $RES -eq 68 ]; then
            echo "STATUS: {T['conv_lzx']}"
            rm -f /tmp/t.wim /tmp/w_usb/sources/install.swm 2>/dev/null || true
            wimlib-imagex export "$TF" all /tmp/t.wim --compress=maximum 2>&1
            
            echo "STATUS: {T['split_wim']}"
            wimlib-imagex split /tmp/t.wim "/tmp/w_usb/sources/install.swm" 3800 2>&1
            rm -f /tmp/t.wim
        elif [ $RES -ne 0 ]; then
            exit $RES
        fi
    fi
fi

echo "STATUS: {T['sync']}"
sync

umount /tmp/w_iso /tmp/w_usb 2>/dev/null || true
rmdir /tmp/w_iso /tmp/w_usb 2>/dev/null || true

echo "STATUS: DONE"
"""
    return script
