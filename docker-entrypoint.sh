#!/bin/bash
set -eo pipefail
shopt -s nullglob

# logging functions
flask_log() {
	local type="$1"; shift
	printf '%s [%s] [Entrypoint]: %s\n' "$(date --rfc-3339=seconds)" "$type" "$*"
}
flask_note() {
	flask_log Note "$@"
}
flask_warn() {
	flask_log Warn "$@" >&2
}
flask_error() {
	flask_log ERROR "$@" >&2
	exit 1
}

# usage: file_env VAR [DEFAULT]
#    ie: file_env 'XYZ_DB_PASSWORD' 'example'
# (will allow for "$XYZ_DB_PASSWORD_FILE" to fill in the value of
#  "$XYZ_DB_PASSWORD" from a file, especially for Docker's secrets feature)
file_env() {
	local var="$1"
	local fileVar="${var}_FILE"
	local def="${2:-}"
	if [ "${!var:-}" ] && [ "${!fileVar:-}" ]; then
		flask_error "Both $var and $fileVar are set (but are exclusive)"
	fi
	local val="$def"
	if [ "${!var:-}" ]; then
		val="${!var}"
	elif [ "${!fileVar:-}" ]; then
		val="$(< "${!fileVar}")"
	fi
	export "$var"="$val"
	unset "$fileVar"
}

# Loads various settings that are used elsewhere in the script
# This should be called after mysql_check_config, but before any other functions
docker_setup_env() {
	file_env 'FLASK_DB_SERVER' 'none'
	file_env 'FLASK_DB_NAME' 'none'
	file_env 'FLASK_DB_USER' 'none'
	file_env 'FLASK_DB_PASS' 'none'
	file_env 'FLASK_SERVER_PORT' '5000'
	file_env 'FLASK_APP' 'entrypoint:app'
	file_env 'FLASK_DEBUG' '0'
	file_env 'FLASK_APP_SETTINGS_MODULE' 'config.default'
	file_env 'FLASK_SECRET_KEY' `tr -dc A-Za-z0-9 </dev/urandom | head -c 64; echo`
}

_main() {
	# skip setup if they aren't running mysqld or want an option that stops mysqld
	docker_setup_env "$@"
	exec "$@"
}

# If we are sourced from elsewhere, don't perform any further actions
_main "$@"
