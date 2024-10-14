#!/bin/bash

# Start the default Oracle entrypoint script in the background
/docker-entrypoint.sh &

# Wait for the Oracle database to be available
until sqlplus / as sysdba <<< "exit" &>/dev/null; do
  echo "Waiting for the database to be available..."
  sleep 5
done

# Now execute the SQL script to create the user
sqlplus / as sysdba @/docker-entrypoint-initdb.d/0_init.sql

# Wait for the background process to finish
wait
