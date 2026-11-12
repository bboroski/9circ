#!/usr/bin/env python3
"""Validate the repository-local Engineering Standard profile (stdlib only)."""
from __future__ import annotations
import json, os, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PROFILE=ROOT/".engineering"/"profile.json"
GATES={"profile-validation","native-project-checks","architecture-and-compatibility-review","security-and-privacy-review","documentation-review","human-review","target-qualification-when-applicable"}
STATUSES={"PROPOSED","PLANNED","IMPLEMENTED","TESTED","VERIFIED","MERGED","RELEASED","BLOCKED"}
def main():
    errors=[]
    for p in (ROOT/"ENGINEERING_STANDARD.md",PROFILE,ROOT/"README.md"):
        if not p.is_file(): errors.append(f"missing {p.relative_to(ROOT)}")
    if errors: print("\n".join("FAIL: "+e for e in errors),file=sys.stderr); return 1
    try: d=json.loads(PROFILE.read_text(encoding="utf-8"))
    except (OSError,UnicodeError,json.JSONDecodeError) as e: print(f"FAIL: profile JSON: {e}",file=sys.stderr); return 1
    if d.get("schema_version")!=1 or d.get("standard_id")!="PERSONA-ENG-STD": errors.append("unsupported schema_version or standard_id")
    repo=d.get("repository"); expected=os.getenv("GITHUB_REPOSITORY")
    if not isinstance(repo,str) or "/" not in repo: errors.append("repository must be owner/name")
    if expected and repo!=expected: errors.append(f"profile repository {repo!r} != {expected!r}")
    project=d.get("project")
    if not isinstance(project,dict) or any(not isinstance(project.get(k),str) or not project[k].strip() for k in ("domain","mission","maturity")): errors.append("project must define non-empty domain, mission, maturity")
    arch=d.get("architecture")
    if not isinstance(arch,dict) or arch.get("preserve_existing_boundaries") is not True: errors.append("architecture must preserve existing boundaries")
    else:
        for k in ("primary_technologies","explicit_non_goals"):
            v=arch.get(k)
            if not isinstance(v,list) or not v or any(not isinstance(x,str) or not x.strip() for x in v): errors.append(f"architecture.{k} must be a non-empty string array")
    s=d.get("safety_boundaries")
    if not isinstance(s,list) or not s or any(not isinstance(x,str) or not x.strip() for x in s): errors.append("safety_boundaries must be a non-empty string array")
    n=d.get("native_validation")
    if not isinstance(n,dict) or n.get("status") not in {"defined","discovery-required","target-evidence-pending"} or not isinstance(n.get("commands"),list) or any(not isinstance(x,str) or not x.strip() for x in n.get("commands",[])): errors.append("native_validation must contain status and command array")
    gs=d.get("required_gates")
    if not isinstance(gs,list) or not GATES.issubset(set(gs or [])): errors.append("required_gates are incomplete")
    m=d.get("merge_policy")
    if not isinstance(m,dict) or m.get("pull_request_required") is not True or m.get("bypass_required_checks") is not False or m.get("release_requires_separate_qualification") is not True: errors.append("merge_policy violates standard")
    st=d.get("status_vocabulary")
    if not isinstance(st,list) or not STATUSES.issubset(set(st or [])): errors.append("status_vocabulary is incomplete")
    if errors: print("\n".join("FAIL: "+e for e in errors),file=sys.stderr); return 1
    print(f"ENGINEERING STANDARD PASS: {repo}")
    print("Profile validated; native builds, tests, reviews and target qualification remain separate.")
    return 0
if __name__=="__main__": raise SystemExit(main())
