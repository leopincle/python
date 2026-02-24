def validate_pipeline(pipeline: dict):

    errors = []
    
    accepted_keys = {"name", "stages", "timeout", "notify_email"}
    required_stages = {"build", "deploy"}

    missing = accepted_keys - pipeline.keys()

    if missing:
        errors.append(f"Missing keys: {missing}. Required keys are: {accepted_keys}")
        return False

    for key in pipeline:
        if key not in accepted_keys:
            errors.append(f"Invalid key: {key}. Allowed keys are: {accepted_keys}")
    
    if pipeline["name"] == "":
        errors.append("Pipeline name cannot be empty.")

    if not isinstance(pipeline["stages"], list) or len(pipeline["stages"]) == 0:
        errors.append("Stages must be a non-empty list.")
    
    if isinstance(pipeline["stages"], list):
        if not required_stages.issubset(set(pipeline["stages"])):
            errors.append("Pipeline must include build and deploy stages.")
        
    if not isinstance(pipeline["timeout"], int) or (pipeline["timeout"] < 5 or pipeline["timeout"] > 60):
        errors.append("Timeout must be an integer between 5 and 60.")
    
    if pipeline["notify_email"] == "" or "@" not in pipeline["notify_email"]:
        errors.append("Invalid email address for notify_email.")

    if errors:
        for error in errors:
            print(f"Error: {error}")
        return False

    return True

pipeline = {
    "name": "CI/CD Pipeline",
    "stages": ["build", "test", "deploy"],
    "timeout": 25,
    "notify_email": "devops@company.com"
}

validate_pipeline(pipeline)