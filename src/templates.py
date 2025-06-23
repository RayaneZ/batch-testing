from string import Template

TEMPLATES = {
    "grep_log": Template("grep 'ERROR' ${path}"),
    "execute_sql": Template("sqlplus -S user/password@db @${script}"),
    "create_dir": Template("mkdir -p ${path} && chmod ${mode} ${path}"),
    "create_file": Template("touch ${path} && chmod ${mode} ${path}"),
    "update_file": Template("touch ${path}"),
    "touch_ts": Template("touch -t ${ts} ${path}"),
    "cat_file": Template("cat ${file}"),
    "copy_file": Template("cp ${src} ${dest}"),
    "copy_dir": Template("cp -r ${src} ${dest}"),
    "move": Template("mv ${src} ${dest}"),
}

