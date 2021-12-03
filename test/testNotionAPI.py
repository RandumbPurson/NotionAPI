import NotionAPI as n

auth_key = "secret_emSRLcKVXYCmk4x7KPybcElNrgl08FweoLleURa2upq"
version = "2021-05-13"

notion = n.NotionAPI(auth_key, version)

id_root = "55674e0b64054b3d862699f788d80378"
raw_root = notion.get_element(n.PAGE, element_id = id_root)
pg_root = n.Page(raw_root["properties"])


pg_new = n.Page()
pg_new.link_notion(parent_type = n.PAGE, parent_id = id_root)
pg_new.set_title("Test3")
print(pg_new.content)
r = notion.create_page(pg_new)

print(pg_new.uuid)
