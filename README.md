# Serverless Monitoring
A serveless monitoring app written in python. This project is part of the Cloud Computing course at UFMG.

## How the project is structured

The project have the folder tree below:

```
project
│   
│   README.md (this document)
│   discussion-task-2.pdf (the discussion about the metrics monitored by the dashboard app)
|   discussion-task-3.pdf (the discussion about the tests performed on the CI/CD structure)
│
└─── handler (the handler implementention)
    │
    │   apply-handler.sh (a script to create the ConfigMaps and apply the yaml files on kubernetes)
    │   delete-handler.sh (a script to delete the instances created on kubernetes)
    │
    └─── kube (folder containing the .yaml files)
        │   deployment.yaml
        │   outputkey.yaml
        │   pyfile.yaml
    │
    └─── src
        │   handler.py

│
└─── dashboard (the dahsboard implementention)
    │
    │   apply-dashboard.sh (a script to apply the yaml files on kubernetes)
    │   delete-dashboard.sh (a script to delete the instances created on kubernetes)
    │
    └─── kube (folder containing the .yaml files)
        │   deployment.yaml
        │   service.yaml
    │
    └─── src
        │   dashboard.py
        │   requirements.txt
        │   Dockerfile
        │   .dockerignore

│
└─── runtime (the runtime implementention)
    │
    └─── kube (folder containing the .yaml files)
        │   deployment.yaml
    │
    └─── src
        │   runtime.py
        │   requirements.txt
        │   Dockerfile
        │   .dockerignore

```

