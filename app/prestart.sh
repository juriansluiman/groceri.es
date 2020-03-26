#! /usr/bin/env bash

echo "Run flask migration upgrades (show current version first)"
flask db current
flask db upgrade