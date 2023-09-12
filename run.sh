#!/bin/bash

set -e

SCRIPT_DIR=$(cd $(dirname $0) ; pwd -P)

TASK=$1
ARGS=${@:2}

chain_name_for_project_id() {
  case $chain_name in
  "alles-1")
		echo "alles-playground";;
	"osmosis-test-5")
		echo "alles-playground";;
  "phoenix-1")
    echo "celatone-production";;
  "pisco-1")
    echo "celatone-production";;
  esac
}

help__fmt="format terraform files"
task__fmt() {
  terraform fmt -recursive
}

help__plan="plan terraform files -- params: environment"
task__plan() {
  local environment=$1

  if [ -z "${environment}" ] ; then
    echo "Requires environment"
    exit 1
  fi

  terraform init
  terraform workspace select $environment || terraform workspace new $environment
  terraform plan -var-file=$environment.tfvars
}

task__build_and_push_image() {
  docker build -t celatone/api:latest .
	docker tag celatone/api:latest asia-southeast1-docker.pkg.dev/alles-share/shared-docker-images/celatone/api:latest
	docker push asia-southeast1-docker.pkg.dev/alles-share/shared-docker-images/celatone/api:latest

  echo "asia-southeast1-docker.pkg.dev/alles-share/shared-docker-images/celatone/api:latest"
}

help__apply="apply terraform files -- params: environment"
task__apply() {
  local environment=$1
  local image_url=$2

  if [ -z "${environment}" ] ; then
    echo "Requires environment"
    exit 1
  fi

  if [ -z "${image_url}" ] ; then
    echo "Requires image_url"
    exit 1
  fi

  cd infrastructure

  terraform init
  terraform workspace select $environment || terraform workspace new $environment
  terraform apply -var-file=$environment.tfvars -var="image_url=$image_url"
}

help__destroy="destroy terraform files -- params: environment"
task__destroy() {
  local environment=$1

  if [ -z "${environment}" ] ; then
    echo "Requires environment"
    exit 1
  fi
}

list_all_helps() {
  compgen -v | egrep "^help__.*" 
}

NEW_LINE=$'\n'
if type -t "task__$TASK" &>/dev/null; then
  task__$TASK $ARGS
else
  echo "usage: $0 <task> [<..args>]"
  echo "task:"

  HELPS=""
  for help in $(list_all_helps)
  do

    HELPS="$HELPS    ${help/help__/} |-- ${!help}$NEW_LINE"
  done

  echo "$HELPS" | column -t -s "|"
  exit
fi
