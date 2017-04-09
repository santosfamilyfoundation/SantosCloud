#!/bin/bash

apidoc -f ".*\\.py$" apidoc -i app/handlers/ -o app/static/apidoc
