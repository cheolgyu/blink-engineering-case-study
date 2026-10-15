import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('guard', ROOT / 'scripts/check_public_case_study.py')
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class PublicationChecks(unittest.TestCase):
    def evidence(self):
        return json.loads((ROOT / 'evidence/selected-results.json').read_text(encoding='utf-8'))

    def test_valid_evidence(self):
        self.assertEqual(guard.check_evidence(self.evidence()), [])

    def test_cannot_claim_physical_gaze(self):
        data = self.evidence()
        data['independently_measured_physical_gaze'] = True
        self.assertTrue(guard.check_evidence(data))

    def test_source_reference_required(self):
        data = self.evidence()
        data['experiments'][0]['sources'] = ['missing-source']
        self.assertIn('Missing source reference', guard.check_evidence(data))

    def test_cannot_drop_conditional_denominator(self):
        data = self.evidence()
        record = next(x for x in data['experiments'] if x['id'] == 'neutral_new')
        record['values']['after_all_visits_percent'] = record['values']['after_percent']
        self.assertIn('Conditional denominator was lost', guard.check_evidence(data))

    def test_state_regression_must_be_visible(self):
        data = self.evidence()
        record = next(x for x in data['experiments'] if x['id'] == 'state')
        record['values']['candidate_sustained_wrong_seconds'] = 0
        self.assertIn('State-model regression was lost', guard.check_evidence(data))

    def test_eye_distance_regression_must_be_visible(self):
        data = self.evidence()
        record = next(x for x in data['experiments'] if x['id'] == 'eyes')
        record['values']['separate_far_percent'] = 100
        self.assertIn('Separate-eye distance regression was lost', guard.check_evidence(data))

    def test_detects_token_without_real_credential(self):
        token = 'gh' + 'p_' + 'x' * 30
        self.assertIn('github-token', guard.sensitive_hits(token))

    def test_detects_local_user_path(self):
        text = 'X:' + '/' + 'Users' + '/' + 'example'
        self.assertIn('user-directory', guard.sensitive_hits(text))

    def test_internal_link_boundary(self):
        path = ROOT / 'docs' / 'gaze-story.ko.md'
        self.assertEqual(guard.local_links(path, '[limits](evidence-and-limits.ko.md)'), [])
        self.assertTrue(guard.local_links(path, '[outside](../../outside.md)'))

    def test_repository_inventory_and_manifest(self):
        self.assertEqual(guard.check(), [])

    def ideas(self):
        return json.loads((ROOT / 'evidence/idea-coverage.json').read_text(encoding='utf-8'))

    def narrative(self):
        return (ROOT / 'docs/blink-story.ko.md').read_text(encoding='utf-8')

    def test_author_ideas_are_connected_to_story(self):
        self.assertEqual(guard.check_ideas(self.ideas(), self.evidence(), self.narrative()), [])

    def test_cannot_claim_exhaustive_history(self):
        data = self.ideas()
        data['exhaustive_conversation_inventory'] = True
        self.assertTrue(guard.check_ideas(data, self.evidence(), self.narrative()))

    def test_removed_idea_wording_is_detected(self):
        data = self.ideas()
        data['items'][0]['required_phrases'] = ['not-a-phrase-in-the-narrative', 'not-present-either']
        self.assertTrue(guard.check_ideas(data, self.evidence(), self.narrative()))

    def test_unknown_idea_source_is_detected(self):
        data = self.ideas()
        data['items'][0]['sources'] = ['not-a-source']
        self.assertTrue(guard.check_ideas(data, self.evidence(), self.narrative()))


if __name__ == '__main__':
    unittest.main()
