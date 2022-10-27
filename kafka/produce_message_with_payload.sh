#!/bin/bash

set -e

main(){
    local payload=$(cat <<-EOF
            {
            	"specversion": "1.0",
            	"id": "0f1f33d1-d58b-459c-af2d-54914de647e2",
            	"source": "someExternalSource",
            	"type": "com.trimble.transportation.safety.vehicle-inspection.repaired.v1",
            	"datacontenttype": "application/json",
            	"data": {
            		"organizationId": "testorg",
            		"accountId": "f391f4ca-89ed-453e-b57f-8bc4c6df5ac4",
            		"reportNumber": 0,
            		"repairOrder": "Reference to repair order",
            		"repairCertification": {
            			"certifiedBy": {
            				"userId": "userIdString",
            				"userIdType": "trimble"
            			},
            			"certificationStatus": "REPAIRS_MADE",
            			"certificationDateTime": "2021-09-13T21:11:00Z"
            		},
            		"notes": [
            			{
            				"noteCreator": {
            					"userId": "userIdString",
            					"userIdType": "trimble"
            				},
            				"noteDateTime": "2021-09-13T21:11:00Z",
            				"note": "One of possibly many note entries."
            			}
            		]
            	}
            }
    EOF
)

    cat <<<  "$payload"
    # kafka-console-producer --producer.config /home/cflor/.kafka-tools/config --broker-list pkc-4k6zp.eastus2.azure.confluent.cloud:9092 --topic dev.trimble.transportation.safety.vehicle-repair.qry --property parse.key=true --property key.separator=, <<< "$payload"

}

main