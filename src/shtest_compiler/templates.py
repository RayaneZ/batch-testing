from string import Template

TEMPLATES = {
    "grep_log": Template("grep 'ERROR' ${path}"),
    # The SQL connection can be overridden via the SQL_CONN environment variable.
    # The default connection uses sqlplus with hardcoded credentials.
    "execute_sql": Template(
        "sqlplus -S ${conn} <<'EOF'\nWHENEVER SQLERROR EXIT 1;\n@${script}\nEOF"
    ),
    "create_dir": Template("mkdir -p ${path} && chmod ${mode} ${path}"),
    "create_file": Template("touch ${path} && chmod ${mode} ${path}"),
    "update_file": Template("touch ${path}"),
    "touch_ts": Template("touch -t ${ts} ${path}"),
    "cat_file": Template("cat ${file}"),
    "copy_file": Template("cp ${src} ${dest}"),
    "copy_dir": Template("cp -r ${src} ${dest}"),
    "move": Template("mv ${src} ${dest}"),
    "purge_dir": Template("rm -rf ${path}/* && mkdir -p ${path}"),
}
