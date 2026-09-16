#!/bin/bash
cd "$(dirname "$0")"
FILE="$(pwd)/gubre-uretimi-vaziyet-plani.drawio"

if [ ! -f "$FILE" ]; then
  echo "Dosya bulunamadı: gubre-uretimi-vaziyet-plani.drawio"
  read -r _
  exit 1
fi

if [ -d "/Applications/draw.io.app" ]; then
  open -a "draw.io" "$FILE"
elif [ -d "/Applications/diagrams.net.app" ]; then
  open -a "diagrams.net" "$FILE"
else
  open "$FILE"
fi
