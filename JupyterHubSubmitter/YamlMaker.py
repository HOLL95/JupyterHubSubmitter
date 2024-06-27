import yaml
import os
from git import Repo, GitCommandError
def create_Yaml(location,**kwargs):
    if "name" not in kwargs:
        name="Generic Job Submission"
    else:
        name=kwargs["name"]
    if "container" not in kwargs:
        print("Warning: setting container to default gpu")
        container="gpu-container"
    else:
        container=kwargs["container"]
    if "image"not in kwargs:
        print("Warning: setting container to default")
        image="gitlab-registry.nrp-nautilus.io/zihaozhou/nautilus_tutorial:jupyterhub"
    else:
        image=kwargs["container"]
    if "python_arg" not in kwargs:
        kwargs["python_arg"]=""
    if "output_file" not in kwargs:
        raise ValueError("Need to provide the trained output file")
    if "data_loc" not in kwargs:
        print("Warning: Assuming data location is provided in train.py")
        kwargs["data_loc"]=""
    data ={
    'kind': 'Job',
    'apiVersion': 'batch/v1',
    'metadata': {
        'name': name
    },
    'spec': {
        'template': {
            'spec': {
                'containers': [{
                    'name': container,
                    'image': image,
                    'command': ["/bin/bash", "-c"],
                    'args': [
                            "python {0}/train.py {1} {2}".format(location, kwargs["python_arg"], kwargs["data_loc"]),
                            "mv {0} /output".format(kwargs["output_file"])
                            ],  # Assuming you want an empty string as an argument
                    'volumeMounts': [{
                        'mountPath': "/output",
                        'name': "mnist-test-volume"
                    }],
                    'resources': {
                        'limits': {
                            'nvidia.com/gpu': "1",
                            'memory': "8G",
                            'cpu': "4"
                        },
                        'requests': {
                            'nvidia.com/gpu': "1",
                            'memory': "8G",
                            'cpu': "4"
                        }
                    }
                }],
                'restartPolicy': 'Never',
                'volumes': [{
                    'name': 'mnist-test-volume',
                    'persistentVolumeClaim': {
                        'claimName': 'mnist-test-volume'
                    }
                }]
                }
            }
        }
    }

    # Specify the file path where the YAML file will be saved
    file_path = 'JobSubmission.yaml'

    # Write the data to the YAML file
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

    print(f"YAML file generated and saved to {file_path}")
def LocateFiles(path):
    if ".git" in path:
        truncated_link=path[:path.find(".git")]
        
        link_list=truncated_link.split("/")
        name=link_list[-1]
        files=os.listdir()
        if name not in files:
            
            try:
                
                Repo.clone_from(path, name)
            
                print("Repository successfully cloned")
            except:
                raise Exception("Failed to clone repository {0}".format(name))
        else:
            print("Warning: using existing {0} directory".format(name))
            
       
    else:
        name=path
    code_location=os.getcwd()+"/"+name
    try:
        files=os.listdir(code_location)
    except:
        raise FileNotFoundError("Code location {0} not found".format(code_location))
    if "train.py" not in files:
        raise FileNotFoundError("YamlMaker requires a train.py in the code directory")
    return name
def RemoteSubmission(path, **kwargs):
    loc=LocateFiles(path)
    create_Yaml(loc, **kwargs)
    #TODO submit to Nautilus
    
