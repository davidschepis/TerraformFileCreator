import subprocess
import json
import webbrowser
f = open("./kube-manifests/services.json")
services = json.load(f)
ip = services['items'][1]['status']['loadBalancer']['ingress'][0]['ip']
c = webbrowser.get('chrome')
c.open(ip)