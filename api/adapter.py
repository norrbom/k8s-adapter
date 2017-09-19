from kubernetes import client

class Api(object):
    def factory(self, kind):
        if kind == 'Service':
            api_instance = client.CoreV1Api()
            api_instance = Adapter(api_instance, **{
                'read_namespaced_resource': api_instance.read_namespaced_service,
                'list_namespaced_resource': api_instance.list_namespaced_service,
                'create_namespaced_resource': api_instance.create_namespaced_service,
                'patch_namespaced_resource': api_instance.patch_namespaced_service
            })
        elif kind == 'ServiceAccount':
            api_instance = client.CoreV1Api()
            api_instance = Adapter(api_instance, **{
                'read_namespaced_resource': api_instance.read_namespaced_service_account,
                'list_namespaced_resource': api_instance.list_namespaced_service_account,
                'create_namespaced_resource': api_instance.create_namespaced_service_account,
                'patch_namespaced_resource': api_instance.patch_namespaced_service_account
            })
        elif kind == 'Deployment':
            api_instance = client.AppsV1beta1Api()
            api_instance = Adapter(api_instance, **{
                'read_namespaced_resource': api_instance.read_namespaced_deployment,
                'list_namespaced_resource': api_instance.list_namespaced_deployment,
                'create_namespaced_resource': api_instance.create_namespaced_deployment,
                'patch_namespaced_resource': api_instance.patch_namespaced_deployment
            })
        elif kind == 'ClusterRole':
            api_instance = client.RbacAuthorizationV1beta1Api()
            api_instance = Adapter(api_instance, **{
                'read_resource': api_instance.read_cluster_role,
                'create_resource': api_instance.create_cluster_role,
                'patch_resource': api_instance.patch_cluster_role
            })
        elif kind == 'Role':
            api_instance = client.RbacAuthorizationV1beta1Api()
            api_instance = Adapter(api_instance, **{
                'read_namespaced_resource': api_instance.read_namespaced_role,
                'create_namespaced_resource': api_instance.create_namespaced_role,
                'patch_namespaced_resource': api_instance.patch_namespaced_role
            })
        elif kind == 'RoleBinding':
            api_instance = client.RbacAuthorizationV1beta1Api()
            api_instance = Adapter(api_instance, **{
                'read_namespaced_resource': api_instance.read_namespaced_role_binding,
                'create_namespaced_resource': api_instance.create_namespaced_role_binding,
                'patch_namespaced_resource': api_instance.patch_namespaced_role_binding
            })
        elif kind == 'ClusterRoleBinding':
            api_instance = client.RbacAuthorizationV1beta1Api()
            api_instance = Adapter(api_instance, **{
                'read_resource': api_instance.read_cluster_role_binding,
                'create_resource': api_instance.create_cluster_role_binding,
                'patch_resource': api_instance.patch_cluster_role_binding
            })
        elif kind == 'StatefulSet':
            api_instance = client.AppsV1beta1Api()
            api_instance = Adapter(api_instance, **{
                'read_namespaced_resource': api_instance.read_namespaced_stateful_set,
                'list_namespaced_resource': api_instance.list_namespaced_stateful_set,
                'create_namespaced_resource': api_instance.create_namespaced_stateful_set,
                'patch_namespaced_resource': api_instance.patch_namespaced_stateful_set
            })
        else:
            # TODO: implement all resource kinds
            raise TypeError('kind {} not implemented'.format(kind))
        return api_instance


class Adapter(object):
    """
    Adapts an object by replacing methods.
    Usage:
    api_instance = AppsV1beta1Api
    api_instance = Adapter(api_instance, dict(list_namespaced_resource=api_instance.list_namespaced_deployment))
    """

    def __init__(self, obj, **adapted_methods):
        """We set the adapted methods in the object's dict"""
        self.obj = obj
        self.__dict__.update(adapted_methods)

    def __getattr__(self, attr):
        """All non-adapted calls are passed to the object"""
        return getattr(self.obj, attr)

    def original_dict(self):
        """Print original object dict"""
        return self.obj.__dict__