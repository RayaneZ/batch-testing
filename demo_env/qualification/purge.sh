#!/bin/bash

# Exemple de script de purge

RANDOM_CHOICE=$((RANDOM % 2))

if [ "$RANDOM_CHOICE" -eq 0 ]; then
  echo "Succès complet"
  exit 0
else
  echo "WARNING: Une légère anomalie a été détectée" >&2
  exit 0
fi
