.DEFAULT_GOAL := default

.PHONY: gen

default:
	echo "Please use 'make help' to see available commands"

gen:
	datamodel-codegen --input openapi.yaml --input-file-type openapi --output schemas.py