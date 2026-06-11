FROM odoo:19.0

USER root

USER odoo

COPY ./boiler_costing_engine /mnt/extra-addons/boiler_costing_engine
COPY ./odoo.conf /etc/odoo/odoo.conf

# Override the official entrypoint so it doesn't force the DB port to match Render's web PORT
ENTRYPOINT ["odoo"]
# Automatically initialize the default 'postgres' database on startup to bypass the Web UI creation screen
CMD ["-c", "/etc/odoo/odoo.conf", "-d", "postgres", "-i", "base"]
