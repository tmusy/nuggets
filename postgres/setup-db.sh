#!/bin/bash

if [ -n "${DB_USER}" ]; then
  if [ -z "${DB_PASS}" ]; then
    echo ""
    echo "WARNING: "
    echo "  Please specify a password for \"${DB_USER}\". Skipping user creation..."
    echo ""
    DB_USER=
  else
    echo "Creating user \"${DB_USER}\"..."
    echo "CREATE ROLE ${DB_USER} with LOGIN CREATEDB PASSWORD '${DB_PASS}';" |
      gosu postgres psql >/dev/null
  fi
fi

if [ -n "${DB_NAME}" ]; then
  for db in $(awk -F',' '{for (i = 1 ; i <= NF ; i++) print $i}' <<< "${DB_NAME}"); do
    echo "Creating database \"${db}\"..."
    echo "CREATE DATABASE ${db};" | \
      gosu postgres psql >/dev/null

    if [ -n "${DB_USER}" ]; then
      echo "Granting access to database \"${db}\" for user \"${DB_USER}\"..."
      echo "GRANT ALL PRIVILEGES ON DATABASE ${db} to ${DB_USER};" |
        gosu postgres psql >/dev/null
    fi
  done
fi
