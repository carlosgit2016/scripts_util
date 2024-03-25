import csv
import click
import boto3
from enum import Enum

class ServiceType(Enum):
    EC2 = 'Amazon Elastic Compute Cloud - Compute'
    RDS = 'Amazon Relational Database Service'
    REDSHIFT = 'Amazon Redshift'
    ELASTICACHE = 'Amazon ElastiCache'
    ELASTISEARCH = 'Amazon Elasticsearch Service'
    OPENSEARCH = 'Amazon OpenSearch Service'
    MEMORYDB = 'Amazon MemoryDB Service'


def get_instance_detail(obj, type: ServiceType, prop: str):
    try:
        if type == ServiceType.EC2:
            return obj['InstanceDetails']['EC2InstanceDetails'].get(prop)
        if type == ServiceType.RDS:
            return obj['InstanceDetails']['RDSInstanceDetails'].get(prop)
        elif type == ServiceType.REDSHIFT:
            return obj['InstanceDetails']['RedshiftInstanceDetails'].get(prop)
        elif type == ServiceType.ELASTICACHE:
            return obj['InstanceDetails']['ElastiCacheInstanceDetails'].get(prop)
        elif type == ServiceType.ELASTISEARCH or type == ServiceType.OPENSEARCH:
            return obj['InstanceDetails']['ElasticsearchInstanceDetails'].get(prop)
        elif type == ServiceType.MEMORYDB:
            return obj['InstanceDetails']['MemoryDBInstanceDetails'].get(prop)
    except KeyError:
        print(f'Error finding key {prop} for {type.name}')

def service_type(value):
    try:
        return ServiceType[value.upper()]
    except KeyError:
        raise click.BadParameter(f'ServiceType must be {[member.name for member in ServiceType]}')

@click.command()
@click.option('--output-path', type=str, prompt='Output CSV file path', help='The path to the output CSV file.')
@click.option('--res-service-type', type=service_type, prompt=f'Service Type ({[member.name for member in ServiceType]})', help=f'Service types to check reservations. {[member.name for member in ServiceType]}')
@click.option('--term-in-years', type=click.Choice(['ONE_YEAR', 'THREE_YEARS']), prompt='Term in years', help='The reservation term in years.')
def get_reservation_recommendation(output_path, res_service_type: ServiceType, term_in_years):
    # Initialize the Cost Explorer client
    ce_client = boto3.client('ce')

    # Call the GetReservationPurchaseRecommendation API
    response = ce_client.get_reservation_purchase_recommendation(
        Service=res_service_type.value,  # Example service, modify as needed
        TermInYears=term_in_years,
        LookbackPeriodInDays='SIXTY_DAYS',  # Example lookback period, modify as needed
        PaymentOption='NO_UPFRONT',
        # Include additional parameters as needed
    )

    headers = [
        'RecommendationId',
        'ServiceType',
        'AccountScope',
        'LookbackPeriodInDays',
        'TermInYears',
        'PaymentOption',
        'AccountId',
        'Family',
        'InstanceType',
        'Region',
        'AvailabilityZone',
        'Platform',
        'Tenancy',
        'CurrentGeneration',
        'SizeFlexEligible',
        'DatabaseEngine',
        'DatabaseEdition',
        'DeploymentOption',
        'LicenseModel',
        'NodeType',
        'ProductDescription',
        'InstanceClass',
        'InstanceSize',
        'RecommendedNumberOfInstancesToPurchase',
        'RecommendedNormalizedUnitsToPurchase',
        'MinimumNumberOfInstancesUsedPerHour',
        'MinimumNormalizedUnitsUsedPerHour',
        'MaximumNumberOfInstancesUsedPerHour',
        'MaximumNormalizedUnitsUsedPerHour',
        'AverageNumberOfInstancesUsedPerHour',
        'AverageNormalizedUnitsUsedPerHour',
        'AverageUtilization',
        'EstimatedBreakEvenInMonths',
        'CurrencyCode',
        'EstimatedMonthlySavingsAmount',
        'EstimatedMonthlySavingsPercentage',
        'EstimatedMonthlyOnDemandCost',
        'EstimatedReservationCostForLookbackPeriod',
        'UpfrontCost',
        'RecurringStandardMonthlyCost',
        'TotalEstimatedMonthlySavingsAmount',
        'TotalEstimatedMonthlySavingsPercentage',
        'CurrencyCode'
    ]

    
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        recommendation_id = response['Metadata']['RecommendationId']
        writer.writeheader()
        for recommendation in response['Recommendations']:
            for detail in recommendation['RecommendationDetails']:
                row = {
                    'RecommendationId': recommendation_id,
                    'ServiceType': res_service_type.name,
                    'AccountScope': recommendation.get('AccountScope'),
                    'LookbackPeriodInDays': recommendation.get('LookbackPeriodInDays'),
                    'TermInYears': recommendation.get('TermInYears'),
                    'PaymentOption': recommendation.get('PaymentOption'),
                    'AccountId': detail.get('AccountId'),
                    'Family': get_instance_detail(detail, res_service_type, 'Family'),
                    'InstanceType': get_instance_detail(detail, res_service_type, 'InstanceType'),
                    'Region': get_instance_detail(detail, res_service_type, 'Region'),
                    'AvailabilityZone': get_instance_detail(detail, res_service_type, 'AvailabilityZone'),
                    'Platform': get_instance_detail(detail, res_service_type, 'Platform'),
                    'Tenancy': get_instance_detail(detail, res_service_type, 'Tenancy'),
                    'CurrentGeneration': get_instance_detail(detail, res_service_type, 'CurrentGeneration'),
                    'SizeFlexEligible': get_instance_detail(detail, res_service_type, 'SizeFlexEligible'),
                    'DatabaseEngine': get_instance_detail(detail, res_service_type, 'DatabaseEngine'),
                    'DatabaseEdition': get_instance_detail(detail, res_service_type, 'DatabaseEdition'),
                    'DeploymentOption': get_instance_detail(detail, res_service_type, 'DeploymentOption'),
                    'LicenseModel': get_instance_detail(detail, res_service_type, 'LicenseModel'),
                    'NodeType': get_instance_detail(detail, res_service_type, 'NodeType'),
                    'ProductDescription': get_instance_detail(detail, res_service_type, 'ProductDescription'),
                    'InstanceClass': get_instance_detail(detail, res_service_type, 'InstanceClass'),
                    'InstanceSize': get_instance_detail(detail, res_service_type, 'InstanceSize'),
                    'RecommendedNumberOfInstancesToPurchase': detail.get('RecommendedNumberOfInstancesToPurchase'),
                    'RecommendedNormalizedUnitsToPurchase': detail.get('RecommendedNormalizedUnitsToPurchase'),
                    'MinimumNumberOfInstancesUsedPerHour': detail.get('MinimumNumberOfInstancesUsedPerHour'),
                    'MinimumNormalizedUnitsUsedPerHour': detail.get('MinimumNormalizedUnitsUsedPerHour'),
                    'MaximumNumberOfInstancesUsedPerHour': detail.get('MaximumNumberOfInstancesUsedPerHour'),
                    'MaximumNormalizedUnitsUsedPerHour': detail.get('MaximumNormalizedUnitsUsedPerHour'),
                    'AverageNumberOfInstancesUsedPerHour': detail.get('AverageNumberOfInstancesUsedPerHour'),
                    'AverageNormalizedUnitsUsedPerHour': detail.get('AverageNormalizedUnitsUsedPerHour'),
                    'AverageUtilization': detail.get('AverageUtilization'),
                    'EstimatedBreakEvenInMonths': detail.get('EstimatedBreakEvenInMonths'),
                    'CurrencyCode': detail.get('CurrencyCode'),
                    'EstimatedMonthlySavingsAmount': detail.get('EstimatedMonthlySavingsAmount'),
                    'EstimatedMonthlySavingsPercentage': detail.get('EstimatedMonthlySavingsPercentage'),
                    'EstimatedMonthlyOnDemandCost': detail.get('EstimatedMonthlyOnDemandCost'),
                    'EstimatedReservationCostForLookbackPeriod': detail.get('EstimatedReservationCostForLookbackPeriod'),
                    'UpfrontCost': detail.get('UpfrontCost'),
                    'RecurringStandardMonthlyCost': detail.get('RecurringStandardMonthlyCost'),
                    'TotalEstimatedMonthlySavingsAmount': detail.get('TotalEstimatedMonthlySavingsAmount'),
                    'TotalEstimatedMonthlySavingsPercentage': detail.get('TotalEstimatedMonthlySavingsPercentage'),
                }

                writer.writerow(row)

if __name__ == '__main__':
    get_reservation_recommendation()
