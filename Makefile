SHELL := /bin/bash

default: oas_document

.PHONY: test

oas_document: bts/static/api/v0/openapi-schema.json

bts/static/api/v0/openapi-schema.json: bts/urls.py bts/views.py bts/serializers.py bts/models.py
	./manage.py generateschema --file bts/static/api/v0/openapi-schema.json --api_version 0.0.1 --title "Bauteilsortiment API"

test:
	./manage.py test

