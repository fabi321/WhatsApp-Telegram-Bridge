#! /bin/bash
# Run with $1: full folder path; $2: filename; $3: full config
# execute remotely using "cat copy.sh | ssh host 'bash -s $1 $2 $3' < file_to_copy"

if [ ! -d "$1" ]; then
  mkdir "$1"
fi

HTACCESS="${1}/.htaccess"

if [ "$(cat "$HTACCESS")" != "$3" ]; then
  echo "$3" > "$HTACCESS"
fi

cat /dev/stdin > "${1}/${2}"
