from ...http import HTTPClient, Param

class SharePoint:
    def __init__(self, client: HTTPClient):
        self.client = client

    def get_site(self, site: str):
        return self.client.get(f"/sites/{site}")
    
    def get_sites(self):
        return self.client.get("/sites")
    
    def get_drive(self, site: str, drive: str):
        return self.client.get(f"/sites/{site}/drives/{drive}")

    def get_drives(self, site: str):
        return self.client.get(f"/sites/{site}/drives")
    
    def get_item_children(self, site: str, drive: str, item: str):
        return self.client.get(f"/sites/{site}/drives/{drive}/items/{item}/children")

    def get_items(self, site: str, drive: str, path: str = None):
        if path is None:
            return self.client.get(f"/drives/{drive}/root/children")
        else:
            return self.client.get(f"/drives/{drive}/root:/{path}:/children")
        
    def get_items_recursive(self, site: str, drive: str, path: str = None, item: str = None) -> dict:
        items = []
        result = []
        if item is None:
            result = self.get_items(site, drive, path).json()["value"]
        else:
            result = self.get_item_children(site, drive, item).json()["value"]
        for i in result:
            item_path = None
            if i["parentReference"]["path"] is not None:
                # Replace /drives/{drive}/root: with /
                if i["parentReference"]["path"].startswith(f"/drives/{drive}/root:"):
                    item_path = i["parentReference"]["path"].replace(f"/drives/{drive}/root:", "")
                item_path = item_path + "/" + i["name"]
            itemObject = {
                "id": i["id"],
                "name": i["name"],
                "type": "file",
                "children": [],
                "path": item_path
            }
            try:
                if i["folder"] is not None:
                    itemObject["type"] = "folder"
            except KeyError:
                pass
            if itemObject["type"] == "folder":
                itemObject["children"] = self.get_items_recursive(site, drive, None, i["id"])
            permissions = self.get_permissions(site, drive, i["id"]).json()["value"]
            itemObject["permissions"] = permissions
            itemObject["permissions_count"] = len(permissions)
            items.append(itemObject)
        return items
    
    def get_permissions(self, site: str, drive: str, item: str):
        return self.client.get(f"/sites/{site}/drives/{drive}/items/{item}/permissions")
    
    def __has_access(self, permissions: dict) -> str:
        value = ""
        for permission in permissions:
            p = permission["grantedToV2"]["user"]["email"]
            value += p + ","
        return value[:-1]

    def get_groups(self, site: str):
        p = Param("expand", "fields")
        result = self.client.get(f"/sites/{site}/lists/User Information List/items?expand=fields", params=[p]).json()
        print(result)
        return result