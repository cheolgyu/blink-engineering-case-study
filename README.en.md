# Blink Engineering Case Study

Blink began as an experiment in scrolling an Android screen with an intentional eye blink. It developed into a family of apps and a separate investigation of gaze-based interaction.

This is a curated engineering narrative, not the full product repository or a claim of production-ready gaze tracking. The author defined the user problems, proposed hypotheses, supplied device input and reproduction feedback, and made prioritization and acceptance decisions. AI coding tools assisted implementation, training, testing, and documentation.

## Read

- [Full project story in Korean](docs/blink-story.ko.md)
- [Detailed gaze-research journey in Korean](docs/gaze-story.ko.md)
- [Portfolio PDF in Korean](reports/blink-project-record-ko.pdf)
- [Architecture and research lineage](docs/architecture-and-lineage.ko.md)
- [Evidence and limitations](docs/evidence-and-limits.ko.md)
- [Editorial review and author-idea coverage](docs/editorial-review.ko.md)

The narrative explains how an unstable pointer led to a gaze-force controller; difficulty observing the pupil led to sclera and eyelid hypotheses; changing captures led to device pose, logging face-pose estimates, relative eye-size measurements, and face-first/eye-residual models. The face angles are model-derived estimates, not externally measured physical ground truth. Later work compared periocular motion, CNN-free kernels, separate-eye representations, neutral classification, causal filters, and learned state transitions. A blink-operated ON/OFF gate was implemented separately in the lab; fixing its frame/event ordering did not improve the underlying gaze model's accuracy.

Several experiments improved specific metrics while regressing elsewhere. For example, a state model increased eligible target agreement from 82.01% to 86.04% and reduced decision changes from 82 to 15, but increased sustained wrong-state time from 12.039 to 15.552 seconds. It was not promoted to the default product model.

These are historical, single-user development results, not independently measured physical gaze accuracy or evidence of new-user generalization. Different experiments use different denominators. The source corpus is private, so this public repository does not reproduce model training or all reported metrics.

High-level patent preparation is described, but filing or grant completion is not asserted. No patent claims, private captures, model weights, real feature rows, device identifiers, credentials, or raw conversations are published. See [Privacy](PRIVACY.md), [Third-party acknowledgement](THIRD_PARTY.md), and [License scope](LICENSE).

Record date: 2026-10-15. Publishing this case study does not constitute a new app release.
