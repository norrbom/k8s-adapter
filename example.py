import logging
import sys
import yaml
from argparse import ArgumentParser

from api.adapter import Api
from kubernetes import config
from kubernetes.client.rest import ApiException

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

class Client(object):
    def __init__(self, config_file, context, namespace):
        """ Constructor """
        config.load_kube_config(config_file, context)
        self.namespace = namespace

    def deploy(self, doc):

        name = doc.get('metadata').get('name')
        kind = doc.get('kind')

        api_instance = Api().factory(kind)

        found = True
        try:
            if api_instance.__dict__.get('read_namespaced_resource'):
                found = api_instance.read_namespaced_resource(name, self.namespace)
            else:
                found = api_instance.read_resource(name)
        except ApiException as e:
            if e.status == 404:
                found = False
            else:
                logger.error("Exception when calling read_namespaced_resource: %s\n" % e)
                raise e

        if not found:
            logger.info('creating resource: {}'.format(name))
            if api_instance.__dict__.get('create_namespaced_resource'):
                api_instance.create_namespaced_resource(self.namespace, doc)
            else:
                api_instance.create_resource(doc)
        else:
            logger.info('resource already exist, applying patch to {}'.format(name))
            if api_instance.__dict__.get('patch_namespaced_resource'):
                api_instance.patch_namespaced_resource(name, self.namespace, doc)
            else:
                api_instance.patch_resource(name, doc)

def process_file(client, file, namespace, command):
    """
    :param file: YAML file to parse
    :return: list of manifests as Python objects
    """
    documents = yaml.load_all(open(file, 'r'))
    for i, doc in enumerate(documents):
        if command == 'deploy':
            client.deploy(doc)
        else:
            raise ValueError('[error] unknown command {}'.format(command))
    logger.info('{} documents processed in {}'.format(i + 1, file))
    return documents

def main(config_file, context, namespace, file, command):
    client = Client(config_file=config_file, context=context, namespace=namespace)
    process_file(client, file, namespace, command)


if __name__ == '__main__':
    div = '---------------------------------------------'
    parser = ArgumentParser(description='Pipeline Deployment Controller')
    parser.add_argument("-k", "--kubeconfig", dest="kubeconfig", help="kube config file", required=True)
    parser.add_argument("-x", "--context", dest="context", help="kube config context", required=True)
    parser.add_argument("-f", "--file", dest="filename", help="YAML manifest file", required=True)
    parser.add_argument("-n", "--namespace", dest="namespace", help="cluster namespace", required=True)
    parser.add_argument("-c", "--command", dest="command", help="the command to run", required=True)
    args = parser.parse_args()

    try:
        logger.info(div)
        logger.info('processing file {}'.format(args.filename))
        main(config_file=args.kubeconfig, context=args.context, namespace=args.namespace, file=args.filename, command=args.command)
    except Exception as e:
        logger.error('An error occurred while processing {}, aborting!'.format(args.filename))
        logger.error(e)
        sys.exit(1)
