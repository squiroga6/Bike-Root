import os
import cfg_load

try:
    # when running locally
    # get name of enviroment variable
    env_name=os.getenv("ENV_VAR")

    # collect secrets if running locally in development enviromnent
    base_secrets = cfg_load.load(r"config\secrets.yml")['default']
    env_secrets = cfg_load.load(r"config\secrets.yml")[env_name]

    # load default and env specific config dictionarys and combine into params
    base = cfg_load.load(os.path.join('config', 'config.yml'))['default']
    env_params = cfg_load.load(os.path.join('config', 'config.yml'))[env_name]
    params = base | env_params | base_secrets | env_secrets

    SLACK_BOT_TOKEN = params['SLACK_BOT_TOKEN']
    CHANNEL_ID = params['CHANNEL_ID']

except:
    # # If running on the server this will throw an error;
    # # fetch secrets from enviroment variables instead    
    # ORA_DRIVER = os.getenv['ORA_DRIVER']
    # ORA_HOST = os.getenv['ORA_HOST']
    # ORA_SERVICE = os.getenv['ORA_SERVICE']
    # ORA_PORT = os.getenv['ORA_PORT']
    # ORA_USERNAME = os.getenv['ORA_USERNAME']
    # ORA_PASSWORD = os.getenv['ORA_PASSWORD']
    pass