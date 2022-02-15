#!/bin/usr/python3
from argparse import ArgumentParser

from kubernetes import client, config, utils

parser = ArgumentParser()
parser.add_argument("-p", "--package", dest="package",
                    help="Package name")
parser.add_argument("-c", "--claim", dest="claim",
                    help="Persistent Volume Claim for libraries")
parser.add_argument("-n", "--namespace", dest="namespace",
                    help="Namespace in which to dispatch job")
parser.add_argument("-m", "--manifest-dir", dest="manifest",
                    help="Directory in which to output manifest of deployed job")
parser.add_argument("-w", "--worker-nodes", dest="workers",
                    help="""List of worker node names in format: -w '"node1","node2"')""")

args = parser.parse_args()

def create_build_job(package, libraries_pvc, workers, namespace="default"):
    config.load_kube_config()
    k8s_client = client.ApiClient()
    with open("job-template.yaml", "r") as f:
        tpl = f.read()
    tpl = tpl.replace("PACKAGENAMELOWER", ''.join(filter(str.isalnum, package.lower()))).replace("PACKAGENAME", package).replace("LIBRARIESCLAIM", libraries_pvc).replace("NAMESPACE", namespace).replace("WORKERNODES", workers)
    with open(f'{args.manifest}/{package}.yaml', "w") as f:
        f.write(tpl)
    utils.create_from_yaml(k8s_client, f'{args.manifest}/{package}.yaml')


create_build_job(args.package, args.claim, args.workers, args.namespace)


# JOB_NAME = "build"
# BUILD_IMAGE = "bioconductor/bioconductor_docker"
# GIT_BASE = "https://gitea.149.165.168.82.nip.io"
# GIT_OWNER = "packages"

# def create_job_object_for_package(package_name): #package_owner=GIT_OWNER, git_url=GIT_BASE):
#     # git_clone_cmd = "git clone {}/{}/{}".format(git_url, package_owner, package_name)
#     # r_install_cmd = "R CMD INSTALL {}".format(package_name)
#     # clone_container = client.V1Container(
#     #     name="build",
#     #     image=BUILD_IMAGE,
#     #     command=["sh"],
#     #     args=["-c", "{} && {}".format(git_clone_cmd, r_install_cmd)])
#     r_cmd = f'RScript -e \'BiocManager::install({package_name}, INSTALL_opts = "--build", update = FALSE, quiet = TRUE, force = TRUE, keep_outputs = TRUE)\''
#     container = client.V1Container(
#         name="build",
#         image=BUILD_IMAGE,
#         command=[r_cmd],
#         args=""
#         )

#     template = client.V1PodTemplateSpec(
#         metadata=client.V1ObjectMeta(labels={"package": package_name}),
#         spec=client.V1PodSpec(restart_policy="OnFailure", containers=[container]))

#     spec = client.V1JobSpec(
#         template=template,
#         backoff_limit=4)
#         #init_containers=init_c)

#     job = client.V1Job(
#         api_version="batch/v1",
#         kind="Job",
#         metadata=client.V1ObjectMeta(name=JOB_NAME),
#         spec=spec)

#     return job


# def create_job(api_instance, job, namespace="default"):
#     api_response = api_instance.create_namespaced_job(
#         body=job,
#         namespace=namespace)
#     print("Job created. status='%s'" % str(api_response.status))
#     get_job_status(api_instance)



# def get_job_status(api_instance):
#     job_completed = False
#     while not job_completed:
#         api_response = api_instance.read_namespaced_job_status(
#             name=JOB_NAME,
#             namespace=namespace)
#         if api_response.status.succeeded is not None or \
#                 api_response.status.failed is not None:
#             job_completed = True
#         sleep(1)
#         print("Job status='%s'" % str(api_response.status))


# def delete_job(api_instance):
#     api_response = api_instance.delete_namespaced_job(
#         name=JOB_NAME,
#         namespace=namespace,
#         body=client.V1DeleteOptions(
#             propagation_policy='Foreground',
#             grace_period_seconds=5))
#     print("Job deleted. status='%s'" % str(api_response.status))


