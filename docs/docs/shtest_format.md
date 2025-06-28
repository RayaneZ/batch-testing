# Construire des fichiers `.shtest`

Ce document décrit la syntaxe utilisée pour écrire les scénarios au format `.shtest`.
Chaque ligne suit la forme **Action : ... ; Résultat : ...**. Les validations sont ensuite compilées
pour générer les scripts shell correspondants.

## Exemple de base
```text
Action: lancer le script test.sh ; Resultat: retour 0
```
Ce couple d'Action/Résultat déclenche l'exécution de `test.sh` puis vérifie que le
script se termine avec un code de retour `0`.

## Alias supportés
Certaines tournures sont automatiquement converties en validations connues :
- `le script retourne un code N` → `retour N`
- `la sortie standard contient TEXTE` → `stdout contient TEXTE`
- `la sortie d'erreur est TEXTE` → `stderr=TEXTE`
- `les identifiants sont configurés` → `identifiants configurés`
- `le dossier est créé` → `dossier créé`

Combinez plusieurs validations avec `et` ou `ou`. Les expressions non reconnues
sont conservées telles quelles.

## Manipulations SQL
Vous pouvez préparer ou vérifier une base de données en exécutant un script SQL :
```text
Action: Exécuter le script SQL init_bdd.sql ; Résultat: base prête.
```
Les scripts sont appelés en utilisant la variable `SQL_CONN` de votre environnement.
Définissez-la dans le scénario si nécessaire :
```text
Action: Définir la variable SQL_CONN = user/password@db ; Résultat: identifiants configurés.
```

## Manipulation de fichiers
Créez, copiez ou mettez à jour des fichiers en décrivant simplement l'opération :
```text
Action: créer le fichier /tmp/test.txt avec les droits 0600 ; Résultat: Le fichier est présent.
Action: copier le fichier /tmp/a.txt vers /tmp/b.txt ; Résultat: le fichier est copié.
```
Vous pouvez également vérifier qu'un fichier est identique à une référence avec
`fichier_identique A B` ou purger un dossier avant les tests.

## Exécution de batchs
Pour lancer un traitement, indiquez le script à exécuter :
```text
Action: exécuter traitement.sh ; Résultat: retour 0.
```
Le moteur exécute le fichier avec les arguments déclarés plus haut puis applique
les validations indiquées.
