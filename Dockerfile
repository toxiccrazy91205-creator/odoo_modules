FROM odoo:19.0

USER root

USER odoo

COPY ./boiler_costing_engine /mnt/extra-addons/boiler_costing_engine
COPY ./odoo.conf /etc/odoo/odoo.conf

# Override the official entrypoint so it doesn't force the DB port to match Render's web PORT
ENTRYPOINT []
# FREE TIER HACK: Initialize the DB and intentionally stop the server.
CMD odoo -c /etc/odoo/odoo.conf --db_host "$PGHOST" --db_port "$PGPORT" --db_user "$PGUSER" --db_password "${PGPASSWORD:-$PASSWORD}" --http-port "${PORT:-8069}"
