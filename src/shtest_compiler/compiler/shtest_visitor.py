from parser.shtest_ast import Action, ShtestFile, TestStep

from compiler.compiler import CompileContext
from compiler.visitors import CompilerVisitor


def compile_shtest_file(ast: ShtestFile, verbose: bool = False) -> list[str]:
    lines = [
        "#!/bin/sh",
        "set -e",
        "",
        "run_cmd() {",
        "  local _stdout=$(mktemp)",
        "  local _stderr=$(mktemp)",
        '  /bin/sh -c "$1" >"$_stdout" 2>"$_stderr"',
        "  last_ret=$?",
        '  last_stdout=$(cat "$_stdout")',
        '  last_stderr=$(cat "$_stderr")',
        '  rm -f "$_stdout" "$_stderr"',
        "  if [ $last_ret -ne 0 ]; then",
        '    echo "STDERR: $last_stderr"',
        "  fi",
        "}",
        "",
        "log_diff() {",
        '  expected="$1"',
        '  actual="$2"',
        '  if [ "$expected" != "$actual" ]; then',
        "    echo 'Différence détectée :'",
        '    echo "- Attendu : $expected"',
        '    echo "- Obtenu : $actual"',
        "  fi",
        "}",
        "",
    ]
    context = CompileContext(counter=[0], last_file_var=[None], verbose=verbose)
    visitor = CompilerVisitor(context)
    print("Passage dans SHTEST_VISITOR")
    for step in ast.steps:
        lines.append(f"# ---- {step.name} ----")
        for action in step.actions:
            lines.append(f'run_cmd "{action.command}"')
            if action.result_ast:
                shell_lines, _ = action.result_ast.accept(visitor)
                lines.extend(shell_lines)

    return lines
