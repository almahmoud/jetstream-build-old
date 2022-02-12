#!/bin/usr/python3
from argparse import ArgumentParser

from kubernetes import client, config, utils

parser = ArgumentParser()
parser.add_argument("-p", "--package", dest="package",
                    help="Package name")
parser.add_argument("-n", "--namespace", dest="namespace",
                    help="Namespace in which to dispatch job")
parser.add_argument("-s", "--status-file", dest="statusfile",
                    help="File in which to report status")
parser.add_argument("-l", "--log-file", dest="logfile",
                    help="File in which to output logs")


args = parser.parse_args()

config.load_kube_config()
batch_v1 = client.BatchV1Api()
core_v1 = client.CoreV1Api()


def get_logs(job_name, namespace):
    job_def = batch_v1.read_namespaced_job(name=job_name, namespace=namespace)
    controllerUid = job_def.metadata.labels["controller-uid"]
    pods_list = core_v1.list_namespaced_pod(namespace=namespace, label_selector=f'controller-uid={controllerUid}', timeout_seconds=10)
    pod_name = pods_list.items[0].metadata.name
    try:
        pod_log_response = core_v1.read_namespaced_pod_log(name=pod_name, namespace=namespace, _return_http_data_only=True, _preload_content=False)
        return pod_log_response.data.decode("utf-8")
    except client.rest.ApiException as e:
        print("Exception when calling CoreV1Api->read_namespaced_pod_log: %s\n" % e)


def write_logs_and_delete(job_name, namespace, logfile):
    with open(logfile, 'w') as f:
        f.write(get_logs(job_name, namespace))
    api_response = batch_v1.delete_namespaced_job(
        name=f'{args.package.lower()}-build',
        namespace=args.namespace,
        body=client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5))
    print("Job deleted. status='%s'" % str(api_response.status))


api_response = batch_v1.read_namespaced_job_status(
    name=f'{args.package.lower()}-build',
    namespace=args.namespace)
if api_response.status.succeeded is not None:
    with open(args.statusfile, 'w') as f:
        f.write("built")
    write_logs_and_delete(job_name=f'{args.package.lower()}-build',
                          namespace=args.namespace,
                          logfile=args.logfile)
elif api_response.status.failed is not None:
    with open(args.statusfile, 'w') as f:
        f.write("failedbuild")
    write_logs_and_delete(job_name=f'{args.package.lower()}-build',
                          namespace=args.namespace,
                          logfile=args.logfile)

else:
    with open(args.statusfile, 'w') as f:
        f.write("runningbuild")



