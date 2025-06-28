
# 🎨 Guide de style – Composants disponibles

Cette page montre comment utiliser les éléments de mise en forme et d’interaction disponibles dans votre documentation MkDocs.

---

## ✅ Alertes

!!! success "Test passé"
    Tous les fichiers ont été générés avec succès.

!!! warning "Attention"
    Une valeur inattendue a été détectée.

!!! failure "Échec"
    Le fichier `output.csv` est manquant.

---

## 💬 Code avec surlignage (monokai)

```bash
#!/bin/bash
echo "Traitement en cours..."
./batch_runner.sh input.csv > result.log
```

```python
def test_execution():
    assert run_job("input.csv") == "SUCCESS"
```

---

## 📂 Détails dépliables

<details>
<summary><strong>Voir le contenu du log</strong></summary>

```log
[INFO] Start job
[OK] Input loaded
[WARN] Delay detected
```

</details>

---

## 📎 Aperçu de documents en popup (PDF, HTML...)

<a class="popup-link" href="assets/example_log.pdf">📎 Voir le rapport PDF</a>

---

## 🧪 Tableau de statut

| Scénario        | Résultat | Durée |
|-----------------|----------|-------|
| bdd_example     | ✅ OK    | 5s    |
| demo_long_test  | ❌ Échec | 12s   |

---

## 🎯 Bouton retour en haut

Cliquez sur le coin inférieur droit pour revenir en haut de page.
