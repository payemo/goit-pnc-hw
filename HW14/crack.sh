#!/bin/bash

# Змінна для файлу захоплення
CAPTURE_FILE="crackme.pcap-01.cap"

# Попередній аналіз файлу і вибір першої мережі
echo "Аналіз захопленого файлу:"
BSSID=$(aircrack-ng $CAPTURE_FILE | grep -Eo "([0-9A-F]{2}:){5}[0-9A-F]{2}" | head -n 1)

if [ -z "$BSSID" ]; then
  echo "Не вдалося знайти жодної мережі в файлі $CAPTURE_FILE."
  exit 1
fi

echo "\nЗнайдена перша мережа: $BSSID"

# Запуск злому WEP
echo "\nЗапуск процесу злому WEP для BSSID $BSSID:"
aircrack-ng -b $BSSID $CAPTURE_FILE