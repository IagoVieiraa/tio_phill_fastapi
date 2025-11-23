#!/bin/bash
# activate-service.sh

service="$1"

if [ -f "./$service/.venv/bin/activate" ]; then
    source "./$service/.venv/bin/activate"
    echo -e "\e[32mAmbiente virtual do $service ativado!\e[0m"
else
    echo -e "\e[31mServiço $service não encontrado!\e[0m"
fi