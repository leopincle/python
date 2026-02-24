def validate_config(config: dict):

    valid_env = ("dev", "staging", "prod")
    valid_keys = {"environment", "replicas", "enable_monitoring", "owner"}

    missing_keys = valid_keys - config.keys()
    if missing_keys:
        print(f"Invalid configuration: Missing keys: {', '.join(missing_keys)}")
        return False
        
    if config["environment"] not in valid_env:
        print(f"Invalid environment value: {config['environment']}. Must be one of: {', '.join(valid_env)}")
        return False
        
    if config["owner"] == "":
        print("Owner cannot be empty.")
        return False

    if not isinstance(config["replicas"], int):
        print("Replicas count must be an integer.")
        return False
    
    if config["replicas"] < 1:
        print("Replicas count must be at least 1.")
        return False
    
    
    return True

      

config = {
    "environment": "prod",
    "replicas": 1,
    "enable_monitoring": True,
    "owner": "L"
}

print(validate_config(config))