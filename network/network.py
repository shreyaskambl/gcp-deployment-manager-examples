def generate_config(context):
    resources = [{
        "name": context.properties['vpcNetwork'],
        "type": "compute.v1.network",
        "properties": {
            "name": "vpc-" + context.properties['vpcNetwork'],
            "autoCreateSubnetworks": False
        }
    }]

    return {'resources': resources}
