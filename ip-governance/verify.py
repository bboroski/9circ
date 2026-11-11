#!/usr/bin/env python3
"""IP governance manifest validator; Python standard library only."""
import hashlib, json, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
HEX64=re.compile(r"^[0-9a-f]{64}$")
def fail(message):
    print("IP governance: ERROR: "+message,file=sys.stderr); raise SystemExit(1)
def main():
    try: data=json.loads((ROOT/"ip-governance/manifest.json").read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc: fail("cannot read manifest: "+str(exc))
    required={"schema_version","object_id","repository","rights","artifacts"}
    if required-data.keys(): fail("missing fields: "+", ".join(sorted(required-data.keys())))
    if data["schema_version"]!="1.0": fail("unsupported schema_version")
    repo=data["repository"]
    if not isinstance(repo,str) or not repo.startswith("https://github.com/"): fail("repository must be canonical GitHub HTTPS URL")
    if data["object_id"]!="urn:uoi:github:"+repo.removeprefix("https://github.com/").rstrip("/"): fail("object_id does not match repository locator")
    rights=data["rights"]
    if not isinstance(rights,dict) or not isinstance(rights.get("license_expression"),str): fail("rights.license_expression must be a string")
    if not isinstance(rights.get("rights_holders"),list) or not isinstance(data["artifacts"],list): fail("rights_holders and artifacts must be arrays")
    seen=set()
    for item in data["artifacts"]:
        if not isinstance(item,dict): fail("artifact entry must be an object")
        path,digest=item.get("path"),item.get("sha256")
        if not isinstance(path,str) or not path or path in seen: fail("invalid or duplicate artifact path")
        seen.add(path); rel=Path(path)
        if rel.is_absolute() or ".." in rel.parts: fail("unsafe artifact path: "+path)
        if not isinstance(digest,str) or not HEX64.fullmatch(digest): fail("invalid SHA-256: "+path)
        target=(ROOT/rel).resolve()
        if ROOT.resolve() not in target.parents or not target.is_file(): fail("missing or unsafe artifact: "+path)
        if hashlib.sha256(target.read_bytes()).hexdigest()!=digest: fail("SHA-256 mismatch: "+path)
    print("IP governance: OK — %d artifact(s); %s"%(len(data["artifacts"]),data["object_id"]))
    return 0
if __name__=="__main__": raise SystemExit(main())
