from apiflask import APIBlueprint
from adapters.aldus.accounts import AccountManager
from adapters.aldus import projects
from adapters.icns.resolver import get_icns_names

accounts_bp = APIBlueprint("accounts", __name__)

@accounts_bp.route('/<chain>/<network>/accounts/<account_address>/info', methods=['GET'])
def get_account_info(chain, network, account_address):
    try:
        public_info = AccountManager(chain, network).get_account(account_address)
    except Exception:
        public_info = None

    try:
        icns = get_icns_names(account_address)
        icns_primary_name = icns.get("primary_name")
        if len(icns_primary_name) == 0:
            icns = None
    except Exception:
        icns = None

    try:
        project_info = projects.get_project(chain, network, public_info.get("slug")).get("details")
    except Exception:
        project_info = None
        
    
    return {"project_info": project_info, "public_info": public_info, "icns": icns }, 200
    
