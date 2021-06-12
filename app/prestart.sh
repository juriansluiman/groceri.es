#! /usr/bin/env bash

echo "Run flask migration upgrades (show current version first)"
mkdir -p db/
flask db current
flask db upgrade

echo "Compile translation files"
flask translate compile
