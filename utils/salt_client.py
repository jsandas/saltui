import requests

try:
    import salt.config
    import salt.client
except ImportError:
    pass

from django.conf import settings

class local_client():
    """
    Interact with saltmaster using LocalClient()
    """
    def __init__(self):
        try:
            self.client = salt.client.LocalClient()
        except Exception as e:
            print('salt package not found')

    def cmd(self, target, function, args=[], kwarg=None, **kwargs):
        ret = self.client.cmd(tgt=target, fun=function, arg=args, kwarg=kwarg, **kwargs)

        return ret

class api_client():
    """
    Interact with saltmaster using Salt API
    """ 
    def __init__(self):
        self.host = settings.SALT_API_HOST
        self.username = settings.SALT_API_USER
        self.password = settings.SALT_API_PASS
        self.auth_type = settings.SALT_API_EAUTH
        self.client = requests.Session()

        self.client.post(self.host + '/login', json={
            'username': self.username,
            'password': self.password,
            'eauth': self.auth_type,
        }, verify=False)

        print('logged in')

    def cmd(self, target, function, args=[], kwarg=None, **kwargs):
        resp = self.client.post(self.host, json=[{
            'client': 'local',
            'tgt': target,
            'fun': function,
            'arg': args,
            'kwarg': kwarg,
            **kwargs
        }], verify=False)

        return resp.json()['return'][0]