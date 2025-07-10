from string import Template

POSTGRES_TEMPLATE = Template("psql $conn -f $script")
