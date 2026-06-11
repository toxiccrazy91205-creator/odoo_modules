#!/bin/bash
set -e

# 1. Start PostgreSQL
echo "Starting PostgreSQL..."
service postgresql start

# 2. Wait for PostgreSQL to be ready
until su - postgres -c "psql -c '\q'"; do
  echo "Waiting for postgres..."
  sleep 2
done

# 3. Create Odoo database user (superuser to allow DB creation via UI)
echo "Setting up Postgres roles..."
su - postgres -c "psql -tc \"SELECT 1 FROM pg_roles WHERE rolname='odoo'\" | grep -q 1 || createuser -s odoo"

echo "PostgreSQL is fully ready!"

# 4. Start Odoo as the 'odoo' user
# We don't use -i base because the database is local, meaning the standard Web UI Database Creation screen will work perfectly!
echo "Starting Odoo..."
su - odoo -c "odoo -c /etc/odoo/odoo.conf --http-port ${PORT:-8069}"
