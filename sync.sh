#!/bin/sh

httrack http://microformats.org/wiki/microformats2 \
  -O Microformats2.docset/Contents/Resources/Documents,cache -I0 \
  --display=2 --timeout=60 --retries=99 --sockets=7 \
  --connection-per-second=5 --max-rate=250000 \
  --keep-alive --depth=4 --mirror --robots=0 \
  --user-agent '$(httrack --version); dash-microformats2 ()' \
  "-*" "+http://microformats.org/wiki/h-*" "-http://microformats.org/wiki/h-*-feedback*" "-http://microformats.org/wiki/h-*-brainstorming*" "+http://microformats.org/wiki/skins/**.css" "+http://microformats.org/wiki/skins/**.gif" "+http://microformats.org/wiki/skins/**.png"
