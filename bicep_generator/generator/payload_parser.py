# a temparay payload parser

def parse(payload):
    resources = dict()
    for resource in payload['resources']:
        resource_type = resource['type']
        for instance in resource['instances']:
            resource_name = instance['name']
            key = '${' + resource_type + '.' + resource_name + '}'
            resources[key] = {
                'type': resource_type,
                'name': resource_name,
                'props': instance
            }
    
    result = dict()
    for binding in payload['bindings']:
        source = binding['source']
        if source not in result:
            result[source] = []
        result[source].append(binding)

    source_keys = list(result.keys())
    source_keys.sort(key=lambda x: len(result[x]), reverse=True)

    new_payload = []
    for source in source_keys:
        source_blocks = {
            'source_type': resources[source]['type'], 
            'source_props': {key:val for key, val in resources[source]['props'].items()},
            'targets': []
        }
        for binding in result[source]:
            target = binding['target']
            target_blocks = {
                'target_type': resources[target]['type'],
                'target_props': {key:val for key, val in resources[target]['props'].items()},
                'auth_type': binding['connection'],
                'kv_store': True if binding.get('store') else False
            }

            if binding.get('key'):
                target_blocks['target_props']['key'] = binding['key']

            source_blocks['targets'].append(target_blocks)
        
        new_payload.append(source_blocks)
    
    return new_payload