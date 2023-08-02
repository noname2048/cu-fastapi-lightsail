#!/usr/bin/bash

images=$(aws lightsail get-container-images  --service-name cu-container-service-1 | jq -r '.containerImages[] | .image')
images_to_delete=$(echo $images | tail -n +5)
for image in $images
do
    echo "delete $image"
    aws lightsail delete-container-image --service-name cu-container-service-1 --image $image
done
