from src.zerorest.providers import Entra, EntraApp
from src.zerorest.api import SharePoint
from src.zerorest import HTTPClient
tenant = "00000000-0000-0000-0000-000000000000"
client_id = "00000000-0000-0000-0000-000000000000"
client_secret = "Smn8Q~w40vF7uJteovbi5_PSVgN0eYil-GZRcduQ" # User Authentication
client = (client_id, client_secret)
p = Entra(tenant=tenant, client=client, scope="sites.read.all", open=False) # User Authentication
auth = p.authenticate()
c = HTTPClient(auth=auth, base_url="https://graph.microsoft.com/v1.0")
c.set_header("Content-Type", "application/json")
s = SharePoint(client=c)
sites = (s.get_me_sites().json()["value"])
print(sites)