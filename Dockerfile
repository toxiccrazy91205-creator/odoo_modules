FROM odoo:19.0

USER root
# Install any extra packages if needed here
# RUN apt-get update && apt-get install -y ...

USER odoo

# Copy your custom module into the Docker image's addons folder
COPY ./boiler_costing_engine /mnt/extra-addons/boiler_costing_engine

# Copy the custom configuration file
COPY ./odoo.conf /etc/odoo/odoo.conf
