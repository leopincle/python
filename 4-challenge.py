class DeploymentValidator:
    def __init__(self, deployment: dict):
        self.errors = []
        self.warnings = []
        self.deployment = deployment

    def add_error(self, message: str):
        self.errors.append(message)

    def add_warning(self, message: str):
        self.warnings.append(message)

    def cpu_validation(self, cpu: str)-> None | str:
        if not isinstance(cpu, str) or not cpu.endswith("m"):
            return "CPU resource must be specified in millicores, e.g., '500m'."
        return None

    def memory_validation(self, memory: str) -> None | str:
        if not isinstance(memory, str) or not (memory.endswith("Mi") or memory.endswith("Gi")):
            return "Memory resource must be specified in Mi, e.g., '256Mi'."
        return None

    def validate_deployment(self):
        accepted_keys = {"name", "replicas", "image", "resources"}

        for key in self.deployment:
            if key not in accepted_keys:
                self.add_error(f"Invalid key: {key}. Allowed keys are: {accepted_keys}")

        missing = accepted_keys - self.deployment.keys()
        if missing:
            return {
                "valid": False,
                "errors": self.errors,
                "warnings": self.warnings
            }

        if self.deployment["name"] == "":
           self.add_error("Deployment name cannot be empty.")
        
        if self.deployment["replicas"] < 1:
            self.add_error("Replicas count must be at least 1.")

        image = self.deployment["image"]

        if not isinstance(image, str):
            self.add_error("Image must be a string.")
        elif ":" not in image:
            self.add_error("Image must include a tag, e.g., 'my-app:v1'.")
        else:
            name, tag = image.split(":", 1)
            if tag =="latest":
                self.add_warning("Using 'latest' tag is not recommended for production deployments. Consider using a specific version tag.")
        
        resources = self.deployment.get("resources", {})
        if not isinstance(resources, dict):
            self.add_error("Resources must be a dictionary containing 'cpu' and 'memory' keys.")
        else:
        
            cpu_validation_result = self.cpu_validation(resources.get("cpu"))
            if cpu_validation_result:
                self.add_error(cpu_validation_result)
            
            memory_validation_result = self.memory_validation(resources.get("memory"))
            if memory_validation_result:
                self.add_error(memory_validation_result)

        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings
        }

