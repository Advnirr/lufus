import os

# Locals, idk
def get_locale_dict():
    lang = os.environ.get('LANG', '')
    if lang.startswith('ru'):
        return {
# russian locals
            "unmount": "Отмонтирование...",
            "copy": "Копирование образа (dd)...",
            "sync": "Синхронизация ввода-вывода (sync)...",
        }
    return {
# english locals
        "unmount": "Unmounting...",
        "copy": "Copying image (dd)...",
        "sync": "Syncing I/O (sync)...",
    }

def get_linux_script(iso_path, dev_path):
    T = get_locale_dict()
    
    script = f"""#!/bin/bash
set -e

# ISO size in bytes
SIZE=$(stat -c%s "{iso_path}")

echo "STATUS: {T['unmount']}"
umount {dev_path}* 2>/dev/null || true
wipefs -a {dev_path}

echo "STATUS: {T['copy']}"
# Progress parsing
dd if="{iso_path}" of="{dev_path}" bs=4M status=progress 2>&1 | tr '\\r' '\\n' | while read -r line; do
    if [[ $line == *" bytes "* ]]; then
        BYTES=$(echo $line | awk '{{print $1}}')
        PCT=$(awk -v b="$BYTES" -v s="$SIZE" 'BEGIN {{printf "%.1f", (b/s)*100}}')
        echo "${{PCT}}%"
    fi
done

echo "STATUS: {T['sync']}"
sync

echo "STATUS: DONE"
"""
    return script
