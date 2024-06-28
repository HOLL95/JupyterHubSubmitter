import yaml
from kubernetes import client, config
from kubernetes.client import V1Job
import uuid

# Load the kube-config from the default location
config.load_kube_config()
print("Loaded kube config")

# Load the YAML file
with open("kube_train.yaml", 'r') as stream:
    job_yaml = yaml.safe_load(stream)
print("loaded yaml file")

# Modify the job name to be unique
unique_job_name = f"{job_yaml['metadata']['name']}-{uuid.uuid4()}"
job_yaml['metadata']['name'] = unique_job_name

# Create the Job object from the YAML
job = client.ApiClient()._ApiClient__deserialize_model(job_yaml, V1Job)
print("created job object")

# Submit the Job to the cluster
api_instance = client.BatchV1Api()
namespace = "rse-kube"
try:
    api_response = api_instance.create_namespaced_job(
        body=job,
        namespace=namespace
    )
    print("Job created. Status='%s'" % str(api_response.status))
except ApiException as e:
    print(f"Exception when creating job: {e}")
