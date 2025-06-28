from jinja2 import Template
from pathlib import Path

DOCS_DIR = Path("docs")
SHTEST_DIR = Path("demo_env")

MD_TEMPLATE = Template("""# 📄 Scénario de test : {{ scenario }}

**Fichier test** : `{{ shtest_file }}`  
**Script associé** : `{{ script_file }}`

""")
def generate_docs():
    shtest_files = list(SHTEST_DIR.glob("*.shtest"))
    nav_entries = []

    for shtest in shtest_files:
        scenario = shtest.stem
        script_file = f"{scenario}.sh"
        log_file = SHTEST_DIR / f"{scenario}.log"
        logs = log_file.read_text() if log_file.exists() else "Aucun log trouvé."

        content = MD_TEMPLATE.render(
            scenario=scenario,
            shtest_file=shtest.name,
            script_file=script_file,
            steps=[],
            logs=logs
        )

        md_path = DOCS_DIR / f"{scenario}.md"
        md_path.write_text(content)
        nav_entries.append(f"  - {scenario}: {scenario}.md")

    # Réécrire index.md avec navigation à jour
    index_path = DOCS_DIR / "index.md"
    with open(index_path, "w") as f:
        f.write("#Scénarios de test\n\n")
        for entry in nav_entries:
            label = entry.split(":")[0].split("-")[-1].strip()
            md = entry.split(":")[1].strip()
            f.write(f"- [{label}]({md})\n")

if __name__ == "__main__":
    generate_docs()