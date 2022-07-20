#!/bin/bash

kubectl delete deploy serverless-redis

kubectl delete configmap pyfile

kubectl delete configmap outputkey