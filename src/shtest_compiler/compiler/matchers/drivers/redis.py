from string import Template

REDIS_TEMPLATE = Template("redis-cli $conn < $script")
