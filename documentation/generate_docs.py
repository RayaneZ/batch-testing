
import pandas as pd
from jinja2 import Template
from pathlib import Path

DOCS_DIR = Path("docs")
SUMMARY_FILE = Path("../demo_env/tests_summary.xlsx")

MD_TEMPLATE = Template("""# 📄 Scénario de test : {{ scenario }}

**Fichier test** : `{{ shtest_file }}`  
**Script associé** : `{{ script_file }}`

## 🧩 Étapes du scénario

| Étape        | Action | Résultat attendu |
|--------------|--------|------------------|
{% for step, action, result in steps %}
| {{ step }} | {{ action }} | {{ result }} |
{% endfor %}

## 📄 Logs (si disponibles)

```
{{ logs }}
```
""")

def generate_docs():
    xls = pd.read_excel(SUMMARY_FILE, sheet_name=None)
    nav_entries = []

    for sheet, df in xls.items():
        steps = list(zip(df['Step'], df['Actions'], df['Actual Results']))
        log_file = Path(f"demo_env/{sheet}.log")
        logs = log_file.read_text() if log_file.exists() else "Aucun log trouvé."

        content = MD_TEMPLATE.render(
            scenario=sheet,
            shtest_file=f"{sheet}.shtest",
            script_file=f"{sheet}.sh",
            steps=steps,
            logs=logs
        )

        md_path = DOCS_DIR / f"{sheet}.md"
        md_path.write_text(content)
        nav_entries.append(f"  - {sheet}: {sheet}.md")

    # Réécrire index.md avec navigation à jour
    with open(DOCS_DIR / "index.md", "w") as f:
        f.write("# 📚 Scénarios de test\n\n")
        for entry in nav_entries:
            label = entry.split(":")[0].split("-")[-1].strip()
            md = entry.split(":")[1].strip()
            f.write(f"- [{label}]({md})\n")

if __name__ == "__main__":
    generate_docs()
