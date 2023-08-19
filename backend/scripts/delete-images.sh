#!/bin/bash

aws lightsail get-container-images  \
    --profile lightsail \
    --service-name cu-container-service-1 \
    | jq -r '.containerImages[] | .image' \
    | tail -n +5
    > images.txt
images=$(cat images.txt)
# tail 은 echo 를 통해 pipeline 으로 넘겨줄 때,
# -n +5 옵션이 제대로 작동하지 않음
for image in $images
do
    echo "delete $image"
    # aws lightsail delete-container-image --service-name cu-container-service-1 --image $image
done

wc -l images.txt | awk '{print $1}' > count.txt
