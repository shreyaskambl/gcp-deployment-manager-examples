COMPUTE_URL_BASE = 'https://www.googleapis.com/compute/v1/'


def GenerateConfig(context):
  """Creates the first virtual machine."""

  resources = [{
      'name': context.properties['name'],
      'type': 'compute.v1.instance',
      'properties': {
          'zone': context.properties['zone'],
          "machineType": "zones/" + context.properties['zone'] + "/machineTypes/n1-standard-1",
          'disks': [{
              'deviceName': 'boot',
              'type': 'PERSISTENT',
              'boot': True,
              'autoDelete': True,
              'initializeParams': {
                  'sourceImage': ''.join([COMPUTE_URL_BASE, 'projects/','windows-cloud/global/', 'images/family/windows-2016'])
                  
              }
          }],
          "serviceAccounts": [
          {
            "email": context.properties['account_name'] + "@" + context.env['project'] + ".iam.gserviceaccount.com"
          }],
          'networkInterfaces': [{
              "network": "projects/" + context.env['project'] + "/global/networks/" + context.properties['network'],
              "subnetwork": "projects/" + context.env['project'] + "/regions/" + context.properties['region'] + "/subnetworks/" + context.properties['subnetwork'],
              'accessConfigs': [{
                  'name': 'External NAT',
                  'type': 'ONE_TO_ONE_NAT'
              }]
          }]
      }
  }]
  return {'resources': resources}
