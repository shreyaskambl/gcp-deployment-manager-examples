#!/bin/bash

sed -i -e "s/ACCOUNT_NAME/${CLUSTER_NAME}/g" userlist_developers.txt

gcloud container clusters get-credentials ${CLUSTER_NAME} --zone ${COMPUTE_ZONE} --project ${GOOGLE_PROJECT_NAME}

cat userlist_developers.txt

while read line
do
  echo "####User is $line"
  echo "----"
  USERNAME=$(echo $line | awk -F "@" '{print $1}' | tr 'A-Z' 'a-z')
  CLUSTEREMAIL=$(echo $line | tr 'A-Z' 'a-z')
  cat Developer_rolebinding_template | sed "s/USERNAME/$USERNAME/g" | sed "s/CLUSTEREMAIL/$CLUSTEREMAIL/g" | kubectl apply -f  -
  echo ""
done <  userlist_developers.txt

kubectl apply -f serviceaccount-default-rbac.yaml
