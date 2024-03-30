#!/bin/bash

docker build . -t airbyte/source-instagram:dev
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 716702562035.dkr.ecr.us-west-2.amazonaws.com
docker tag airbyte/source-instagram:dev 716702562035.dkr.ecr.us-west-2.amazonaws.com/airbyte_instagram:dev
docker push 716702562035.dkr.ecr.us-west-2.amazonaws.com/airbyte_instagram:dev