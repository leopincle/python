def cpu_validation(cpu: str):
    if not isinstance(cpu, str) or not cpu.endswith("m"):
        return "CPU resource must be specified in millicores, e.g., '500m'."
    return None

def memory_validation(memory: str):
    if not isinstance(memory, str) or not (memory.endswith("Mi") or memory.endswith("Gi")):
        return "Memory resource must be specified in Mi, e.g., '256Mi'."
    return None

def validate_deployment(deployment: dict):

    errors = []
    warnings = []

    accepted_keys = {"name", "replicas", "image", "resources"}

    for key in deployment:
        if key not in accepted_keys:
            errors.append(f"Invalid key: {key}. Allowed keys are: {accepted_keys}")

    missing = accepted_keys - deployment.keys()
    if missing:
        return {
            "valid": False,
            "errors": errors
        }

    if deployment["name"] == "":
        errors.append("Deployment name cannot be empty.")
    
    if deployment["replicas"] < 1:
        errors.append("Replicas count must be at least 1.")

    image = deployment["image"]

    if not isinstance(image, str):
        errors.append("Image must be a string.")
    elif ":" not in image:
        errors.append("Image must include a tag, e.g., 'my-app:v1'.")
    else:
        name, tag = image.split(":", 1)
        if tag =="latest":
            warnings.append("Using 'latest' tag is not recommended for production deployments. Consider using a specific version tag.")
    
    resources = deployment.get("resources", {})
    if not isinstance(resources, dict):
        errors.append("Resources must be a dictionary containing 'cpu' and 'memory' keys.")
    else:
    
        cpu_validation_result = cpu_validation(deployment["resources"].get("cpu"))
        if cpu_validation_result:
            errors.append(cpu_validation_result)
        
        memory_validation_result = memory_validation(deployment["resources"].get("memory"))
        if memory_validation_result:
            errors.append(memory_validation_result)

    if errors:
        return {
            "valid": False,
            "errors": errors,
            "warnings": warnings
        }
        
    return {
        "valid": True,
        "errors": errors,
        "warnings": warnings
    }


deployment = {
    "name": "my-app-deployment",
    "replicas": 3,
    "image": "my-app:latest",
    "resources": {
        "cpu": "500m",
        "memory": "256Mi"
    }
}

validate_deployment(deployment)