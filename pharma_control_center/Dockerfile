FROM odoo:18.0

USER root

RUN apt-get update && apt-get install -y wkhtmltopdf

RUN mkdir -p /mnt/extra-addons

COPY ./pharma_control_center /mnt/extra-addons/pharma_control_center

RUN chown -R odoo:odoo /mnt/extra-addons

USER odoo