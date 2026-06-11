FROM odoo:19.0

USER root

# Install PostgreSQL inside the container
RUN apt-get update && apt-get install -y postgresql postgresql-client && rm -rf /var/lib/apt/lists/*

# Copy Odoo Config
COPY ./odoo.conf /etc/odoo/odoo.conf

# Copy the custom startup script
COPY ./start.sh /start.sh
RUN chmod +x /start.sh

# Copy both custom modules into the addons folder
COPY ./boiler_costing_engine /mnt/extra-addons/boiler_costing_engine
COPY ./crm_inquiry_management /mnt/extra-addons/crm_inquiry_management

# Ensure correct permissions for the odoo user
RUN chown -R odoo:odoo /mnt/extra-addons /etc/odoo/odoo.conf

# The container MUST run as root initially to start the Postgres service. 
# The start.sh script will safely switch to the 'odoo' user before running Odoo.
USER root

# Define the start script as the entrypoint
ENTRYPOINT ["/start.sh"]
CMD []
