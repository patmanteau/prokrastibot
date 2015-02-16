#!/bin/bash
URL='http://localhost:8000/ping'
HEADER='Content-Type: application/json'

# Usage: send_message(name, text, header, url)
function send_message {
	echo "name: $1 text: $2 (header:$3 url: $4)"
	curl -X POST -d "{\"name\": \"$1\", \"text\": \"$2\"}" -H "'$3'" "$4"
}

send_message "Johnny Five" "kann ich nicht" "$HEADER" "$URL"
send_message "Johnny Five" "prokrastibot" "$HEADER" "$URL"
send_message "Johnny Five" "!meme batman_slapping_robin|stop acting|like a chicken!" "$HEADER" "$URL"
send_message "Johnny Five" "!memelist" "$HEADER" "$URL"
send_message "Johnny Five" "!help" "$HEADER" "$URL"
send_message "Johnny Five" "y u no shut up" "$HEADER" "$URL"
send_message "Johnny Five" "awesome!" "$HEADER" "$URL"
