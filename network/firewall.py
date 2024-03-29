def get_network(properties):
    """ Gets a network name. """

    network_name = properties.get('network')
    if network_name:
        is_self_link = '/' in network_name or '.' in network_name

        if is_self_link:
            network_url = network_name
        else:
            network_url = 'global/networks/{}'.format(network_name)

    return network_url


def generate_config(context):
    """ Entry point for the deployment resources. """
    project = context.env['project']
    network = context.properties.get('network')

    resources = []
    out = {}
    for i, rule in enumerate(context.properties['rules'], 1000):
        # Use VPC if specified in the properties. Otherwise, specify
        # the network URL in the config. If the network is not specified in
        # the config, the API defaults to 'global/networks/default'.
        if network and not rule.get('network'):
            rule['network'] = get_network(context.properties)

        rule['priority'] = rule.get('priority', i)
        resources.append(
            {
                'name': rule['name'],
                'type': 'compute.beta.firewall',
                'properties': rule
            }
        )

    return {'resources': resources }
