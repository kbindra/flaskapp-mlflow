from kubernetes import client, config


def create_deployment_object(teamid):
    deployment_name = str('mlflow-deployment-' + teamid)
    folder_name = str('--backend-store-uri=/opt/mlflow/backend-' + teamid + '/')
    # Configureate Pod template container
    container = client.V1Container(
        name="mlflow-instance",
        image="kbindra12/mlflow:v4",
        image_pull_policy="Always",
        volume_mounts=[
            client.V1VolumeMount(
                name="mlflow-pvc",
                mount_path="/opt/mlflow/"
            )
        ],
        args=[
            "--host=0.0.0.0",
            "--port=5000",
            folder_name
        ],
        ports=[
            client.V1ContainerPort(
                name="http",
                container_port=5000,
                protocol="TCP"
            )
        ]
    )
    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": deployment_name}),
        spec=client.V1PodSpec(
            containers=[container],
            volumes=[
                client.V1Volume(
                    name="mlflow-pvc",
                    persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                        claim_name="mlflow-pvc"
                    )
                ),
            ],
        )
    )
    # Create the specification of deployment
    spec = client.V1DeploymentSpec(
        replicas=1,
        template=template,
        selector={
            'matchLabels': {'app': deployment_name}
        }
    )
    # Instantiate the deployment object
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=deployment_name),
        spec=spec
    )

    return deployment

def create_service(teamid):
    deployment_name = str('mlflow-deployment-' + teamid)
    service_name = str("mlflow-service-" + teamid)
    core_v1_api = client.CoreV1Api()
    body = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(
            name=service_name
        ),
        spec=client.V1ServiceSpec(
            type="NodePort",
            selector={"app": deployment_name},
            ports=[client.V1ServicePort(
                port=5000,
                target_port=5000,
                protocol="TCP",
                name="http"
            )]
        )
    )
    # Creation of the Deployment in specified namespace
    # (Can replace "default" with a namespace you may have created)
    api_response = core_v1_api.create_namespaced_service(namespace="default", body=body)
    print("Service created. status='%s'" % str(api_response.status))


def delete_service(teamid):
    service_name = str("mlflow-service-" + team_id)
    core_v1_api = client.CoreV1Api()
    # Creation of the Deployment in specified namespace
    # (Can replace "default" with a namespace you may have created)
    api_response = core_v1_api.delete_namespaced_service(namespace="default", name=service_name)
    print("Service deleted. status='%s'" % str(api_response.status))


def create_deployment(api_instance, deployment):
    # Create deployement
    api_response = api_instance.create_namespaced_deployment(
        body=deployment,
        namespace="default")
    print("Deployment created. status='%s'" % str(api_response.status))



def delete_deployment(api_instance, teamid):
    # Delete deployment
    deployment_name = str('mlflow-deployment-' + teamid)
    api_response = api_instance.delete_namespaced_deployment(
        name=deployment_name,
        namespace="default",
        body=client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5))
    print("Deployment deleted. status='%s'" % str(api_response.status))

def get_api_instance():
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    config.load_kube_config()

    # Create a ApiClient with our config
    ApiClient = client.ApiClient()
    
    apps_v1 = client.AppsV1Api(ApiClient)

    return apps_v1