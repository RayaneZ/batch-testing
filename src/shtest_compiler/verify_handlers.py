import os
import yaml

YAML_PATH = os.path.join(
    os.path.dirname(__file__), "config", "patterns_validations.yml"
)
PLUGINS_DIR = os.path.join(os.path.dirname(__file__), "plugins")
CORE_HANDLERS_DIR = os.path.join(os.path.dirname(__file__), "core", "handlers")


def main():
    with open(YAML_PATH, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    handlers = set(entry["handler"] for entry in data["validations"])
    plugin_files = set(
        f[:-3]
        for f in os.listdir(PLUGINS_DIR)
        if f.endswith(".py") and not f.startswith("__")
    )
    core_files = set(
        f[:-3]
        for f in os.listdir(CORE_HANDLERS_DIR)
        if f.endswith(".py") and not f.startswith("__")
    )

    print("--- Handler Coverage Report ---")
    for handler in sorted(handlers):
        plugin_exists = handler in plugin_files
        core_exists = handler in core_files
        status = []
        if not plugin_exists:
            status.append("MISSING PLUGIN")
        if not core_exists:
            status.append("MISSING CORE HANDLER")
        if not status:
            status.append("OK")
        print(
            f"{handler:25} | Plugin: {'Y' if plugin_exists else 'N'} | Core: {'Y' if core_exists else 'N'} | {'; '.join(status)}"
        )

    print("\n--- Alias/Opposite Symmetry Report ---")
    for entry in data["validations"]:
        phrase = entry.get("phrase")
        aliases = entry.get("aliases", [])
        opposite = entry.get("opposite", {})
        opp_phrase = opposite.get("phrase") if isinstance(opposite, dict) else None
        opp_aliases = opposite.get("aliases", []) if isinstance(opposite, dict) else []
        if opp_phrase:
            # Try to find the opposite entry in the YAML
            opp_entry = next(
                (e for e in data["validations"] if e.get("phrase") == opp_phrase), None
            )
            if opp_entry:
                opp_aliases = opp_entry.get("aliases", [])
            # Compare alias counts
            if not opp_aliases:
                print(
                    f"[WARN] Opposite for '{phrase}' ('{opp_phrase}') has NO aliases."
                )
            elif abs(len(aliases) - len(opp_aliases)) > max(
                2, 0.5 * max(len(aliases), 1)
            ):
                print(
                    f"[WARN] Alias count mismatch: '{phrase}' ({len(aliases)}) vs opposite '{opp_phrase}' ({len(opp_aliases)})"
                )
    print("Alias/opposite symmetry check complete.")


if __name__ == "__main__":
    main()
