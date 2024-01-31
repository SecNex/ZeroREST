from src.zerorest.providers import Entra, EntraApp
# Authentication via Client Credentialsssh
from src.zerorest.api import SharePoint
from src.zerorest import HTTPClient
tenant = "00000000-0000-0000-0000-000000000000"
client_id = "00000000-0000-0000-0000-000000000000"
client_secret = "chJ8Q~v8M.NBfgIGno2wQyjnexfHO37jEX3hzc_q" # App Authentication
client = (client_id, client_secret)
p = EntraApp(tenant=tenant, client=client)
auth = p.authenticate()
c = HTTPClient(auth=auth, base_url="https://graph.microsoft.com/v1.0")
c.set_header("Content-Type", "application/json")
s = SharePoint(client=c)
sites = (s.get_me_sites().json()["value"])
print(sites)