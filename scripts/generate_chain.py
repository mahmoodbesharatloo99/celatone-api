import os

# def create_chain_directory(chain_name, network_names):
#     for network in network_names:
#         network_name = network.replace('-', '_')

#         # Creating the directories
#         os.makedirs(f'./server-v2/core/{chain_name.replace("-", "_")}/{network_name}', exist_ok=True)

#         # Writing the routes.py file for the network
#         with open(f'./server-v2/core/{chain_name.replace("-", "_")}/{network_name}/routes.py', 'w') as file:
#             file.write(f'''from core.base.base_blueprint import BaseBlueprint
# from .service import {network_name.capitalize()}Service as Service

# service_instance = Service()
# name = '{network}'
# url_prefix = '/{network}'

# base_blueprint = BaseBlueprint(service_instance, name, url_prefix)
# blueprint = base_blueprint.get_blueprint()
# ''')

#         # Writing the service.py file for the network
#         with open(f'./server-v2/core/{chain_name.replace("-", "_")}/{network_name}/service.py', 'w') as file:
#             file.write(f'''from core.base.base_service import BaseService

# class {network_name.capitalize()}Service(BaseService):
#     chain: str = "{chain_name}"
#     network: str = "{network}"
# ''')

#     # Writing the routes.py file for the chain
#     imports = "\n".join([f'from .{network.replace("-", "_")}.routes import blueprint as {network.replace("-", "_")}' for network in network_names])
#     blueprints = "\n".join([f'blueprint.register_blueprint({network.replace("-", "_")})' for network in network_names])
#     with open(f'./server-v2/core/{chain_name.replace("-", "_")}/routes.py', 'w') as file:
#         file.write(f'''from flask import Blueprint
# {imports}

# blueprint = Blueprint('{chain_name}', __name__, url_prefix='/{chain_name}')

# {blueprints}
# ''')

def create_chain_directory(chain_name, network_names):
    chain_directory = f'./server-v2/core/{chain_name.replace("-", "_")}'
    chain_exists = os.path.exists(chain_directory)

    for network in network_names:
        network_name = network.replace('-', '_')

        # Creating the directories
        os.makedirs(f'{chain_directory}/{network_name}', exist_ok=True)

        # Creating the directories
        os.makedirs(f'./server-v2/core/{chain_name.replace("-", "_")}/{network_name}', exist_ok=True)

        # Writing the routes.py file for the network
        with open(f'./server-v2/core/{chain_name.replace("-", "_")}/{network_name}/routes.py', 'w') as file:
            file.write(f'''from core.base.base_blueprint import BaseBlueprint
from .service import {network.replace("-", "").capitalize()}Service as Service

service_instance = Service()
name = '{network}'
url_prefix = '/{network}'

base_blueprint = BaseBlueprint(service_instance, name, url_prefix)
blueprint = base_blueprint.get_blueprint()
''')

        # Writing the service.py file for the network
        with open(f'./server-v2/core/{chain_name.replace("-", "_")}/{network_name}/service.py', 'w') as file:
            file.write(f'''from core.base.base_service import BaseService

class {network.replace("-", "").capitalize()}Service(BaseService):
    chain: str = "{chain_name}"
    network: str = "{network}"
''')

    # If chain already exists, just append new networks
    if chain_exists:
        with open(f'{chain_directory}/routes.py', 'r') as file:
            lines = file.readlines()

        # Finding the index to insert the import line
        import_line_index = next((i for i, line in enumerate(lines) if 'import' not in line), -1)
        for network in network_names:
            network_name = network.replace("-", "_")
            lines.insert(import_line_index, f'from .{network_name}.routes import blueprint as {network_name}\n')
            import_line_index += 1

        # Appending the register_blueprint line at the end
        for network in network_names:
            network_name = network.replace("-", "_")
            lines.append(f'blueprint.register_blueprint({network_name})\n')

        with open(f'{chain_directory}/routes.py', 'w') as file:
            file.writelines(lines)
    else:
        # Writing the routes.py file for the chain
        imports = "\n".join([f'from .{network.replace("-", "_")}.routes import blueprint as {network.replace("-", "_")}' for network in network_names])
        blueprints = "\n".join([f'blueprint.register_blueprint({network.replace("-", "_")})' for network in network_names])
        with open(f'{chain_directory}/routes.py', 'w') as file:
            file.write(f'''from flask import Blueprint
{imports}

blueprint = Blueprint('{chain_name}', __name__, url_prefix='/{chain_name}')

{blueprints}
''')
        update_app_file(chain_name)
                    
def update_app_file(chain_name):
    # Check if the app.py file exists
    app_file_path = './server-v2/app.py'
    if os.path.exists(app_file_path):
        with open(app_file_path, 'r') as file:
            lines = file.readlines()

        # Adding the import line after the existing imports
        import_line_index = next((i for i, line in enumerate(lines) if 'import' not in line), -1)
        lines.insert(import_line_index, f'from core.{chain_name.replace("-", "_")}.routes import blueprint as {chain_name.replace("-", "_")}\n')

        # Finding the index to insert the app.register_blueprint line after the last existing one
        register_blueprint_index = max(i for i, line in enumerate(lines) if 'app.register_blueprint' in line) + 1
        lines.insert(register_blueprint_index, f'app.register_blueprint({chain_name.replace("-", "_")})\n')

        with open(app_file_path, 'w') as file:
            file.writelines(lines)
    else:
        print("app.py file not found.")

# Usage: python scripts/generate_chain.py
chain_name = input("Enter the chain name: ")
network_names = input("Enter the network names, separated by commas: ").split(",")
create_chain_directory(chain_name, network_names)


