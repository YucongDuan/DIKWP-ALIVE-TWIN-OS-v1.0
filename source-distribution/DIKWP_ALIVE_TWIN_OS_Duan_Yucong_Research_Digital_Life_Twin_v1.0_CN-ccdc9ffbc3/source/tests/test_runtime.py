import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("alive", ROOT/"runtime"/"alive_twin_runtime.py")
alive=importlib.util.module_from_spec(spec); spec.loader.exec_module(alive)

class AliveTwinTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.corpus=json.loads((ROOT/"data"/"sample_corpus.json").read_text(encoding="utf-8"))
        cls.policy=json.loads((ROOT/"config"/"default_policy.json").read_text(encoding="utf-8"))
        cls.state=alive.run(cls.corpus, cls.policy)

    def test_deterministic(self):
        self.assertEqual(self.state["result_hash"], alive.run(self.corpus,self.policy)["result_hash"])
    def test_identity_boundary(self):
        self.assertIn("never a personality clone", self.state["identity_boundary"])
    def test_no_person_value_score(self):
        self.assertIsNone(self.state["metrics"]["intrinsic_person_value_score"])
    def test_no_subjective_claim(self):
        self.assertIsNone(self.state["metrics"]["subjective_experience_claim"])
    def test_metric_range(self):
        for k,v in self.state["metrics"].items():
            if isinstance(v,float): self.assertGreaterEqual(v,0); self.assertLessEqual(v,1)
    def test_contradiction_detected(self):
        keys=[x["key"] for x in self.state["contradictions"]]
        self.assertIn("authorized_patents",keys)
    def test_workspace_limit(self):
        self.assertEqual(len(self.state["workspace"]),3)
    def test_replication_focus(self):
        self.assertEqual(self.state["workspace"][0]["id"],"W1")
    def test_hypothesis_has_falsifier(self):
        self.assertTrue(all(h["falsifier"] for h in self.state["hypotheses"]))
    def test_experiment_requires_review(self):
        self.assertTrue(all(e["human_review"] for e in self.state["experiments"]))
    def test_actions_include_freeze(self):
        self.assertTrue(any("Freeze creation" in a["action"] for a in self.state["actions"]))
    def test_hash_length(self):
        self.assertEqual(len(self.state["result_hash"]),64)

if __name__=='__main__': unittest.main()
