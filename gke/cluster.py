oauthScopes = ["cloud-platform", "taskqueue", "bigquery", "sqlservice", "datastore", "pubsub", "servicecontrol",
               "cloud_debugger", "service.management", "userinfo.email", "compute", "devstorage.full_control",
               "sqlservice.admin", "logging.write", "monitoring", "trace.append", "bigtable.data", "bigtable.admin"]

def generate_config(context):
    type_name = context.properties['clustername'] + '-type'
    k8s_endpoints = {
        '': 'api/v1',
        '-apps': 'apis/apps/v1beta1',
        '-v1beta1-extensions': 'apis/extensions/v1beta1'
    }
    resources = [{
        "name": "gke-setup-" + context.properties['clustername'],
        "type": "container.v1.cluster",
        "properties": {
            "zone": context.properties['zone'],
            "cluster": {
                "name": context.properties['clustername'],
                "network": "$(ref." + context.properties['network'] + ".name)",
                "subnetwork": context.properties['subnetwork'],
                "addonsConfig": {
                    "httpLoadBalancing": {
                        "disabled": False
                    },
                    "horizontalPodAutoscaling": {
                        "disabled": False
                    },
                    "kubernetesDashboard": {
                        "disabled": False
                    },
                    "networkPolicyConfig": {
                        "disabled": False
                    },
                },
                "nodePools": [{
                    "name": "default-pool",
                    "config": {
                        "machineType": context.properties['machineType'],
                        "diskSizeGb": context.properties['machineDiskSize'],
                        "imageType": context.properties['gkeImageType'],
                        "preemptible": False,
                        "minCpuPlatform": "Intel Broadwell",
                        "oauthScopes":
                        [
                            'https://www.googleapis.com/auth/' + oauthscope
                            for oauthscope in oauthScopes
                        ],
                        "serviceAccount": context.properties['clustername'] + "@" + context.env['project']
                                          + ".iam.gserviceaccount.com"
                    },
                    "initialNodeCount": context.properties['initialNodeCount'],
                    "version": context.properties['clusterVersion'],
                    "autoscaling": {
                        "enabled": True,
                        "minNodeCount": context.properties['initialNodeCount'],
                        "maxNodeCount": context.properties['maxNodeCount']
                    },
                    "management": {
                        "autoUpgrade": True,
                        "autoRepair": True
                    }
                }],
                "locations": [
                    context.properties['zone']
                ],
                "enableKubernetesAlpha": False,
                "legacyAbac": {
                    "enabled": False
                },
                "ipAllocationPolicy": {
                    "useIpAliases": True,
                    "createSubnetwork": False,
                    "clusterIpv4CidrBlock": context.properties['clusterIPv4CidrBlock'],
                    "servicesIpv4CidrBlock": context.properties['servicesIPv4CidrBlock']
                },
                "maintenancePolicy": {
                    "window": {
                        "dailyMaintenanceWindow": {
                            "startTime": "01:00"
                        }
                    }
                },
                "initialClusterVersion": context.properties['clusterVersion'],
                "currentMasterVersion": context.properties['clusterVersion']
            }
        }
    }, {
        "name": "vpc-" + context.properties['clustername'],
        "type": "compute.v1.network",
        "properties": {
            "name": "vpc-" + context.properties['clustername'],
            "autoCreateSubnetworks": False
        }
    }]
    for type_suffix, endpoint in k8s_endpoints.iteritems():
        resources.append({
            'name': type_name + type_suffix,
            'type': 'deploymentmanager.v2beta.typeProvider',
            'properties': {
                'options': {
                    'validationOptions': {
                           'schemaValidation': 'IGNORE_WITH_WARNINGS'
                    },
                    'inputMappings': [{
                        'fieldName': 'name',
                        'location': 'PATH',
                        'methodMatch': '^(GET|DELETE|PUT)$',
                        'value': '$.ifNull('
                                 '$.resource.properties.metadata.name, '
                                 '$.resource.name)'
                    }, {
                        'fieldName': 'metadata.name',
                        'location': 'BODY',
                        'methodMatch': '^(PUT|POST)$',
                        'value': '$.ifNull('
                                 '$.resource.properties.metadata.name, '
                                 '$.resource.name)'
                    }, {
                        'fieldName': 'Authorization',
                        'location': 'HEADER',
                        'value': '$.concat("Bearer ",'
                                 '$.googleOauth2AccessToken())'
                    }]
                },
                'descriptorUrl':
                    ''.join([
                        'https://$(ref.gke-setup-', context.properties['clustername'], '.endpoint)/swaggerapi/',
                        endpoint
                    ])
            }
        })
    outputs = [{
        "name": "selfLink",
        "value": "$(ref.gke-setup-" + context.properties['clustername'] + ".selfLink)"
    }, {
        "name": "Zone",
        "value": "$(ref.gke-setup-" + context.properties['clustername'] + ".zone)"
    }, {
        "name": "endpoint",
        "value": "$(ref.gke-setup-" + context.properties['clustername'] + ".endpoint)"
    }, {
        "name": "currentMasterVersion",
        "value": "$(ref.gke-setup-" + context.properties['clustername'] + ".currentMasterVersion)"
    }, {
        "name": "currentNodeVersion",
        "value": "$(ref.gke-setup-" + context.properties['clustername'] + ".currentNodeVersion)"
    }, {
        "name": "status",
        "value": "$(ref.gke-setup-" + context.properties['clustername'] + ".status)"
    }, {
        "name": "servicesIpv4Cidr",
        "value": "$(ref.gke-setup-" + context.properties['clustername'] + ".servicesIpv4Cidr)"
    }, {
        "name": "currentNodeCount",
        "value": "$(ref.gke-setup-" + context.properties['clustername'] + ".currentNodeCount)"
    }]

    return {'resources': resources, 'outputs': outputs}
