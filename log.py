def validate_config(config: dict):

    valid_env = ("dev", "staging", "prod")
    valid_keys = ("environment", "replicas", "enable_monitoring", "owner")

    
    if "environment" in valid_keys and "replicas" in valid_keys and "enable_monitoring" in valid_keys and "owner" in valid_keys:
        
        if config["environment"] in valid_env:
            if config["owner"] != "":
                if config["environment"] == "prod" and config["replicas"] >=2:
                    
                    return True
                
                elif config["environment"] != "prod" and config["replicas"] >= 1:

                    return True
                
                else:
                    return False
                
            else:
                return False
        else:
            return False

                

config = {
    "environment": "dev",
    "replicas": 1,
    "enable_monitoring": True,
    "owner": "L"
}

print(validate_config(config))