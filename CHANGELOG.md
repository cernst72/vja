# Changelog

All notable changes to this project will be documented in this file. See
[Conventional Commits](https://conventionalcommits.org) for commit guidelines.

## [0.5.2](https://gitlab.com/ce72/vja/compare/0.5.1...0.5.2) (2023-02-20)

## [0.5.1](https://gitlab.com/ce72/vja/compare/0.5.0...0.5.1) (2023-02-20)

## 1.0.0 (2023-02-20)


### Features

* add bucket filter ([9c82c5b](https://gitlab.com/ce72/vja/commit/9c82c5b0b676389e5d68bc8bcfdb1627b4f539cd))
* Custom output format with --custom-format ([e587691](https://gitlab.com/ce72/vja/commit/e5876918309c8b38e01c3339f7cabbaeac622b6e))
* filter by due-date with conditional operators (lt,le,gt, ge, before/after) ([89bd55b](https://gitlab.com/ce72/vja/commit/89bd55ba9fe27a7606a0decb042be7f448a95743))
* filter by priority with conditional operators (lt..eq..gt..) ([abfc72c](https://gitlab.com/ce72/vja/commit/abfc72c2ac817ab3158f6a6f37403eaa3293b70f))
* filter tasks with empty labels (vja ls --label='') ([d51d4a3](https://gitlab.com/ce72/vja/commit/d51d4a36d91496833059d9ca367118dd011ee299))
* filter tasks with empty labels (vja ls --label='') ([7fd72f2](https://gitlab.com/ce72/vja/commit/7fd72f2b49047357b9abfd584050193dca6710ef))
* filter tasks with empty labels (vja ls --label='') ([4df7e91](https://gitlab.com/ce72/vja/commit/4df7e91b9f484fde0e76dcc47e4c54edf3ceb1fc))
* log absolute path to config ([252beca](https://gitlab.com/ce72/vja/commit/252beca7a432ce71325a23360dfeec11ab76a1ad))
* show done_at date ([edd360c](https://gitlab.com/ce72/vja/commit/edd360c73909d58beed2d94910a304f5c320dfa7))
* sort tasks ([10a827f](https://gitlab.com/ce72/vja/commit/10a827f8538e0988804f6825fcb2391c1a55264f))
* toggle done flag of task ([d7a516d](https://gitlab.com/ce72/vja/commit/d7a516d8c9f9ff21fc62754964b8d0cb2d187712))
* use click.echo instead of print ([8210ce2](https://gitlab.com/ce72/vja/commit/8210ce2967203650afe08cbf9e4810d17b4219df))
* vja ls -u defaults to -u 3 ([e7f19c5](https://gitlab.com/ce72/vja/commit/e7f19c5cdc494106168a70c72fd539652b4699f7))


### Bug Fixes

* accept iso formatted date args ([83e3b01](https://gitlab.com/ce72/vja/commit/83e3b016f717243237b3103bcae831610db56a98))
* data_dict for arrays ([0c082bc](https://gitlab.com/ce72/vja/commit/0c082bc2b6e434395daa766951b5716a869126ad))
* parsed time defaults to 00:00 ([60d0875](https://gitlab.com/ce72/vja/commit/60d087513072c5ea465d406ba15a8bd532a41e35))
* refactor output and add tests ([6bce1f3](https://gitlab.com/ce72/vja/commit/6bce1f337b60c8687f08901fee90288d3ac87aac))
* refactor output and add tests ([a4f4b08](https://gitlab.com/ce72/vja/commit/a4f4b08d3d0f31da931d82f9498ecfb0096b9f20))
* remove deprecation warning from parsedatetime ([d031bb0](https://gitlab.com/ce72/vja/commit/d031bb0b990f83287b9b48edbe377fb24d26756b))
* remove pytest.ini ([26231d4](https://gitlab.com/ce72/vja/commit/26231d4963dfe5c048fb8ad450a5b185992dfdbc))
* toggle done does not overwrite other fields ([97dd074](https://gitlab.com/ce72/vja/commit/97dd07471c3d90050c7ada395124a25e814ba800))
