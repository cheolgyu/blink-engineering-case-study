"""Check this curated publication, not the private model or device results."""

from hashlib import sha256
import ipaddress
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'evidence/public-files.sha256.json'
ALLOWED = frozenset({
    '.gitignore', '.gitattributes', 'LICENSE', 'README.md', 'README.en.md', 'PRIVACY.md',
    'SECURITY.md', 'THIRD_PARTY.md', 'docs/blink-story.ko.md',
    'docs/gaze-story.ko.md', 'docs/architecture-and-lineage.ko.md',
    'docs/evidence-and-limits.ko.md', 'evidence/selected-results.json',
    'docs/editorial-review.ko.md', 'evidence/idea-coverage.json',
    'evidence/publication-review.json', MANIFEST, 'reports/blink-project-record-ko.pdf',
    'scripts/check_public_case_study.py', 'tests/test_public_case_study.py',
})
LINK = re.compile(r'!?\[[^\]]+\]\(([^\s)]+)\)')
PATTERNS = {
    'private-key': r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    'github-token': r'gh[pousr]_[A-Za-z0-9]{20,}',
    'google-api-key': r'AIza[0-9A-Za-z_-]{30,}',
    'user-directory': r'[A-Za-z]:[\\/]Users[\\/]',
    'email-address': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
}


def sensitive_hits(text):
    hits = [name for name, pattern in PATTERNS.items() if re.search(pattern, text)]
    for match in re.finditer(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])', text):
        try:
            ipaddress.ip_address(match.group())
        except ValueError:
            continue
        hits.append('ip-address')
    return sorted(set(hits))


def local_links(path, text, root=ROOT):
    failures = []
    for target in LINK.findall(text):
        if target.startswith(('https://', '#')):
            continue
        if ':' in target or target.startswith('/'):
            failures.append(target)
            continue
        name = target.split('#', 1)[0]
        resolved = (path.parent / name).resolve()
        if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
            failures.append(target)
    return failures


def check_evidence(data):
    errors = []
    for flag in ('independently_measured_physical_gaze', 'training_or_device_tests_rerun_for_this_publication',
                 'original_corpus_public'):
        if data.get(flag) is not False:
            errors.append('Scope flag must be false: ' + flag)
    sources = data.get('sources', [])
    ids = [s.get('id') for s in sources]
    if len(ids) != len(set(ids)) or not ids:
        errors.append('Invalid or duplicate source ids')
    for source in sources:
        if not re.fullmatch(r'[0-9a-f]{64}', source.get('sha256', '')):
            errors.append('Invalid source hash')
        if source.get('access') != 'private-original-not-included':
            errors.append('Private source boundary missing')
    experiments = data.get('experiments', [])
    experiment_ids = [x.get('id') for x in experiments]
    if len(experiment_ids) != len(set(experiment_ids)):
        errors.append('Duplicate experiment ids')
    for experiment in experiments:
        if not experiment.get('population') or not experiment.get('limitation') or not experiment.get('measure'):
            errors.append('Missing experiment scope')
        if not experiment.get('sources') or set(experiment['sources']) - set(ids):
            errors.append('Missing source reference')
    m = {x['id']: x['values'] for x in experiments}
    required = {'force_free', 'force_target', 'face_pose_missing', 'eyelid', 'error_parts_y',
                'eyes', 'neutral_new', 'filters', 'state', 'rust_transform'}
    if set(m) != required:
        return errors + ['Unexpected experiment inventory']
    if sum(m['error_parts_y'][k] for k in ('jitter_percent', 'shared_bias_percent', 'capture_disagreement_percent')) != 100:
        errors.append('Error decomposition must sum to 100')
    state = m['state']
    if not (state['candidate_score_percent'] > state['raw_score_percent'] and
            state['candidate_switches'] < state['raw_switches'] and
            state['candidate_sustained_wrong_seconds'] > state['raw_sustained_wrong_seconds']):
        errors.append('State-model regression was lost')
    neutral = m['neutral_new']
    if not (neutral['after_all_visits_percent'] < neutral['after_percent'] and
            neutral['observed_visits'] < neutral['planned_visits']):
        errors.append('Conditional denominator was lost')
    eyes = m['eyes']
    if eyes['separate_far_percent'] >= eyes['old_far_percent']:
        errors.append('Separate-eye distance regression was lost')
    return errors


def check_ideas(coverage, evidence, narrative):
    errors = []
    for flag in ('first_proposal_dates_independently_verified', 'exhaustive_conversation_inventory'):
        if coverage.get(flag) is not False:
            errors.append('Unverified idea-history scope: ' + flag)
    items = coverage.get('items', [])
    if [item.get('id') for item in items] != [f'I{n:02d}' for n in range(1, 32)]:
        errors.append('Expected 31 ordered author decisions')
    source_ids = {source['id'] for source in evidence['sources']}
    normalized = re.sub(r'\s+', '', narrative)
    for item in items:
        if not item.get('author_idea') or not item.get('scope'):
            errors.append('Missing idea attribution or scope')
        if not item.get('sources') or set(item['sources']) - source_ids:
            errors.append('Unknown idea source: ' + item['id'])
        phrases = item.get('required_phrases', [])
        if len(phrases) < 2 or any(re.sub(r'\s+', '', phrase) not in normalized for phrase in phrases):
            errors.append('Idea wording missing from narrative: ' + item['id'])
    return errors


def check(root=ROOT):
    errors = []
    files = {}
    for path in root.rglob('*'):
        parts = path.relative_to(root).parts
        if any(part in ('.git', '__pycache__') for part in parts):
            continue
        if path.is_symlink():
            errors.append('Symlink not allowed: ' + path.name)
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        files[rel] = path
        if rel not in ALLOWED:
            errors.append('Unexpected public file: ' + rel)
        if path.suffix in ('.md', '.py', '.json') or rel in ('LICENSE', '.gitignore'):
            text = path.read_text(encoding='utf-8')
            for hit in sensitive_hits(text):
                errors.append(f'{rel}: {hit}')
            if path.suffix == '.md':
                errors.extend(f'{rel}: broken link {link}' for link in local_links(path, text, root))
    for missing in ALLOWED - files.keys():
        errors.append('Missing public file: ' + missing)
    if 'evidence/selected-results.json' in files:
        evidence = json.loads(files['evidence/selected-results.json'].read_text(encoding='utf-8'))
        errors.extend(check_evidence(evidence))
        if 'evidence/idea-coverage.json' in files and 'docs/blink-story.ko.md' in files:
            coverage = json.loads(files['evidence/idea-coverage.json'].read_text(encoding='utf-8'))
            errors.extend(check_ideas(coverage, evidence, files['docs/blink-story.ko.md'].read_text(encoding='utf-8')))
    if 'evidence/publication-review.json' in files:
        review = json.loads(files['evidence/publication-review.json'].read_text(encoding='utf-8'))
        pdf = files.get('reports/blink-project-record-ko.pdf')
        if pdf and review.get('pdf_sha256') != sha256(pdf.read_bytes()).hexdigest():
            errors.append('PDF differs from reviewed revision')
        narrative_hashes = review.get('narrative_source_sha256', {})
        if set(narrative_hashes) != {'docs/blink-story.ko.md', 'docs/gaze-story.ko.md'}:
            errors.append('Missing reviewed narrative hashes')
        for rel, expected in narrative_hashes.items():
            if rel not in files or sha256(files[rel].read_bytes()).hexdigest() != expected:
                errors.append('Narrative differs from reviewed PDF source: ' + rel)
    if 'docs/gaze-story.ko.md' in files:
        text = files['docs/gaze-story.ko.md'].read_text(encoding='utf-8')
        numbers = re.findall(r'^## (\d{2}) ', text, re.M)
        if numbers != [f'{n:02d}' for n in range(1, 23)]:
            errors.append('Gaze narrative must contain 22 ordered scenes')
    if MANIFEST in files:
        manifest = json.loads(files[MANIFEST].read_text(encoding='utf-8'))
        if set(manifest) != ALLOWED - {MANIFEST}:
            errors.append('Manifest file inventory mismatch')
        for rel, expected in manifest.items():
            if rel not in files or sha256(files[rel].read_bytes()).hexdigest() != expected:
                errors.append('Manifest hash mismatch: ' + rel)
    return errors


if __name__ == '__main__':
    problems = check()
    for problem in problems:
        print(problem)
    print('FAIL' if problems else 'PASS: curated files, links, selected evidence and scope checks')
    raise SystemExit(bool(problems))
