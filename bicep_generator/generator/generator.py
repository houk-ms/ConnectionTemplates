import sys
from models.connector import (
    AuthType,
    NetworkSolution,
    Connector,
    TargetType
)
from engine_factory import (
    get_source_engine,
    get_target_engine,
    get_service_connector_engine,
    get_role_assignment_engine,
    get_firewall_engine,
    get_secret_engine
)


class Generator():
    def __init__(self, payload):
        self.payload = payload
        self._resolve_target_info(payload)
        self.engines = []
        self.deployment_names = []
        
        self.use_service_connector = False


    def _resolve_target_info(self, payload):
        self.connectors = []
        for block in payload:
            source_type = block.get('source_type')
            source_id = block.get('source_id')
            source_props = block.get('source_props')

            block_connectors = []
            for target in block.get('targets'):
                block_connectors.append(Connector(
                    source_type = source_type,
                    source_id = source_id,
                    source_props = source_props,
                    target_type = target.get('target_type'),
                    target_id = target.get('target_id'),
                    target_props= target.get('target_props'),
                    auth_type = target.get('auth_type'),
                    client_type = target.get('client_type'),
                    kv_store = target.get('kv_store'),
                    network_solution = target.get('network_solution')
                ))
            self.connectors.append(block_connectors)


    def _add_comment(self, comment):
        return '\n\n// {}\n\n'.format(comment)


    def generate_main_with_manual_configs(self):
        main_params = self._add_comment('The main bicep to create compute and target services with connections')
        target_blocks = ''
        source_blocks = ''
        role_assignment_blocks = ''
        firewall_blocks = ''

        for block_connectors in self.connectors:
            
            app_settings = []
            for connector in block_connectors:
                target_engine = get_target_engine(connector)
                self.engines.append(target_engine)
                app_settings += target_engine.get_app_settings()

                # target resource blocks
                if target_engine.module_deployment_name not in self.deployment_names:
                    self.deployment_names.append(target_engine.module_deployment_name)

                    main_params += target_engine.generate_parameters()
                    target_blocks += self._add_comment('Create target service: {}'.format(target_engine.service_brand_name))
                    target_blocks += target_engine.generate_module()
                    if target_engine.need_existing_resource:
                        target_blocks += target_engine.generate_existing_resource()
                    target_blocks += target_engine.generate_variables()

                # if keyvault secret store is enabled
                if connector.kv_store:
                    target_blocks += self._add_comment('Create keyvault secret for: {}'.format(target_engine.service_brand_name))
                    secret_engine = get_secret_engine(connector)
                    self.engines.append(secret_engine)

                    secret_name = target_engine.get_secret_name()
                    secret_engine.set_module_param_secret(secret_name)
                    target_blocks += secret_engine.generate_module()
                    target_blocks += secret_engine.generate_variables()

            
            source_engine = get_source_engine(block_connectors[0])
            self.engines.append(source_engine)
            main_params += source_engine.generate_parameters()
            
            if source_engine.module_deployment_name not in self.deployment_names:
                self.deployment_names.append(source_engine.module_deployment_name)

                source_blocks += self._add_comment('Create compute service: {}'.format(source_engine.service_brand_name))
                source_engine.set_module_param_app_settings(app_settings)
                source_blocks += source_engine.generate_module()
            
            # if any target need system identity to auth, set principal_id variable, similar for outbound ip
            use_principal = False
            use_outboundip = False
            for connector in block_connectors:
                if connector.auth_type == AuthType.SystemIdentity.value:
                    use_principal = True
                if connector.network_solution == NetworkSolution.IpFirewall.value:
                    use_outboundip = True

            if use_principal:
                source_engine.set_variable_principal_id()
            if use_outboundip:
                source_engine.set_variable_outbound_ip()
            source_blocks += source_engine.generate_variables()

            for connector in block_connectors:
                if connector.auth_type == AuthType.SystemIdentity.value:
                    # target resource role assignment blocks
                    principal_id = source_engine.get_principal_id()
                    role_assignment_engine = get_role_assignment_engine(connector)
                    self.engines.append(role_assignment_engine)
                    role_assignment_blocks += self._add_comment('Create {}'.format(role_assignment_engine.service_brand_name))
                    role_assignment_engine.set_module_param_principal_id(principal_id)
                    role_assignment_blocks += role_assignment_engine.generate_module()
                    main_params += role_assignment_engine.generate_parameters()
                if connector.network_solution == NetworkSolution.IpFirewall.value:
                    # target resource ip firewall blocks
                    outbound_ip = source_engine.get_outbound_ip()
                    firewall_engine = get_firewall_engine(connector)
                    self.engines.append(firewall_engine)
                    firewall_blocks += self._add_comment('Create {}'.format(firewall_engine.service_brand_name))
                    firewall_engine.set_module_param_outbound_ip(outbound_ip)
                    firewall_blocks += firewall_engine.generate_module()

        return main_params + target_blocks + source_blocks + role_assignment_blocks + firewall_blocks
    

    def generate_main_with_service_connector(self):
        main_params = self._add_comment('The main bicep to create compute and target services with connections')
        target_blocks = ''
        service_connector_blocks = ''
        source_blocks = ''
        for connector in self.connectors:
            target_engine = get_target_engine(connector)
            self.engines.append(target_engine)
        
            target_blocks += self._add_comment('Create target service: {}'.format(target_engine.service_brand_name))
            target_blocks += target_engine.generate_module()
            main_params += target_engine.generate_parameters()

            target_resource_id = target_engine.get_target_resource_id()
            service_connector_engine = get_service_connector_engine(connector)
            self.engines.append(service_connector_engine)
            service_connector_blocks += self._add_comment('Create service connector for {}'.format(target_engine.service_brand_name))
            service_connector_blocks += service_connector_engine.generate_module(target_resource_id)
            main_params += service_connector_engine.generate_parameters()

        source_engine = get_source_engine(self.connectors[0])
        self.engines.append(source_engine)
        main_params += source_engine.generate_parameters()
        source_blocks += self._add_comment('Create compute service: {}'.format(source_engine.service_brand_name))
        source_blocks += source_engine.generate_module()

        return main_params + target_blocks + source_blocks + service_connector_blocks


    def generate_main(self):
        if self.use_service_connector:
            return self.generate_main_with_service_connector()
        return self.generate_main_with_manual_configs()

    def resource_path(sefl, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        import os
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


    def generate(self, output_path):
        from datetime import datetime
        import os, shutil

        output_folder = '{}/infra/{}'.format(output_path, datetime.now().strftime('%Y-%m-%d#%H-%M-%S'))
        assets_folder = self.resource_path('./biceps')
        os.makedirs(output_folder)
        # shutil.rmtree('./infra/')
        
        main_content = self.generate_main()
        main_file = open('{}/main.bicep'.format(output_folder), 'w', encoding='utf-8')
        main_file.write(main_content.strip())

        dependency_files = []
        for engine in self.engines:
            dependency_files += engine.dependency_bicep_files
            dependency_files.append(engine.module_bicep_file)
        
        for file_name in dependency_files:
            shutil.copy('{}/{}'.format(assets_folder, file_name), '{}/{}'.format(output_folder, file_name))

        print('Success! Bicep files generated in folder: {}'.format(output_folder))


def main(file_path, output_path):
    import json

    payload_file = open(file_path, 'r', encoding='utf-8')
    payload = json.load(payload_file)

    import payload_parser
    payload = payload_parser.parse(payload)
    generator = Generator(payload)
    generator.generate(output_path)


if len(sys.argv) > 2:
    main(sys.argv[1], sys.argv[2])
else:
    print("Please provide the payloads.json file path and output folder path.")