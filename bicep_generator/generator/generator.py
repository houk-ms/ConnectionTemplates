from models.connector import (
    AuthType,
    NetworkSolution,
    Connector
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
        self._resolve_source_info(payload)
        self._resolve_target_info(payload)
        self.engines = []


    def _resolve_source_info(self, payload):
        self.source_type = payload.get('source_type')
        self.source_id = payload.get('source_id')
        self.use_service_connector = payload.get('use_service_connector')


    def _resolve_target_info(self, payload):
        self.connectors = []
        for target in payload.get('targets'):
            self.connectors.append(Connector(
                source_type = self.source_type,
                source_id = self.source_id,
                target_type = target.get('target_type'),
                target_id = target.get('target_id'),
                auth_type = target.get('auth_type'),
                client_type = target.get('client_type'),
                kv_store = target.get('kv_store'),
                network_solution = target.get('network_solution')
            ))


    def _add_comment(self, comment):
        return '\n\n// {}\n\n'.format(comment)


    def generate_main_with_manual_configs(self):
        main_params = self._add_comment('The main bicep to create compute and target services with connections')
        target_blocks = ''
        source_blocks = ''

        
        app_settings = []
        for connector in self.connectors:
            target_engine = get_target_engine(connector)
            self.engines.append(target_engine)
            main_params += target_engine.generate_parameters()
            app_settings += target_engine.get_app_settings()

            # target resource blocks
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

        
        source_engine = get_source_engine(self.connectors[0])
        self.engines.append(source_engine)
        main_params += source_engine.generate_parameters()
        
        source_blocks += self._add_comment('Create compute service: {}'.format(source_engine.service_brand_name))
        source_engine.set_module_param_app_settings(app_settings)
        source_blocks += source_engine.generate_module()
        
        # if any target need system identity to auth, set principal_id variable, similar for outbound ip
        use_principal = False
        use_outboundip = False
        for connector in self.connectors:
            if connector.auth_type == AuthType.SystemIdentity.value:
                use_principal = True
            if connector.network_solution == NetworkSolution.IpFirewall.value:
                use_outboundip = True

        if use_principal:
            source_engine.set_variable_principal_id()
        if use_outboundip:
            source_engine.set_variable_outbound_ip()
        source_blocks += source_engine.generate_variables()


        role_assignment_blocks = ''
        firewall_blocks = ''
        for connector in self.connectors:
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


    def generate(self):
        from datetime import datetime
        import os, shutil

        output_folder = './outputs/{}'.format(datetime.now().strftime('%Y-%m-%d#%H-%M-%S'))
        assets_folder = './assets/resource_biceps'
        shutil.rmtree('./outputs/')
        os.makedirs(output_folder)

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


def main():
    import json

    payload_file = open('./generator/payload.json', 'r', encoding='utf-8')
    payload = json.load(payload_file)

    generator = Generator(payload)
    generator.generate()


main()