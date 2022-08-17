import paramiko
import re

#README

#To create service accounts before registering with PPDM

username = "administrator"
password = "emclegato"
fh = open('kmasters.txt')
for f in fh:
    host = f.rstrip()
    print("\033[1m" + host + "\033[0m")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password)


    def execommand(thecommand):
        stdina, stdouta, stderra = client.exec_command(thecommand)
        print(thecommand)
        for i in stdouta.readlines():
            print("{}".format(i))
        for i in stderra.readlines():
            print('\x1b[1;31m' + i + '\x1b[0m')

    create_accnt = "kubectl create serviceaccount dashboard -n default"
    execommand(create_accnt)

    create_crb = "kubectl create clusterrolebinding dashboard-admin -n default --clusterrole=cluster-admin --serviceaccount=default:dashboard"

    execommand(create_crb)
    print("GET TOKEN : {}".format(host))

    get_token = "kubectl get secret $(kubectl get serviceaccount dashboard -n default -o jsonpath=\"{.secrets[0].name}\") -o jsonpath=\"{.data.token}\" | base64 --decode"
    execommand(get_token)

    # get_ns = "kubectl get namespace | grep powerprotect | awk '{print$1}'"
    # execommand(get_ns)
    # namespace = []
    # namespaces = execommand(get_ns)
    # print(namespaces)
    # if namespaces is None:
    #     print("No powerprotect namespace")
    # else:
    #     for ns in namespaces:
    #         type_of_deployment = ["pod"]
    #         for type in type_of_deployment:
    #             get_deployments = "kubectl get {} -n {} | grep -v \"NAME\" | awk '{{print$1}}'".format(type.rstrip(),
    #                                                                                                    ns.rstrip())
    #             apps = execommand(get_deployments)
    #             for app in apps:
    #                 print("\033[1m" + "DELETE {} OF TYPE {} FROM NAMESPACE {}".format(app.rstrip(), type.rstrip(),
    #                                                                                   ns.rstrip()) + "\033[0m")
    #                 delete_deployments = "kubectl delete {} {} -n {}".format(type.rstrip(), app.rstrip(), ns.rstrip())
    #                 execommand(delete_deployments)
