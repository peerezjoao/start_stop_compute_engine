from dotenv import load_dotenv
from google.oauth2 import service_account
from google.cloud import compute_v1
import os, json, logging

load_dotenv()

CREDENTIALS = json.loads(os.environ.get('CREDENTIALS'))

if not os.path.exists('credentials.json'):
    with open('credentials.json', 'w') as cred_file:
        json.dump(CREDENTIALS, cred_file)
        
def get_env_vars(var_name : str):
    value = os.environ.get(var_name)
    if not value:
        raise ValueError(f'Required environment variable {var_name} is not set.' )
    return value

def start_instance(credentials_json, project_id, zone, instance_name):
    logging.basicConfig(level=logging.INFO)
    # validate essentials fields in credentials
    if not all(field in credentials_json for field in ('project_id', 'private_key_id')):
        raise ValueError(f"Missing required fields in credentials: project_id, private_key_id")

    credentials_account = service_account.Credentials.from_service_account_info(credentials_json, 
                                scopes=["https://www.googleapis.com/auth/cloud-platform"])
    
    try:
        gce = compute_v1.InstancesClient(credentials=credentials_account)
        request = compute_v1.StartInstanceRequest(project=project_id, zone=zone, instance=instance_name)
        response = gce.start(request)
        logging.info(f'Instance {instance_name} started successfully. Response: {response}')

    except Exception as e:
        logging.error(f'Unexpected error: {e}')

if __name__ == "__main__":
    try:
        # Retrieve and validate environment variables
        project_id = CREDENTIALS['project_id']
        zone = get_env_vars('ZONE')
        instance_name = get_env_vars('MY_INSTANCE_NAME')

        # Start the instance 
        start_instance(CREDENTIALS, project_id, zone, instance_name)

    except Exception as e:
        logging.error(f"An error occurred in the main execution: {e}")
