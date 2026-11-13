#!/usr/bin/env python3
"""Validate a repository's modular-monolith composition profile without executing products."""
from __future__ import annotations
import argparse,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PROFILE=ROOT/"ARCHITECTURE_PROFILE.json"
SCHEMA="bboroski.modular-monolith-profile.v1"
MODES={"modular-monolith","static-library","static-web","freestanding-kernel","host-tool","research-workstream","scaffold","design-specification"}
MATURITY={"experimental-alpha","host-diagnostics","host-tested-core","static-portal","early-kernel-bringup","architecture-proposal","experimental-foundation","workspace-prototype","scaffold-only","design-specification"}
STATUSES={"implemented","partial","planned","specified","not-present"}
INTEGRATION={"in-process","static-link","versioned-contract","metadata-only","isolated-target","planned","not-applicable"}
SLUG=re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
def validate(data,root=ROOT):
 e=[]
 if not isinstance(data,dict):return ["profile root must be an object"]
 if data.get("schema_version")!=SCHEMA:e.append("unsupported schema_version")
 if data.get("project")!=root.name:e.append(f"project must match repository directory {root.name!r}")
 if data.get("maturity") not in MATURITY:e.append("unsupported maturity")
 a=data.get("architecture")
 if not isinstance(a,dict):e.append("architecture must be an object");a={}
 if a.get("mode") not in MODES:e.append("unsupported architecture.mode")
 for k in ("scope","runtime_boundary","composition_rule"):
  if not isinstance(a.get(k),str) or not a[k].strip():e.append(f"architecture.{k} is required")
 for k in ("entrypoints","components","dependencies","preserved_boundaries","forbidden_composition","build_profiles","gaps"):
  if not isinstance(data.get(k),list):e.append(f"{k} must be an array")
 paths=[]
 for i,x in enumerate(data.get("entrypoints",[]) if isinstance(data.get("entrypoints"),list) else []):
  if not isinstance(x,dict) or not isinstance(x.get("path"),str) or not x.get("kind"):e.append(f"entrypoints[{i}] requires path and kind");continue
  paths.append((f"entrypoints[{i}]",x["path"]))
 seen=set()
 for i,x in enumerate(data.get("components",[]) if isinstance(data.get("components"),list) else []):
  if not isinstance(x,dict):e.append(f"components[{i}] must be an object");continue
  ident=x.get("id")
  if not isinstance(ident,str) or not SLUG.fullmatch(ident):e.append(f"components[{i}].id must be a lowercase slug")
  elif ident in seen:e.append(f"duplicate component id: {ident}")
  seen.add(ident)
  if not isinstance(x.get("responsibility"),str) or not x["responsibility"].strip():e.append(f"components[{i}].responsibility is required")
  if x.get("status") not in STATUSES:e.append(f"components[{i}].status is unsupported")
  if x.get("integration") not in INTEGRATION:e.append(f"components[{i}].integration is unsupported")
 for i,x in enumerate(data.get("dependencies",[]) if isinstance(data.get("dependencies"),list) else []):
  if not isinstance(x,dict) or not x.get("project") or not x.get("relationship"):e.append(f"dependencies[{i}] requires project and relationship");continue
  if not isinstance(x.get("runtime_dependency"),bool):e.append(f"dependencies[{i}].runtime_dependency must be boolean")
 for k in ("preserved_boundaries","forbidden_composition","gaps"):
  v=data.get(k,[])
  if isinstance(v,list) and any(not isinstance(z,str) or not z.strip() for z in v):e.append(f"{k} entries must be non-empty strings")
 pids=set()
 for i,x in enumerate(data.get("build_profiles",[]) if isinstance(data.get("build_profiles"),list) else []):
  if not isinstance(x,dict):e.append(f"build_profiles[{i}] must be an object");continue
  ident=x.get("id")
  if not isinstance(ident,str) or not SLUG.fullmatch(ident):e.append(f"build_profiles[{i}].id must be a lowercase slug")
  elif ident in pids:e.append(f"duplicate build profile id: {ident}")
  pids.add(ident)
  if x.get("status") not in {"declared","blocked","not-applicable","not-yet-verified"}:e.append(f"build_profiles[{i}].status is unsupported")
  if not isinstance(x.get("commands"),list) or any(not isinstance(z,str) or not z.strip() for z in x.get("commands",[])):e.append(f"build_profiles[{i}].commands must be an array")
  if not isinstance(x.get("evidence"),list):e.append(f"build_profiles[{i}].evidence must be an array")
  else:
   for j,path in enumerate(x["evidence"]):
    if not isinstance(path,str):e.append(f"build_profiles[{i}].evidence[{j}] must be a path");continue
    paths.append((f"build_profiles[{i}].evidence[{j}]",path))
 for field,path in paths:
  candidate=(root/path).resolve()
  if not candidate.is_relative_to(root.resolve()):e.append(f"{field} escapes repository root: {path}")
  elif not candidate.exists():e.append(f"{field} does not exist: {path}")
 return e
def self_test():
 import tempfile
 sample={"schema_version":SCHEMA,"project":"fixture","maturity":"scaffold-only","architecture":{"mode":"scaffold","scope":"fixture","runtime_boundary":"none","composition_rule":"no executable composition claimed"},"entrypoints":[],"components":[],"dependencies":[],"preserved_boundaries":["No code execution"],"forbidden_composition":["No inferred runtime"],"build_profiles":[{"id":"metadata-only","status":"declared","commands":[],"evidence":["README.md"]}],"gaps":["Implementation pending"]}
 with tempfile.TemporaryDirectory() as tmp:
  root=Path(tmp);(root/"README.md").write_text("fixture",encoding="utf-8")
  assert not validate(sample,root)
  bad=dict(sample);bad["schema_version"]="invalid";assert validate(bad,root)
 print("Architecture profile validator self-test passed.")
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("--self-test",action="store_true");a=p.parse_args()
 if a.self_test:self_test()
 try:data=json.loads(PROFILE.read_text(encoding="utf-8"))
 except (OSError,json.JSONDecodeError) as exc:print(f"ERROR: {exc}",file=sys.stderr);return 2
 errors=validate(data)
 if errors:
  for x in errors:print(f"ERROR: {x}")
  print(f"Architecture profile check failed for {ROOT.name}.");return 1
 print(f"Architecture profile check passed for {ROOT.name}: {len(data['components'])} components, {len(data['build_profiles'])} build profiles.");return 0
if __name__=="__main__":raise SystemExit(main())
