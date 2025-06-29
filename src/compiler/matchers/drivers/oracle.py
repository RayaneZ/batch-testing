from string import Template

ORACLE_TEMPLATE = Template("sqlplus -S $conn <<'EOF'\nWHENEVER SQLERROR EXIT 1;\n@$script\nEOF")
