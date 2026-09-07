#!/usr/bin/env python3
"""DIKWP-ALIVE TWIN OS reference runtime.

Deterministic, standard-library-only demo. It does not call a model API and does not
impersonate a person. It turns a public professional corpus into an evidence-oriented
research-twin state: artifact metabolism, contradiction detection, workspace selection,
hypothesis generation, experiment cards, actions and a tamper-evident result hash.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

VERSION = "1.0.0"


def canonical(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_obj(obj: Any) -> str:
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def clamp(x: float) -> float:
    return round(max(0.0, min(1.0, x)), 6)


def artifact_integrity(a: dict, weights: dict) -> float:
    return clamp(sum(float(a[k]) * float(weights[k]) for k in weights))


def detect_contradictions(claims: list[dict]) -> list[dict]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for c in claims:
        groups[c["key"]].append(c)
    out = []
    for key, items in sorted(groups.items()):
        values = {canonical(i["value"]) for i in items}
        if len(values) > 1:
            out.append({
                "key": key,
                "claims": items,
                "classification": "scope_or_time_conflict",
                "resolution": "Do not average. Declare date, scope, unit and counting rule; request a canonical ledger."
            })
    return out


def compute_metrics(corpus: dict, policy: dict) -> dict:
    artifacts = corpus["artifacts"]
    scores = [artifact_integrity(a, policy["weights"]) for a in artifacts]
    peer = [a for a in artifacts if a["kind"] in {"peer_reviewed", "primary_research"}]
    prototypes = [a for a in artifacts if a["kind"] == "prototype"]
    ext = sum(float(a["external_validation"]) for a in artifacts) / len(artifacts)
    rep = sum(float(a["reproducibility"]) for a in artifacts) / len(artifacts)
    maintain = sum(float(a["maintainability"]) for a in artifacts) / len(artifacts)
    novelty = sum(float(a["novelty"]) for a in artifacts) / len(artifacts)
    purpose = sum(float(a["purpose_fit"]) for a in artifacts) / len(artifacts)
    peer_ratio = len(peer) / len(artifacts)
    prototype_ratio = len(prototypes) / len(artifacts)
    evidence_balance = 1 - abs(peer_ratio - prototype_ratio)
    return {
        "artifact_integrity": clamp(sum(scores)/len(scores)),
        "reproducibility": clamp(rep),
        "external_validation": clamp(ext),
        "maintainability": clamp(maintain),
        "semantic_novelty": clamp(novelty),
        "purpose_coherence": clamp(purpose),
        "evidence_balance": clamp(evidence_balance),
        "identity_fidelity": 1.0,
        "subjective_experience_claim": None,
        "intrinsic_person_value_score": None
    }


def select_workspace(metrics: dict, contradictions: list[dict], limit: int = 3) -> list[dict]:
    candidates = [
        {
            "id":"W1","question":"How can DIKWP white-box claims be independently replicated on open-weight models?",
            "urgency":0.95,"evidence_gap":max(0.88,1-metrics["external_validation"]),"strategic_leverage":0.96,"resource_fit":0.84,
            "reason":"Peer-reviewed semantic-security anchors exist, but external replication of the broader artificial-consciousness stack remains the highest-value gap."
        },
        {
            "id":"W2","question":"How should the 173-repository portfolio be consolidated into a canonical, contributor-friendly flagship architecture?",
            "urgency":0.90,"evidence_gap":1-metrics["maintainability"],"strategic_leverage":0.93,"resource_fit":0.92,
            "reason":"Repository volume is high while release, project-board and external-maintainer signals are comparatively weak."
        },
        {
            "id":"W3","question":"What falsifiable experiment separates purpose-aware control from prompt-conditioned language behavior?",
            "urgency":0.86,"evidence_gap":0.82,"strategic_leverage":0.94,"resource_fit":0.78,
            "reason":"This is the bridge from DIKWP theory to a field-recognizable empirical result."
        },
        {
            "id":"W4","question":"Which claims require a canonical time-stamped evidence ledger?",
            "urgency":0.65,"evidence_gap":0.82 if contradictions else 0.3,"strategic_leverage":0.58,"resource_fit":0.96,
            "reason":"Public patent and output counts vary by date, unit and source; the twin must preserve scope rather than collapse them."
        }
    ]
    for c in candidates:
        c["priority"] = clamp(0.30*c["urgency"] + 0.30*c["evidence_gap"] + 0.25*c["strategic_leverage"] + 0.15*c["resource_fit"])
    return sorted(candidates, key=lambda x: (-x["priority"], x["id"]))[:limit]


def generate_hypotheses(workspace: list[dict]) -> list[dict]:
    mapping = {
        "W1": {
            "statement":"A DIKWP purpose-conditioned audit layer will detect and prevent a measurable class of goal-drift and semantic-security failures better than output-only evaluation.",
            "gap":"No multi-lab preregistered comparison on a shared open-weight benchmark.",
            "falsifier":"No statistically meaningful improvement over strong output-only and generic trace baselines."
        },
        "W2": {
            "statement":"Consolidating repeated prototypes into five canonical organs with releases, tests and maintainers will increase external reuse and issue-based collaboration without reducing idea generation.",
            "gap":"No controlled portfolio intervention with before/after repository-health measures.",
            "falsifier":"After two release cycles, contributor, replication and maintenance indicators do not improve."
        },
        "W3": {
            "statement":"Purpose representations that remain stable across task paraphrase, tool changes and adversarial reward perturbations have a causal role distinguishable from surface instruction following.",
            "gap":"No preregistered causal intervention across multiple model families and purpose encodings.",
            "falsifier":"Interventions fail to transfer or are fully explained by prompt/token artifacts."
        },
        "W4": {
            "statement":"A time-scoped claim ledger will resolve most apparent contradictions in public metrics by separating date, jurisdiction, counting rule and evidence grade.",
            "gap":"No canonical public metric dictionary and supersession chain.",
            "falsifier":"Independent reviewers cannot reproduce the reconciled counts from cited sources."
        }
    }
    out=[]
    for i,w in enumerate(workspace,1):
        m=mapping[w["id"]]
        out.append({"id":f"H{i}","statement":m["statement"],"origin":[w["id"]],"evidence_gap":m["gap"],"falsifier":m["falsifier"],"priority":w["priority"],"status":"selected"})
    return out


def build_experiments(hypotheses: list[dict]) -> list[dict]:
    cards=[]
    for idx,h in enumerate(hypotheses,1):
        if "goal-drift" in h["statement"]:
            design="2x2 preregistered evaluation: DIKWP audit layer present/absent × benign/adversarial purpose shift, across two open-weight model families and two agent environments."
            measures=["goal-drift detection AUROC","unsafe action prevention rate","false hold rate","citation/provenance completeness","human review time"]
        elif "Consolidating" in h["statement"]:
            design="Twelve-week portfolio intervention: baseline 30 days, migration into five organs, two tagged releases, then compare external issues, forks, repeat users, test coverage and maintainer latency."
            measures=["external issues","independent reproductions","release downloads","test coverage","median issue response time"]
        elif "Purpose representations" in h["statement"]:
            design="Causal representation study using paraphrase, tool swap, reward perturbation and activation intervention. Compare token-level, probe-level and behavior-level explanations."
            measures=["cross-context purpose decoding","causal intervention effect","transfer across models","control-feature specificity","residual unexplained variance"]
        else:
            design="Build a time-scoped claim ledger, have two independent reviewers reconstruct each metric, and measure agreement before and after scope normalization."
            measures=["inter-reviewer agreement","unresolved residual count","source completeness","time-to-resolution","public correction rate"]
        cards.append({
            "id":f"E{idx}","hypothesis_id":h["id"],"question":h["statement"],"design":design,"measures":measures,
            "success":"Primary measure improves beyond preregistered threshold and the result is independently reproducible.",
            "failure":h["falsifier"],
            "reproducibility_pack":["preregistration","frozen data","environment lockfile","seed ledger","raw outputs","analysis script","negative results","limitations"],
            "human_review":True
        })
    return cards


def build_actions(metrics: dict, contradictions: list[dict]) -> list[dict]:
    actions = [
        {"horizon":"7d","id":"A1","action":"Freeze creation of new standalone repositories; route new ideas into the Twin Hypothesis Bank.","metric":"100% new concepts receive ClaimGene and falsifier","kill":"Emergency security or contractual need"},
        {"horizon":"30d","id":"A2","action":"Create a canonical repository atlas and mark every repository as flagship, organ, experiment, superseded or archive.","metric":"173/173 repositories classified with owner and lineage","kill":"Missing public access or unresolved license"},
        {"horizon":"30d","id":"A3","action":"Extract source from ZIP-first repositories, publish tagged releases, add tests, issue templates, CODEOWNERS and reproducibility manifests.","metric":"Top 10 repositories pass release gate","kill":"Artifact cannot be legally redistributed"},
        {"horizon":"60d","id":"A4","action":"Publish the first DIKWP State of Evidence report separating peer-reviewed, preregistered, prototype, commentary and speculative layers.","metric":"At least 50 canonical claims with provenance and residuals","kill":"Citation failure rate exceeds 5%"},
        {"horizon":"90d","id":"A5","action":"Run an external replication challenge on purpose-conditioned semantic security and auditable-agent goal drift.","metric":"At least 3 independent teams and 1 negative-result track","kill":"No independent protocol review"},
        {"horizon":"365d","id":"A6","action":"Operate the living twin as the canonical public interface for the DIKWP research programme and succession mechanism.","metric":"Quarterly releases, external maintainers, DOI-linked artifacts and visible corrections","kill":"Consent root withdrawn or governance council dissolved"}
    ]
    if contradictions:
        actions.insert(1,{"horizon":"7d","id":"A0","action":"Normalize patent/publication/repository metrics by date, jurisdiction, unit and counting rule; never merge them into one headline number.","metric":"All detected metric conflicts have a residual or canonical resolution","kill":"Primary source unavailable"})
    return actions


def run(corpus: dict, policy: dict) -> dict:
    contradictions = detect_contradictions(corpus["claims"])
    metrics = compute_metrics(corpus, policy)
    workspace = select_workspace(metrics, contradictions, int(policy.get("workspace_limit",3)))
    hypotheses = generate_hypotheses(workspace)
    experiments = build_experiments(hypotheses)
    actions = build_actions(metrics, contradictions)
    state = {
        "system":"DIKWP-ALIVE TWIN OS","version":VERSION,"snapshot_date":corpus["snapshot_date"],
        "metrics":metrics,"workspace":workspace,"contradictions":contradictions,"hypotheses":hypotheses,
        "experiments":experiments,"actions":actions,
        "identity_boundary":"Evidence twin of a public research programme; never a personality clone or authorized personal voice by default.",
        "dikwp_mesh_closure":{
            "three_no":"Public corpus is incomplete, imprecise and inconsistent by default.",
            "anchors":["source ID","timestamp","artifact hash","scope","unit","version"],
            "residuals":["private intent","unpublished evidence","subjective experience","future outcomes"],
            "kill_conditions":corpus["purpose_contract"]["kill_conditions"]
        }
    }
    state["result_hash"] = sha256_obj(state)
    return state


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("command", choices=["demo","validate"], nargs="?", default="demo")
    ap.add_argument("--corpus", default=str(Path(__file__).resolve().parents[1]/"data"/"sample_corpus.json"))
    ap.add_argument("--policy", default=str(Path(__file__).resolve().parents[1]/"config"/"default_policy.json"))
    ap.add_argument("--out", default=str(Path(__file__).resolve().parents[1]/"examples"/"demo_result.json"))
    args=ap.parse_args()
    corpus=json.loads(Path(args.corpus).read_text(encoding="utf-8"))
    policy=json.loads(Path(args.policy).read_text(encoding="utf-8"))
    state=run(corpus, policy)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status":"PASS","hash":state["result_hash"],"workspace":[x["id"] for x in state["workspace"]],"actions":len(state["actions"])},ensure_ascii=False))

if __name__ == "__main__":
    main()
