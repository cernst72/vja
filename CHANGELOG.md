## [4.1.0](https://gitlab.com/ce72/vja/compare/4.0.0...4.1.0) (2024-07-08)

### Features

* **ls:** alias --all for --include-completed ([4d6f868](https://gitlab.com/ce72/vja/commit/4d6f868c3cb067bedf66c8b4f70cba97b72feb06))
* **show:** more concise output ([dbd21a3](https://gitlab.com/ce72/vja/commit/dbd21a3e4b8c7097ecdd4684010df4d309bc61cd))

### Misc

* **deps:** update dependency pip to v24.1.2 ([01f271b](https://gitlab.com/ce72/vja/commit/01f271bc7309073b55cb3bfc899b39a545d1c539))

## [4.0.0](https://gitlab.com/ce72/vja/compare/3.4.0...4.0.0) (2024-07-02)

### ⚠ BREAKING CHANGES

* Will require vikunja > 0.23.
- (task) Remove bucket filter (`-b`) from `vja ls`.
- (task) Remove commands `vja push` / `vja pull`
- (buckets) `vja bucket` applies to first kanban view of the project

### Features

* Handle Vikunjas new ProjectViews. Remove support for buckets. ([5d53ab4](https://gitlab.com/ce72/vja/commit/5d53ab497930acdcfcbfd01d7661232b1207b0d7))
* **ls:** apply new filter syntax ([60bb3b2](https://gitlab.com/ce72/vja/commit/60bb3b272bbe4eafdf775c7f59a201e632a61199))

### Documentation

* update Readme ([449c47e](https://gitlab.com/ce72/vja/commit/449c47e930c6d93003910091ae5bfa22ca50df5e))

### Misc

* **ci:** pull vikunja image separately and only once ([d867d0a](https://gitlab.com/ce72/vja/commit/d867d0a38881b7e9208c5a075d5845d46c02ec41))
* **deps:** update all dependencies ([63cc9eb](https://gitlab.com/ce72/vja/commit/63cc9eb663e068e390d01f2d780a3a923ebc11ca))

### Automation

* compose file supports distroless vikunja image ([5c93027](https://gitlab.com/ce72/vja/commit/5c93027db1bd8845f00c22be9ae24ca0407d51d4))
* reactivate 404 test ([4cf3d6c](https://gitlab.com/ce72/vja/commit/4cf3d6cbb7e37490f3229b8addc8ad3fb9137c2c))
* test with vikunja/vikunja:0.24.0 base image ([b7a7ed6](https://gitlab.com/ce72/vja/commit/b7a7ed63c1c13b7e303c516dc3a7104c18547339))
* unpin conventional-changelog-conventionalcommits ([7644d1f](https://gitlab.com/ce72/vja/commit/7644d1fe37a662d1b495bc55032ccbc4ebdd581c))

## [3.4.0](https://gitlab.com/ce72/vja/compare/3.3.2...3.4.0) (2024-05-30)


### Features

* **add, edit:** set default time 08:00 in parsed dates ([5939075](https://gitlab.com/ce72/vja/commit/5939075d4826c5cedb2e4b1cb331e700d7265f1e))

## [3.3.2](https://gitlab.com/ce72/vja/compare/3.3.1...3.3.2) (2024-05-30)


### Bug Fixes

* **ls:** exception due to "object of type generator has no len" ([2c4f09a](https://gitlab.com/ce72/vja/commit/2c4f09a03931b5f301621d81967e4e8bade366fa))


### Misc

* **deps:** update all dependencies ([893cbbf](https://gitlab.com/ce72/vja/commit/893cbbf4a2c06e0e85e904d81ec78326a3a37e9e))

## [3.3.1](https://gitlab.com/ce72/vja/compare/3.3.0...3.3.1) (2024-03-26)


### Bug Fixes

* TypeError for vja ls with task_ids ([450d953](https://gitlab.com/ce72/vja/commit/450d953b86e5b2c275a46ebf0ab6d9f34039a128))

## [3.3.0](https://gitlab.com/ce72/vja/compare/3.2.1...3.3.0) (2024-03-25)


### Features

* **add:** support creating tasks with multiple labels ([1e45554](https://gitlab.com/ce72/vja/commit/1e455543b21f839c9617732237746bcd58aecb66))


### Misc

* edit Changelog ([1e65150](https://gitlab.com/ce72/vja/commit/1e6515067c55f1e5e22a92e546accd6bab3eba07))

## [3.2.1](https://gitlab.com/ce72/vja/compare/3.2.0...3.2.1) (2024-03-20)


### Misc

* **deps:** update all dependencies ([8d01b92](https://gitlab.com/ce72/vja/commit/8d01b9277ceb8097e8c811c2deec46489f23f867))
* **deps:** update all dependencies ([8675f0b](https://gitlab.com/ce72/vja/commit/8675f0b6bd53fcc69617c3b02abb4883a17bfa74))

### Documentation
* Rename to README.md ([8938099](https://gitlab.com/ce72/vja/-/commit/89380991042fa9a2a3eb5f2e8993128e7da482c7))

### Automation

* create required folders and init user in sep. container ([efce86f](https://gitlab.com/ce72/vja/commit/efce86fae18065b5a3dfd3edbb024acb99569f80))
* no need to docker compose down in pipeline ([a433ebd](https://gitlab.com/ce72/vja/commit/a433ebd6be62ef6afa8c2c84011ebe771509a75e))
* **semantic:** create patch release for keyword ci ([ab586e8](https://gitlab.com/ce72/vja/commit/ab586e8d9ceae62c73c31d50648ae23b8c5ecdac))
* **test:** pin test image to current stable ([97b4d66](https://gitlab.com/ce72/vja/commit/97b4d6615ac625b705e0282e2a2e18584a4a30a0))

## [3.2.0](https://gitlab.com/ce72/vja/compare/3.1.0...3.2.0) (2024-02-19)


### Features

* **ls:** display task count ([9cb417a](https://gitlab.com/ce72/vja/commit/9cb417a9a8cf149e585eaa571fbf76999e9fabaf))


### Misc

* **deps:** update dependency pytest to v8.0.1 ([eb85646](https://gitlab.com/ce72/vja/commit/eb85646fcccfdd13de36327f5701a062296ebacf))
* reactivate test ([4b003b2](https://gitlab.com/ce72/vja/commit/4b003b2c4b06fb8828a4c097abcec4f336aeaf41))
* test vikunja-0.23.0 compatibility ([5fc1ac7](https://gitlab.com/ce72/vja/commit/5fc1ac7193dbf3e069a738aa77519fcf077b46dd))

## [3.1.0](https://gitlab.com/ce72/vja/compare/3.0.0...3.1.0) (2024-02-06)


### Features

* allow aliases projects, buckets, labels ([07b8e45](https://gitlab.com/ce72/vja/commit/07b8e455159839198fb3f197d5cafa9fd99a7427))
* **cli:** 'vja open project_id' in webbrowser ([6dfef76](https://gitlab.com/ce72/vja/commit/6dfef76976c4603220eaafd6a53db923debc28dc))
* **project:** display new fields ([2e371d5](https://gitlab.com/ce72/vja/commit/2e371d59069e4ed9beb6f14892179a9e4be2236c))
* vja open supports multiple tasks ([0efbdc5](https://gitlab.com/ce72/vja/commit/0efbdc5e0730dafd31988ac31e7b6103c79580fc))


### Documentation

* describe login, including API token ([ba0d48e](https://gitlab.com/ce72/vja/commit/ba0d48e4aeda893d6e41829bfac1b3d15410d9f6))


### Misc

* **deps:** update all dependencies ([fb24895](https://gitlab.com/ce72/vja/commit/fb248956c33b708b84dce644ea1dd952960dc243))
* **deps:** update all dependencies ([6f1f3b2](https://gitlab.com/ce72/vja/commit/6f1f3b2058aa6e227ce12a73159f443ed147249d))
* **deps:** update dependency pip to v23.3.2 ([8c06908](https://gitlab.com/ce72/vja/commit/8c06908d77f93720c3be4a2856792d5e68c37006))
* fix linter issues ([c5a0149](https://gitlab.com/ce72/vja/commit/c5a0149e012b2e1b0dec0d3906092078fea99e80))


### Automation

* define minimum required versions ([debc2aa](https://gitlab.com/ce72/vja/commit/debc2aa4f4bbf7c417d4ec15ed3e1aab452543be))
* fix CHANGELOG ([738c67a](https://gitlab.com/ce72/vja/commit/738c67a4b6e72107f7119b727c0780c277892716))

## [3.0.0](https://gitlab.com/ce72/vja/compare/2.4.1...3.0.0) (2023-12-19)


### ⚠ BREAKING CHANGES

* support Vikunja 0.22.0 api ([4d727e17](https://gitlab.com/ce72/vja/commit/4d727e17be2ea978d2cece4f532bc39b019e2c1c))

### Features

* **bucket:** remove output of bucket.is_done_bucket ([23e8bf7](https://gitlab.com/ce72/vja/commit/23e8bf7c138e62bc46d3bb78bba203cdb29be140))


### Documentation

* **Readme:** favor pip install --user ([b71e171](https://gitlab.com/ce72/vja/commit/b71e1713554a4f4f9b5411d82a8fd0e4d564db0a))


### Automation

* disable pip cache ([eecd839](https://gitlab.com/ce72/vja/commit/eecd83902c8235c03793ecffa8f1aee6d1dd542f))
* don't call deprecated setup.py ([9011135](https://gitlab.com/ce72/vja/commit/901113597b6c49bfb782b70b9ea4f8749508a58b))
* don't call wheel and setup.py directly ([eeb68d9](https://gitlab.com/ce72/vja/commit/eeb68d92ddde1677c8d192aacd87eb90fac4a0fb))


## [2.5.0](https://gitlab.com/ce72/vja/compare/2.4.1...2.5.0) (2023-12-19)

*Released by mistake with parts of 3.0.0*

## [2.4.1](https://gitlab.com/ce72/vja/compare/2.4.0...2.4.1) (2023-12-16)


### Bug Fixes

* **ci:** use virtual environments and fix requirements handling ([fdd33f2](https://gitlab.com/ce72/vja/commit/fdd33f2cae1dd53ca2744f40f03574968a474866))
* **ci:** use virtual environments and python3 -m pip ([363d94e](https://gitlab.com/ce72/vja/commit/363d94e98aec3990312ff9580bad70059c837711))


### Automation

* use venv ([69a2943](https://gitlab.com/ce72/vja/commit/69a29437f2dfafd73f17768c4f1f1a370af311d4))

## [2.4.0](https://gitlab.com/ce72/vja/compare/2.3.0...2.4.0) (2023-12-16)


### Features

* **cli:** vja ls [task_ids] ([67a5166](https://gitlab.com/ce72/vja/commit/67a516657dbd68d0e6689990bcc1845befd2de53))


### Misc

* **deps:** update all dependencies ([b046d57](https://gitlab.com/ce72/vja/commit/b046d57d18fd9bb60315676ec3e59a31a9992424))


### Automation

* fix semantic release step ([55162da](https://gitlab.com/ce72/vja/commit/55162da166d8db3818fd90d115b2a8612ece2c8c))
* pin docker to 24.0.6 ([23612bc](https://gitlab.com/ce72/vja/commit/23612bc574422963b58ffabdc4c920d487274b34))
* pip with --break-system-packages ([251768b](https://gitlab.com/ce72/vja/commit/251768b5a3e2effc7cb36890e08b91d71a6922e7))
* run pipeline in virtual env ([b82aa0b](https://gitlab.com/ce72/vja/commit/b82aa0bdb513a9c7631dea1172c7e609a4aa191b))
* unpin docker version ([0185db0](https://gitlab.com/ce72/vja/commit/0185db09eb50e166e8ea1dcb4d7372146dee911f))

## [2.3.0](https://gitlab.com/ce72/vja/compare/2.2.1...2.3.0) (2023-10-06)


### Features

* **cli:** vja push/pull task ([50ce795](https://gitlab.com/ce72/vja/commit/50ce7958d1791f1fd5b0ec71b641f7e127d979bc))
* **cli:** vja push/pull task ([2be0e85](https://gitlab.com/ce72/vja/commit/2be0e85b56ceada24207e7d8b3465f5aa4d5f2e0))


### Misc

* **deps:** update all dependencies ([f9d578b](https://gitlab.com/ce72/vja/commit/f9d578b534385ea36ddc6980306d91817e8eea66))
* **deps:** update all dependencies ([1db988e](https://gitlab.com/ce72/vja/commit/1db988e1eb39f72a35b1bc6c9bc6ff30e840a3a9))

## [2.2.1](https://gitlab.com/ce72/vja/compare/2.2.0...2.2.1) (2023-09-08)


### Bug Fixes

* **cli:** allow --notes (in addition to --note) ([de090a3](https://gitlab.com/ce72/vja/commit/de090a3ddf90bcbca2dab213e5c5dde9ad1c395d))
* **ls:** --include-completed got an error ([5c150ca](https://gitlab.com/ce72/vja/commit/5c150ca961c83011d0a35a7b4bc05dbbca374c9a))
* **ls:** --include-completed got an error ([5039352](https://gitlab.com/ce72/vja/commit/503935279f9584ed94ad26e053e336658494cdfb))


### Automation

* workaround - pin conventional-changelog-conventionalcommits ([b8e35d1](https://gitlab.com/ce72/vja/commit/b8e35d19a6b7aef6123dfc38e33b05ce4bfa1ddb))

## [2.2.0](https://gitlab.com/ce72/vja/compare/2.1.0...2.2.0) (2023-08-22)


### Features

* **ls:** support regex in label.title and project.title filter ([022844b](https://gitlab.com/ce72/vja/commit/022844bf01539222098fc94b524497a6f2e2602f))
* **ls:** support regex in label.title and project.title filter ([7689d8a](https://gitlab.com/ce72/vja/commit/7689d8a52a090f848d53a091fd9fca0c4bdd2872))
* **ls:** support regex in label.title and project.title filter ([e6d3de2](https://gitlab.com/ce72/vja/commit/e6d3de22b41c38d71a1fc365ca3a062d2c521649))

## [2.1.0](https://gitlab.com/ce72/vja/compare/2.0.0...2.1.0) (2023-08-21)


### Features

* **cli:** verbose (-v) and quiet (-q) for editing tasks ([36a3527](https://gitlab.com/ce72/vja/commit/36a35279ad0bd19d9c03566e5735c5bb7c7b22d0))


### Misc

* **deps:** update all dependencies ([3bed81b](https://gitlab.com/ce72/vja/commit/3bed81b1826454549798da36bd0657974aaf9f7e))


### Automation

* remove requirements_ci.txt ([2c4abb6](https://gitlab.com/ce72/vja/commit/2c4abb6a3028dee1027628a377d164d763861837))
* simplify pipeline rules ([6eba5cc](https://gitlab.com/ce72/vja/commit/6eba5ccf508c06fcdcefb40eebd4d0a568fcb429))
* update build requirements ([c5d5397](https://gitlab.com/ce72/vja/commit/c5d53975bc77beee92616a17e128782be6c878da))
* use latest docker:cli image ([a47cef0](https://gitlab.com/ce72/vja/commit/a47cef01196f943c353384effeeb05318d1322f3))

## [2.0.0](https://gitlab.com/ce72/vja/compare/1.5.1...2.0.0) (2023-07-07)


### ⚠ BREAKING CHANGES

* remove namespaces
* **api:** remove reminder_dates
* **api:** New projects api (only backend side)
* Preliminary support for new reminder array

### Features

* **api:** New projects api (only backend side) ([b1df704](https://gitlab.com/ce72/vja/commit/b1df70496a070b827c7431c68181d4ec18aa5190))
* **api:** remove reminder_dates ([6f18cff](https://gitlab.com/ce72/vja/commit/6f18cff9ffae2e95dafd9c936400b5e216b44008))
* **cli:** alias --urgent for --urgency ([3701ab2](https://gitlab.com/ce72/vja/commit/3701ab25ddeebc7f07959c0ac2bdca9833b5d15f))
* defer reminder ([aec5f53](https://gitlab.com/ce72/vja/commit/aec5f53ed530a3e1a486b7cad56a9c1613ae100a))
* **defer task:** defer passed due date relative to now ([f6a70e5](https://gitlab.com/ce72/vja/commit/f6a70e58506104f5c0fd6eb421baf9017f31feb9))
* fetch long_token when logging in (with a ttl of 30 days) ([1e8a7b8](https://gitlab.com/ce72/vja/commit/1e8a7b86ae4781b812909132d1574380965e99d3))
* **filter, sort:** Rename "label-titles" to "labels" ([0a452ac](https://gitlab.com/ce72/vja/commit/0a452acbd727762ec660faa6c268582c4111d01f))
* **ls -i:** filter by title case-insensitive ([511a807](https://gitlab.com/ce72/vja/commit/511a807866936914ebc0d33880232fec538b2e64))
* **ls:** output flags for alarm, repeat, description ([2b01087](https://gitlab.com/ce72/vja/commit/2b010877d1582408722f719ab985ce10318f9182))
* Preliminary support for new reminder array ([fe2c332](https://gitlab.com/ce72/vja/commit/fe2c33281206fcf4e121875164ab36ea78369987))
* **project:** add project to parent-project by title ([ba67a8a](https://gitlab.com/ce72/vja/commit/ba67a8a6a985eacb8e5402f3b0f770dd4e4393b6))
* **reminders:** remove legacy reminder_dates ([66491d0](https://gitlab.com/ce72/vja/commit/66491d046997881dfec5f9e01a27b771685c4a19))
* **reminders:** Set relative reminders like "1h before due" ([18534b4](https://gitlab.com/ce72/vja/commit/18534b4921a04e603ad4003a4a3f3ad9196de10c))
* remove namespaces ([3c027b0](https://gitlab.com/ce72/vja/commit/3c027b09b996dcfc8ff650b75c565d6500a124b4))
* rename lists to project within vja ([54b0b0a](https://gitlab.com/ce72/vja/commit/54b0b0a46cfaaa20236fe79580a9a28909056d7c))
* Support for new reminder array (read) ([5caff10](https://gitlab.com/ce72/vja/commit/5caff109bf444087ec83f8f6e3257d5ffddefaa1))
* **task ls:** filter tasks by --base-project ([2740e73](https://gitlab.com/ce72/vja/commit/2740e7361aaeab79d952ce8bc87299c58ddea8d2))


### Bug Fixes

* **clone:** clone labels too ([0516908](https://gitlab.com/ce72/vja/commit/05169086c09ff4b77d597799defff00b01f4b591))
* **clone:** do not clone positions and have --bucket ([15fac96](https://gitlab.com/ce72/vja/commit/15fac96ec4f34fbde4906eef925646fef8ba0d6e))
* **clone:** do not clone positions and have --bucket ([9e0a9aa](https://gitlab.com/ce72/vja/commit/9e0a9aa8ce9e8d6b845063888c22ece7f40b1028))
* do not unset reminder if missing in vja edit ([7b8c922](https://gitlab.com/ce72/vja/commit/7b8c922acaf726060c9de5ad574da585bc8e2e9a))
* **ls -i:** correctly filter by title case-insensitive ([44cda6e](https://gitlab.com/ce72/vja/commit/44cda6e39e100804b330c7f7f31af2823562bc0e))
* sharpen test ([c5dbf43](https://gitlab.com/ce72/vja/commit/c5dbf43d582b244f8b17787ed12a06d160a20856))


### Documentation

* Add table of contents to Features.md ([e394ca5](https://gitlab.com/ce72/vja/commit/e394ca5e3959a77e1a8bb39285f4dc348d997cbd))
* describe env variable VJA_CONFIGDIR ([ef0c2bd](https://gitlab.com/ce72/vja/commit/ef0c2bd9b6b38414a091787c3d641cc9e9799f9a))
* **filters:** improve documentation (and tests) ([2c2b967](https://gitlab.com/ce72/vja/commit/2c2b967f736055f6ab65a3ef7f03c05cc6798344))
* prepare to support vikunja 0.21.0 release ([18cb8ae](https://gitlab.com/ce72/vja/commit/18cb8aeadf1e45d150995f9f47f93ff13441690f))


### Misc

* **release:** Release 2.0.0-beta.1 update changelog [skip ci] ([5f35c3a](https://gitlab.com/ce72/vja/commit/5f35c3a2bced9bd44b4b8528295b6f5f23b4a467))
* **release:** Release 2.0.0-beta.1 update changelog [skip ci] ([a96579c](https://gitlab.com/ce72/vja/commit/a96579c02a01f66008283e4178aa2a389e1d7da1))
* **release:** Release 2.0.0-beta.1 update changelog [skip ci] ([8745e3a](https://gitlab.com/ce72/vja/commit/8745e3a9374a5185c1fd884411ae2e338e77720d))
* **release:** Release 2.0.0-beta.1 update changelog [skip ci] ([8fa7747](https://gitlab.com/ce72/vja/commit/8fa7747305cff1e22934dc260534deda890d8c54))
* **release:** Release 2.0.0-beta.1 update changelog [skip ci] ([9d27ea2](https://gitlab.com/ce72/vja/commit/9d27ea2639c0ffec7582199f004508006479385e))
* **release:** Release 2.0.0-beta.2 update changelog [skip ci] ([ed78554](https://gitlab.com/ce72/vja/commit/ed78554db8f5adaec000fca4358d709755ee20a5))
* **release:** Release 2.0.0-beta.3 update changelog [skip ci] ([1d10ce6](https://gitlab.com/ce72/vja/commit/1d10ce675ab4dd4305196e7048261b018c4dd9f7))
* **release:** Release 2.0.0-beta.4 update changelog [skip ci] ([65b7fbe](https://gitlab.com/ce72/vja/commit/65b7fbe811cd2d2e3ab78cdc54e8f7c0980731f8))
* **release:** Release 2.0.0-rc.1 update changelog [skip ci] ([1a5ce6c](https://gitlab.com/ce72/vja/commit/1a5ce6cda6ac4ab66f6adce16e32af0f1f7c5119))
* **release:** Release 2.0.0-rc.2 update changelog [skip ci] ([9193961](https://gitlab.com/ce72/vja/commit/9193961cb296cbbf3b4def41d84403eb3c87188a))
* **release:** Release 2.0.0-rc.3 update changelog [skip ci] ([4ce239e](https://gitlab.com/ce72/vja/commit/4ce239e6468c18da68c0fd6bc7900ca70bd66f4d))
* **release:** Release 2.0.0-rc.4 update changelog [skip ci] ([1cf039d](https://gitlab.com/ce72/vja/commit/1cf039d842b5ee3cee8be5552401563f6c0fb8a2))
* Remove redundant test ([719943a](https://gitlab.com/ce72/vja/commit/719943a9d1b77a7663d87abac602f8d869c246b1))


### Automation

* add --due-date with/without time ([a28e5fc](https://gitlab.com/ce72/vja/commit/a28e5fca97294351b30e64857a4580164927d895))
* add rc as prerelase branch name ([cf20bc5](https://gitlab.com/ce72/vja/commit/cf20bc5bf50024e721de5116c9cf41f1efde7a59))
* add rc as prerelase branch name ([7c786ee](https://gitlab.com/ce72/vja/commit/7c786eeb74a7a790be27de0c10320ec267b0cfdd))
* add rc as prerelase branch name ([7607fa8](https://gitlab.com/ce72/vja/commit/7607fa853fbdfbbbffec4c0a3e73e16c3f69fdfb))
* automate beta releases ([a325254](https://gitlab.com/ce72/vja/commit/a32525446577421f95b51cb578390d2c72d114c3))
* automate beta releases ([a3fed80](https://gitlab.com/ce72/vja/commit/a3fed80753d817a8026d1ac8eb65291576c5a10f))
* automate beta releases ([f2dc40a](https://gitlab.com/ce72/vja/commit/f2dc40ae6d731b96946c999f3f9d639b38f2b601))
* automate beta releases ([c57f4bc](https://gitlab.com/ce72/vja/commit/c57f4bcd40fcbad44b1d364884864bf764b012e9))
* capture click output ([727c282](https://gitlab.com/ce72/vja/commit/727c2823f2adab62e4e91835ed39219f2b274fe2))
* cleanup gitlab-ci ([cb6f743](https://gitlab.com/ce72/vja/commit/cb6f743f14ab85afd8059c8c9f4baa68e492b215))
* cleanup gitlab-ci ([cab2530](https://gitlab.com/ce72/vja/commit/cab2530d7bdfe9261acf9ae4f30d304e8279b6aa))
* cleanup gitlab-ci ([0716eb9](https://gitlab.com/ce72/vja/commit/0716eb94ebd32ebe4c6fbea7b75f35d66d9e2439))
* cleanup gitlab-ci ([017cf44](https://gitlab.com/ce72/vja/commit/017cf444633a7f800c6f8d1960ea84e093a79c65))
* cleanup test setup ([c8a3872](https://gitlab.com/ce72/vja/commit/c8a387244ee86728241970d86e8b59d259a90c40))
* fix version number ([a985a5e](https://gitlab.com/ce72/vja/commit/a985a5e28f2b1212a4a4f48aa41eadb0dacebcd3))
* fix version number ([4518c3f](https://gitlab.com/ce72/vja/commit/4518c3fa5343762c2eaaa05ab2e60c61294b9b6a))
* fix version number ([cc346c7](https://gitlab.com/ce72/vja/commit/cc346c7aea5b2486a79be2f142801c209adf82d7))
* install coverage from requirements_dev.txt ([9b03ba1](https://gitlab.com/ce72/vja/commit/9b03ba180ceb1a9d8125a4713a5e2799777e4e36))
* install twine via apt ([ba8ba86](https://gitlab.com/ce72/vja/commit/ba8ba863527529ada8519c168e8563a3e7fbe5c4))
* pipeline on branches only manual ([9b05c2d](https://gitlab.com/ce72/vja/commit/9b05c2ddaf778f179a7ddd16a56fa1d5d9b5b5fc))
* pipeline on branches only manual ([3a936d9](https://gitlab.com/ce72/vja/commit/3a936d9a0425ca3c6c87c61b526e87b7474398c3))
* remove build stage ([8e4f36c](https://gitlab.com/ce72/vja/commit/8e4f36cee4ebaff4fcf3c703e6e1b265d955d302))
* remove build stage ([e4858e3](https://gitlab.com/ce72/vja/commit/e4858e363aed6369ef29ef0fe3ed56115083a11b))
* remove build stage ([e27df75](https://gitlab.com/ce72/vja/commit/e27df75b220380148aab79e75af0e5194041d381))
* remove build stage ([49d2fe2](https://gitlab.com/ce72/vja/commit/49d2fe2d4261fa993aa06365fd004876d8fff055))
* remove build stage ([1661721](https://gitlab.com/ce72/vja/commit/166172141e63f3ef22c576196aacaf7de5bea227))
* remove redundant apk packages ([bf6c0ea](https://gitlab.com/ce72/vja/commit/bf6c0eae179929555ecba1315d19683f052a046e))
* remove redundant apk packages ([a34a24d](https://gitlab.com/ce72/vja/commit/a34a24d396bb508d4635bc1cb405d3ab9d6bbdc7))
* trigger on default branch again ([de6dce2](https://gitlab.com/ce72/vja/commit/de6dce20ea387058cc61535324abd3c900a836ff))
* update semantic-release configuration ([de4df86](https://gitlab.com/ce72/vja/commit/de4df867ec80fbead7e8831edbc8d38fd46e0a76))
* wait for running api container ([60d6915](https://gitlab.com/ce72/vja/commit/60d6915845050c5b5b8e528feea69a42f8bbe5d3))

## [2.0.0-rc.4](https://gitlab.com/ce72/vja/compare/2.0.0-rc.3...2.0.0-rc.4) (2023-06-12)


### Features

* **reminders:** remove legacy reminder_dates ([66491d0](https://gitlab.com/ce72/vja/commit/66491d046997881dfec5f9e01a27b771685c4a19))

## [2.0.0-rc.3](https://gitlab.com/ce72/vja/compare/2.0.0-rc.2...2.0.0-rc.3) (2023-06-05)


### Features

* **ls -i:** filter by title case-insensitive ([511a807](https://gitlab.com/ce72/vja/commit/511a807866936914ebc0d33880232fec538b2e64))
* **ls:** output flags for alarm, repeat, description ([2b01087](https://gitlab.com/ce72/vja/commit/2b010877d1582408722f719ab985ce10318f9182))
* **project:** add project to parent-project by title ([ba67a8a](https://gitlab.com/ce72/vja/commit/ba67a8a6a985eacb8e5402f3b0f770dd4e4393b6))


### Bug Fixes

* **ls -i:** correctly filter by title case-insensitive ([44cda6e](https://gitlab.com/ce72/vja/commit/44cda6e39e100804b330c7f7f31af2823562bc0e))

## [2.0.0-rc.2](https://gitlab.com/ce72/vja/compare/2.0.0-rc.1...2.0.0-rc.2) (2023-06-02)


### Features

* **filter, sort:** Rename "label-titles" to "labels" ([0a452ac](https://gitlab.com/ce72/vja/commit/0a452acbd727762ec660faa6c268582c4111d01f))
* **task ls:** filter tasks by --base-project ([2740e73](https://gitlab.com/ce72/vja/commit/2740e7361aaeab79d952ce8bc87299c58ddea8d2))

## [2.0.0-rc.1](https://gitlab.com/ce72/vja/compare/1.5.1...2.0.0-rc.1) (2023-06-02)


### ⚠ BREAKING CHANGES

* **api:** remove namespaces
* **api:** remove reminder_dates
* **api:** New projects api (only backend side)
* Preliminary support for new reminder array

### Features

* **api:** New projects api (only backend side) ([b1df704](https://gitlab.com/ce72/vja/commit/b1df70496a070b827c7431c68181d4ec18aa5190))
* **api:** remove reminder_dates ([6f18cff](https://gitlab.com/ce72/vja/commit/6f18cff9ffae2e95dafd9c936400b5e216b44008))
* **cli:** alias --urgent for --urgency ([3701ab2](https://gitlab.com/ce72/vja/commit/3701ab25ddeebc7f07959c0ac2bdca9833b5d15f))
* defer reminder ([aec5f53](https://gitlab.com/ce72/vja/commit/aec5f53ed530a3e1a486b7cad56a9c1613ae100a))
* **defer task:** defer passed due date relative to now ([f6a70e5](https://gitlab.com/ce72/vja/commit/f6a70e58506104f5c0fd6eb421baf9017f31feb9))
* fetch long_token when logging in (with a ttl of 30 days) ([1e8a7b8](https://gitlab.com/ce72/vja/commit/1e8a7b86ae4781b812909132d1574380965e99d3))
* Preliminary support for new reminder array ([fe2c332](https://gitlab.com/ce72/vja/commit/fe2c33281206fcf4e121875164ab36ea78369987))
* **reminders:** Set relative reminders like "1h before due" ([18534b4](https://gitlab.com/ce72/vja/commit/18534b4921a04e603ad4003a4a3f3ad9196de10c))
* remove namespaces ([3c027b0](https://gitlab.com/ce72/vja/commit/3c027b09b996dcfc8ff650b75c565d6500a124b4))
* rename lists to project within vja ([54b0b0a](https://gitlab.com/ce72/vja/commit/54b0b0a46cfaaa20236fe79580a9a28909056d7c))
* Support for new reminder array (read) ([5caff10](https://gitlab.com/ce72/vja/commit/5caff109bf444087ec83f8f6e3257d5ffddefaa1))


### Bug Fixes

* **clone:** clone labels too ([0516908](https://gitlab.com/ce72/vja/commit/05169086c09ff4b77d597799defff00b01f4b591))
* **clone:** do not clone positions and have --bucket ([15fac96](https://gitlab.com/ce72/vja/commit/15fac96ec4f34fbde4906eef925646fef8ba0d6e))
* **clone:** do not clone positions and have --bucket ([9e0a9aa](https://gitlab.com/ce72/vja/commit/9e0a9aa8ce9e8d6b845063888c22ece7f40b1028))
* do not unset reminder if missing in vja edit ([7b8c922](https://gitlab.com/ce72/vja/commit/7b8c922acaf726060c9de5ad574da585bc8e2e9a))
* sharpen test ([c5dbf43](https://gitlab.com/ce72/vja/commit/c5dbf43d582b244f8b17787ed12a06d160a20856))


### Documentation

* Add table of contents to Features.md ([e394ca5](https://gitlab.com/ce72/vja/commit/e394ca5e3959a77e1a8bb39285f4dc348d997cbd))
* describe env variable VJA_CONFIGDIR ([ef0c2bd](https://gitlab.com/ce72/vja/commit/ef0c2bd9b6b38414a091787c3d641cc9e9799f9a))
* **filters:** improve documentation (and tests) ([2c2b967](https://gitlab.com/ce72/vja/commit/2c2b967f736055f6ab65a3ef7f03c05cc6798344))


### Misc

* Remove redundant test ([719943a](https://gitlab.com/ce72/vja/commit/719943a9d1b77a7663d87abac602f8d869c246b1))


### Automation

* add --due-date with/without time ([a28e5fc](https://gitlab.com/ce72/vja/commit/a28e5fca97294351b30e64857a4580164927d895))
* add rc as prerelase branch name ([cf20bc5](https://gitlab.com/ce72/vja/commit/cf20bc5bf50024e721de5116c9cf41f1efde7a59))
* add rc as prerelase branch name ([7c786ee](https://gitlab.com/ce72/vja/commit/7c786eeb74a7a790be27de0c10320ec267b0cfdd))
* add rc as prerelase branch name ([7607fa8](https://gitlab.com/ce72/vja/commit/7607fa853fbdfbbbffec4c0a3e73e16c3f69fdfb))
* automate beta releases ([a325254](https://gitlab.com/ce72/vja/commit/a32525446577421f95b51cb578390d2c72d114c3))
* automate beta releases ([a3fed80](https://gitlab.com/ce72/vja/commit/a3fed80753d817a8026d1ac8eb65291576c5a10f))
* automate beta releases ([f2dc40a](https://gitlab.com/ce72/vja/commit/f2dc40ae6d731b96946c999f3f9d639b38f2b601))
* automate beta releases ([c57f4bc](https://gitlab.com/ce72/vja/commit/c57f4bcd40fcbad44b1d364884864bf764b012e9))
* capture click output ([727c282](https://gitlab.com/ce72/vja/commit/727c2823f2adab62e4e91835ed39219f2b274fe2))
* cleanup gitlab-ci ([cb6f743](https://gitlab.com/ce72/vja/commit/cb6f743f14ab85afd8059c8c9f4baa68e492b215))
* cleanup gitlab-ci ([cab2530](https://gitlab.com/ce72/vja/commit/cab2530d7bdfe9261acf9ae4f30d304e8279b6aa))
* cleanup gitlab-ci ([0716eb9](https://gitlab.com/ce72/vja/commit/0716eb94ebd32ebe4c6fbea7b75f35d66d9e2439))
* cleanup gitlab-ci ([017cf44](https://gitlab.com/ce72/vja/commit/017cf444633a7f800c6f8d1960ea84e093a79c65))
* cleanup test setup ([c8a3872](https://gitlab.com/ce72/vja/commit/c8a387244ee86728241970d86e8b59d259a90c40))
* fix version number ([a985a5e](https://gitlab.com/ce72/vja/commit/a985a5e28f2b1212a4a4f48aa41eadb0dacebcd3))
* fix version number ([4518c3f](https://gitlab.com/ce72/vja/commit/4518c3fa5343762c2eaaa05ab2e60c61294b9b6a))
* fix version number ([cc346c7](https://gitlab.com/ce72/vja/commit/cc346c7aea5b2486a79be2f142801c209adf82d7))
* install coverage from requirements_dev.txt ([9b03ba1](https://gitlab.com/ce72/vja/commit/9b03ba180ceb1a9d8125a4713a5e2799777e4e36))
* pipeline on branches only manual ([9b05c2d](https://gitlab.com/ce72/vja/commit/9b05c2ddaf778f179a7ddd16a56fa1d5d9b5b5fc))
* pipeline on branches only manual ([3a936d9](https://gitlab.com/ce72/vja/commit/3a936d9a0425ca3c6c87c61b526e87b7474398c3))
* remove build stage ([8e4f36c](https://gitlab.com/ce72/vja/commit/8e4f36cee4ebaff4fcf3c703e6e1b265d955d302))
* remove build stage ([e4858e3](https://gitlab.com/ce72/vja/commit/e4858e363aed6369ef29ef0fe3ed56115083a11b))
* remove build stage ([e27df75](https://gitlab.com/ce72/vja/commit/e27df75b220380148aab79e75af0e5194041d381))
* remove build stage ([49d2fe2](https://gitlab.com/ce72/vja/commit/49d2fe2d4261fa993aa06365fd004876d8fff055))
* remove build stage ([1661721](https://gitlab.com/ce72/vja/commit/166172141e63f3ef22c576196aacaf7de5bea227))
* remove redundant apk packages ([bf6c0ea](https://gitlab.com/ce72/vja/commit/bf6c0eae179929555ecba1315d19683f052a046e))
* remove redundant apk packages ([a34a24d](https://gitlab.com/ce72/vja/commit/a34a24d396bb508d4635bc1cb405d3ab9d6bbdc7))
* update semantic-release configuration ([de4df86](https://gitlab.com/ce72/vja/commit/de4df867ec80fbead7e8831edbc8d38fd46e0a76))
* wait for running api container ([60d6915](https://gitlab.com/ce72/vja/commit/60d6915845050c5b5b8e528feea69a42f8bbe5d3))


## [1.5.0](https://gitlab.com/ce72/vja/compare/1.4.1...1.5.0) (2023-03-31)


### Features

* defer task ([af87d8a](https://gitlab.com/ce72/vja/commit/af87d8acd821b36609c95fccd4a77ffea96e4b08))


### Misc

* **deps:** update all dependencies ([5abe98f](https://gitlab.com/ce72/vja/commit/5abe98f0e32d450930f2d28f904ea2a565e1b011))

## [1.4.1](https://gitlab.com/ce72/vja/compare/1.4.0...1.4.1) (2023-03-17)


### Bug Fixes

* multiple edit only worked for one task ([dac74af](https://gitlab.com/ce72/vja/commit/dac74afb9ccffafcd2205313b11aba06ca7be85d))

## [1.4.0](https://gitlab.com/ce72/vja/compare/1.3.2...1.4.0) (2023-03-14)


### Features

* more command aliases (create and copy) ([70d936d](https://gitlab.com/ce72/vja/commit/70d936d9e751be3e4f311193e416db463482cd61))
* remove workaround to set position when adding task ([1409895](https://gitlab.com/ce72/vja/commit/140989542a06f2dcb1ca8dafddbb104b973992de))
* vja clone <taskId> <new title> ([4b15fbc](https://gitlab.com/ce72/vja/commit/4b15fbca6237e0e6bc00d19c6091e6f6ada46c33))


### Misc

* **deps:** update all dependencies ([2ad612b](https://gitlab.com/ce72/vja/commit/2ad612bfcbd6aa489c48e25d15be891d25c5f21e))
* update vikunja version ([6239c97](https://gitlab.com/ce72/vja/commit/6239c9751e241ee5b25b51c7a8d7e125ce677e0d))

## [1.3.2](https://gitlab.com/ce72/vja/compare/1.3.1...1.3.2) (2023-03-02)


### Bug Fixes

* open <task_id> does not open task in browser ([58c6dce](https://gitlab.com/ce72/vja/commit/58c6dcea20df8e8ed35c30e4edda5c6e1e6178f6))
* Respect existing reminder dates. Edit only first one. ([28afc65](https://gitlab.com/ce72/vja/commit/28afc652c1d4eaca960b13580e89c004214501ef))


### Automation

* Add test for combining general filter ([0c94125](https://gitlab.com/ce72/vja/commit/0c941250af961e6b8574e7ecc8f8b1ea8f283b5d))

## [1.3.1](https://gitlab.com/ce72/vja/compare/1.3.0...1.3.1) (2023-02-26)


### Bug Fixes

* Allow multiple --filter options ([c2ec9d4](https://gitlab.com/ce72/vja/commit/c2ec9d4f73c22e351c3421ff1131d75d9e9fe58a))
* Allow multiple --filter options ([9361f27](https://gitlab.com/ce72/vja/commit/9361f274068804c2b05c79a8b76483d4a1322f89))
* Parse timedelta in order to filter on repeat_after ([ce6e6e8](https://gitlab.com/ce72/vja/commit/ce6e6e8cfbeadf50487b86c1c54381b154c35fad))

## [1.3.0](https://gitlab.com/ce72/vja/compare/1.2.1...1.3.0) (2023-02-23)


### Features

* Make urgency calculation configurable ([5013825](https://gitlab.com/ce72/vja/commit/501382551f3f677a40649f8b2a446a6fa5c16500))


### Misc

* Remove and .gitignore .vscode folder ([bb7b668](https://gitlab.com/ce72/vja/commit/bb7b6683736123bdbf1131ac7b07fb0dc36f37da))


### Documentation

* Describe configuration in more detail ([f50246b](https://gitlab.com/ce72/vja/commit/f50246b113ec0e4c1a234790794985e2070d86c2))
* Formatting and Spelling of help text ([3e2233f](https://gitlab.com/ce72/vja/commit/3e2233fc4fc87f8a7301f795ca80d5d28afea370))


### Improvements

* Code style ([fe6553b](https://gitlab.com/ce72/vja/commit/fe6553b28d6f27ae7610b852a1974bcbd7c3ac46))

## [1.2.1](https://gitlab.com/ce72/vja/compare/1.2.0...1.2.1) (2023-02-22)


### Documentation

* Extend Features.md ([a06e8c5](https://gitlab.com/ce72/vja/commit/a06e8c5cacbac7d5424421703a5e08d7245ed8a7))


### Improvements

* Use general filters where possible ([6452679](https://gitlab.com/ce72/vja/commit/6452679080577a71e403451c3d839fcf90b4cefb))

## [1.2.0](https://gitlab.com/ce72/vja/compare/1.1.0...1.2.0) (2023-02-21)


### Features

* arbitrary filter with vja ls --filter="<field> <operator> <value>" ([e408195](https://gitlab.com/ce72/vja/commit/e4081958b9916ef2f59f1f5a8aa05626bab12bf6))


### Automation

* Always release on main branch (remove "manual") ([56e28e9](https://gitlab.com/ce72/vja/commit/56e28e9b492eaf58316fab7cda622d094fa24bbd))


### Improvements

* Simplify sort by dates with NoneType ([ee902b1](https://gitlab.com/ce72/vja/commit/ee902b1dc8bfe66a00811a75c62c543d690c3f5c))

## [1.1.0](https://gitlab.com/ce72/vja/compare/1.0.6...1.1.0) (2023-02-21)


### Features

* Ignore case when sorting text fields ([d7464b6](https://gitlab.com/ce72/vja/commit/d7464b6aa55cda1007c7a932f507f1096f9a79e1))
* Support sorting with sort=label|labels|tag|tags ([04ce769](https://gitlab.com/ce72/vja/commit/04ce769664c45e3430ecc219a9450d8ae1ac78bd))


### Documentation

* spelling fixes ([37d46cb](https://gitlab.com/ce72/vja/commit/37d46cbebce339b205790316b9860d256900dd37))


### Automation

* Improve test robustness ([a2779f7](https://gitlab.com/ce72/vja/commit/a2779f78f6f1d7ba2e0a272d1fc798523c98e632))
* use the (smaller) requirements_ci.txt for release stage ([33143c9](https://gitlab.com/ce72/vja/commit/33143c9c8771b6c8582a435bf649850082caa977))

## [1.0.6](https://gitlab.com/ce72/vja/compare/1.0.5...1.0.6) (2023-02-20)


### Automation

* @semantic-release/gitlab to create gitlab release ([ca1c1bc](https://gitlab.com/ce72/vja/commit/ca1c1bc1287214463f35aff0cd7c68964f9836ae))

## [1.0.5](https://gitlab.com/ce72/vja/compare/1.0.4...1.0.5) (2023-02-20)


### Automation

* simplify ci pipeline ([e771908](https://gitlab.com/ce72/vja/commit/e771908dd17323657ceb11ec4f966d7673216ffd))

## [1.0.4](https://gitlab.com/ce72/vja/compare/1.0.3...1.0.4) (2023-02-20)


### Automation

* let sematic-release manage pypi upload ([ea501a5](https://gitlab.com/ce72/vja/commit/ea501a549566f9a94c031e811c078fa752a54eb2))
* manage version in setup.cfg file ([af2afdc](https://gitlab.com/ce72/vja/commit/af2afdc3e9e6bec8644723d6a7a7c11dbeaf9e3f))

## [1.0.3](https://gitlab.com/ce72/vja/compare/1.0.2...1.0.3) (2023-02-20)


### Automation

* .releaserc in yaml format for better editing ([310621c](https://gitlab.com/ce72/vja/commit/310621c46dd88abe3decc8fe949acf249ca11e1d))
* recreate CHANGELOG.md ([5a42e31](https://gitlab.com/ce72/vja/commit/5a42e31fbc35600a6059591601ac99a9a3535f80))
* regenrate changelog with pip install git-changelog ([402391b](https://gitlab.com/ce72/vja/commit/402391b84c9db21a6367cad1985aeb5e2cb01b99))
* regenrate changelog with pip install git-changelog ([c841455](https://gitlab.com/ce72/vja/commit/c8414559c6203f3f481986399826cd0a1d818cd7))

##  (2023-02-20)


### Automation

* regenrate changelog with pip install git-changelog ([402391b](https://gitlab.com/ce72/vja/commit/402391b84c9db21a6367cad1985aeb5e2cb01b99))
* regenrate changelog with pip install git-changelog ([c841455](https://gitlab.com/ce72/vja/commit/c8414559c6203f3f481986399826cd0a1d818cd7))

### [1.0.2](https://gitlab.com/ce72/vja/compare/1.0.1...1.0.2) (2023-02-20)


### Automation

* trying to get Changelog creation right ([05e1181](https://gitlab.com/ce72/vja/commit/05e1181a5cfe20d781d2f36679bf1bf6c859a96b))


### Misc

* Release 1.0.2 ([fa5616c](https://gitlab.com/ce72/vja/commit/fa5616c7a708f5d156f4014696c4a4e5402f3fef))

### [1.0.1](https://gitlab.com/ce72/vja/compare/1.0.0...1.0.1) (2023-02-20)


### Automation

* trying to get Changelog creation right ([e58998e](https://gitlab.com/ce72/vja/commit/e58998e0e70ea98f51b61766766fd20ffe8fccc2))


### Misc

* Release 1.0.1 [skip ci] ([d4eb6ab](https://gitlab.com/ce72/vja/commit/d4eb6ab3ff3a1a758edf8a5f42ec3379f34fd38f))

## [1.0.0](https://gitlab.com/ce72/vja/compare/0.5.2...1.0.0) (2023-02-20)


### Misc

* prepare for release 1.0.0 ([72d1631](https://gitlab.com/ce72/vja/commit/72d16314ab1abcbefab8784e85fc8c628558d92e))

### [0.5.2](https://gitlab.com/ce72/vja/compare/0.5.1...0.5.2) (2023-02-20)


### Automation

* generate changelog ([f32c8ab](https://gitlab.com/ce72/vja/commit/f32c8abd390ece90b7c837b6a571340544f01688))


### Misc

* Release 0.5.2 [skip ci] ([12e24f6](https://gitlab.com/ce72/vja/commit/12e24f6a11948df6bd210999d43c967d1356502b))

### [0.5.1](https://gitlab.com/ce72/vja/compare/0.5.0...0.5.1) (2023-02-20)


### Automation

* generate changelog ([fea4e4c](https://gitlab.com/ce72/vja/commit/fea4e4c5583c94fd33fdaf6d8d6c03f9536e19b8))
* generate changelog ([389bb9a](https://gitlab.com/ce72/vja/commit/389bb9a6c1a3d22a6bdfa121e13b133c50a7b119))


### Misc

* Release 0.5.1 [skip ci] ([d91bb63](https://gitlab.com/ce72/vja/commit/d91bb638570d7f8c36434eabd5d0e0159908ab9a))
* Release 1.0.0 [skip ci] ([0cd68ca](https://gitlab.com/ce72/vja/commit/0cd68ca0af9d7c243a6a944abd69c4d95facc2da))

## [0.5.0](https://gitlab.com/ce72/vja/compare/0.4.1...0.5.0) (2023-02-20)


### Features

* add bucket filter ([9c82c5b](https://gitlab.com/ce72/vja/commit/9c82c5b0b676389e5d68bc8bcfdb1627b4f539cd))
* sort tasks ([10a827f](https://gitlab.com/ce72/vja/commit/10a827f8538e0988804f6825fcb2391c1a55264f))


### Misc

* **deps:** update dependency pip to v23.0.1 ([d599a94](https://gitlab.com/ce72/vja/commit/d599a94569b4cd96f25c371744e58f7818cf13d0))

### [0.4.1](https://gitlab.com/ce72/vja/compare/0.4.0...0.4.1) (2023-02-19)


### Bug Fixes

* parsed time defaults to 00:00 ([60d0875](https://gitlab.com/ce72/vja/commit/60d087513072c5ea465d406ba15a8bd532a41e35))

## [0.4.0](https://gitlab.com/ce72/vja/compare/0.3.1...0.4.0) (2023-02-19)


### Features

* filter by due-date with conditional operators (lt,le,gt, ge, before/after) ([89bd55b](https://gitlab.com/ce72/vja/commit/89bd55ba9fe27a7606a0decb042be7f448a95743))
* filter by priority with conditional operators (lt..eq..gt..) ([abfc72c](https://gitlab.com/ce72/vja/commit/abfc72c2ac817ab3158f6a6f37403eaa3293b70f))


### Misc

* refactor filtering logic ([2ac9d07](https://gitlab.com/ce72/vja/commit/2ac9d07f69c0a84478a92dd66309c4e81099c3b6))

### [0.3.1](https://gitlab.com/ce72/vja/compare/0.3.0...0.3.1) (2023-02-19)


### Features

* filter tasks with empty labels (vja ls --label='') ([d51d4a3](https://gitlab.com/ce72/vja/commit/d51d4a36d91496833059d9ca367118dd011ee299))
* filter tasks with empty labels (vja ls --label='') ([7fd72f2](https://gitlab.com/ce72/vja/commit/7fd72f2b49047357b9abfd584050193dca6710ef))
* filter tasks with empty labels (vja ls --label='') ([4df7e91](https://gitlab.com/ce72/vja/commit/4df7e91b9f484fde0e76dcc47e4c54edf3ceb1fc))
* show done_at date ([edd360c](https://gitlab.com/ce72/vja/commit/edd360c73909d58beed2d94910a304f5c320dfa7))


### Documentation

* update pypi badge ([1a6813b](https://gitlab.com/ce72/vja/commit/1a6813b4f2305800ea6353c1661d9abb9ad2afad))

## [0.3.0](https://gitlab.com/ce72/vja/compare/0.1.6...0.3.0) (2023-02-19)


### Features

* add brief description of ls output format ([bdbac99](https://gitlab.com/ce72/vja/commit/bdbac99d89d0619267b498b234868b948d32e3e6))
* add task with list name ([0c68174](https://gitlab.com/ce72/vja/commit/0c68174479d94db3af1be381ddb3437f1b6c6bb5))
* append to note (vja edit --note-append ([b1a1212](https://gitlab.com/ce72/vja/commit/b1a1212709e9c4365bdd7b402516ea35e8942c6f))
* Custom output format with --custom-format ([e587691](https://gitlab.com/ce72/vja/commit/e5876918309c8b38e01c3339f7cabbaeac622b6e))
* display more attributes from vja show ([84f1df7](https://gitlab.com/ce72/vja/commit/84f1df7094946dabbca8c9d6f48ac42587e47053))
* display result after add and edit ([af850d0](https://gitlab.com/ce72/vja/commit/af850d0dff73b63fc1cfe234f09270507a95bff3))
* edit --list-id, allowing to move task between lists ([6fa5e0f](https://gitlab.com/ce72/vja/commit/6fa5e0f8ce8b9bff56145100eefedee2f140cb6f))
* log absolute path to config ([252beca](https://gitlab.com/ce72/vja/commit/252beca7a432ce71325a23360dfeec11ab76a1ad))
* regard user.settings.default_list_id ([17e3ca0](https://gitlab.com/ce72/vja/commit/17e3ca085f235f4c8020bd1c3cea93ad141938f2))
* reminder=due to set reminder=due_date ([b987828](https://gitlab.com/ce72/vja/commit/b9878283e8f915cf6aa519622ddc3f715f6dd074))
* show and edit multiple task ids ([eac4b70](https://gitlab.com/ce72/vja/commit/eac4b7067b10beda309fab02d44c7218df2fc030))
* support paging when reading json ([4165aff](https://gitlab.com/ce72/vja/commit/4165aff7273d42f7df23b9a3c868b11e18c20e33))
* use click.echo instead of print ([8210ce2](https://gitlab.com/ce72/vja/commit/8210ce2967203650afe08cbf9e4810d17b4219df))


### Bug Fixes

* accept iso formatted date args ([83e3b01](https://gitlab.com/ce72/vja/commit/83e3b016f717243237b3103bcae831610db56a98))
* data_dict for arrays ([0c082bc](https://gitlab.com/ce72/vja/commit/0c082bc2b6e434395daa766951b5716a869126ad))
* refactor output and add tests ([6bce1f3](https://gitlab.com/ce72/vja/commit/6bce1f337b60c8687f08901fee90288d3ac87aac))
* refactor output and add tests ([a4f4b08](https://gitlab.com/ce72/vja/commit/a4f4b08d3d0f31da931d82f9498ecfb0096b9f20))
* remove deprecation warning from parsedatetime ([d031bb0](https://gitlab.com/ce72/vja/commit/d031bb0b990f83287b9b48edbe377fb24d26756b))
* remove pytest.ini ([26231d4](https://gitlab.com/ce72/vja/commit/26231d4963dfe5c048fb8ad450a5b185992dfdbc))
* toggle done does not overwrite other fields ([97dd074](https://gitlab.com/ce72/vja/commit/97dd07471c3d90050c7ada395124a25e814ba800))


### Documentation

* extend help texts and Features.md ([c8980b4](https://gitlab.com/ce72/vja/commit/c8980b47146310646a70d4ae4c39cb4447d315ff))
* update Readme.md ([0edf8c0](https://gitlab.com/ce72/vja/commit/0edf8c0108ea0b5f73de40408a03d5554dcbe3f2))


### Automation

* add some badges to readme ([be3237c](https://gitlab.com/ce72/vja/commit/be3237cd5cea96744e516b8d8f233838af6d22b9))
* disable vikunja server rate limit ([37eb25a](https://gitlab.com/ce72/vja/commit/37eb25acd96e6ba5a9aaa987386ff6dcc80f59e3))
* more of them ([0d195d4](https://gitlab.com/ce72/vja/commit/0d195d4bc7634b4b90f3ec3fd61c3eb545271c13))
* more of them ([8d19381](https://gitlab.com/ce72/vja/commit/8d193810357a2f1f42510f38776c7c2efc7f2ebb))
* simplify test setup; preparing to migrate to pytest ([45e8dbe](https://gitlab.com/ce72/vja/commit/45e8dbeb4b3f254e046522a88ae6cbe5a357b722))
* simplify test setup; preparing to migrate to pytest ([12727e7](https://gitlab.com/ce72/vja/commit/12727e7c42163e107573bb4582934b046eb806ed))
* simplify test setup; preparing to migrate to pytest ([ced4635](https://gitlab.com/ce72/vja/commit/ced463510c12316ff1b281fdb712ce4bed87229a))
* simplify test setup; preparing to migrate to pytest ([529659d](https://gitlab.com/ce72/vja/commit/529659daae69019a5d82681caa591aca1a639084))
* simplify test setup; preparing to migrate to pytest ([559a514](https://gitlab.com/ce72/vja/commit/559a514acea40203309e1430e8314145394dc0fa))
* test renew token ([b3141cf](https://gitlab.com/ce72/vja/commit/b3141cfee58e1e4d66b7d91321331ad4f54818d1))


### Misc

* clean up model code ([03c3938](https://gitlab.com/ce72/vja/commit/03c39388c6a77b31e3614c5ab4b365a73744dcff))
* code clean up ([5bc733d](https://gitlab.com/ce72/vja/commit/5bc733d127aa14a22f9de0c2070bb58690af1bd0))
* **deps:** update all dependencies ([5bda8b5](https://gitlab.com/ce72/vja/commit/5bda8b5e2468eee2d623981f4e807cf6e5f861a2))
* enable renovate for requirements_dev.txt ([f5cc9f4](https://gitlab.com/ce72/vja/commit/f5cc9f434f201958f08c7f633947a5af2802c0bc))
* make methods private ([1bc1bcc](https://gitlab.com/ce72/vja/commit/1bc1bccfaf3ceca3ef890d50351a607b3b9c0144))
* prepare 0.3.0 release ([c5be207](https://gitlab.com/ce72/vja/commit/c5be207fa43f50768fe33407c33aaa3a5b83cb3b))
* refactor tests ([b2fdd0d](https://gitlab.com/ce72/vja/commit/b2fdd0db1a64e98b8acfb9e3d0fb64fe2aff94af))
* test coverage badge ([e75db76](https://gitlab.com/ce72/vja/commit/e75db767a5221c658b4cc01d6af2f22b49964be4))
* test coverage badge ([4704edb](https://gitlab.com/ce72/vja/commit/4704edbf9711c1df9479e24f6d168d5a2f0c1a31))
* test coverage badge ([26f06e6](https://gitlab.com/ce72/vja/commit/26f06e6d593d2cc5022e30788207ebff0571db08))
* test coverage badge ([361b4a5](https://gitlab.com/ce72/vja/commit/361b4a51f7b3e813189153633b95b31b9e4032ee))
* test coverage badge ([bf5514a](https://gitlab.com/ce72/vja/commit/bf5514ae95232ef4fcfc2818b36a2133f031dd69))

### [0.1.5](https://gitlab.com/ce72/vja/compare/1a6561161ba3434df3542807f51e4d620678c648...0.1.5) (2023-02-07)


### Improvements

* data_dict per class decorator ([1a65611](https://gitlab.com/ce72/vja/commit/1a6561161ba3434df3542807f51e4d620678c648))
