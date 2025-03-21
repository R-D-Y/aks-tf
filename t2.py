#!/bin/bash

total=0

for org in $(cf orgs | tail -n +4); do
  cf target -o "$org" > /dev/null
  for space in $(cf spaces | tail -n +4); do
    cf target -o "$org" -s "$space" > /dev/null

    # Récupère toutes les lignes contenant "rabbitmq" dans la colonne OFFERING
    count=$(cf services | awk 'NR>3 && tolower($2) ~ /rabbitmq/ {count++} END {print count+0}')
    
    echo "[$org / $space] : $count RabbitMQ"
    total=$((total + count))
  done
done

echo "Total RabbitMQ services: $total"