#!/bin/bash

images=($(cat images.txt)) # File with images
contexts=($(kubectl config get-contexts | grep "arn:aws:eks:us-east-1" | awk '{ print $2 }' | tail +2)) # Add your contexts here
for image in "${images[@]}"; do

    image_found=""
    clusters=""
    for context in "${contexts[@]}"; do
        kubectl config use-context "$context" > /dev/null # Silecing context switch

        pods_using_image=$(kubectl get pods --all-namespaces -o=jsonpath='{range .items[*]}{"\n"}{.metadata.name}{":\t"}{range .spec.containers[*]}{.image}{", "}{end}{end}' | grep "$image")

        if [ -z "$pods_using_image" ]; then
            continue
        else
            image_found="yes"
            clusters+="$context"
        fi
    done
    echo "$image|$image_found|$clusters"
done
