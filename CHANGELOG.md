## [2.0.0-beta.2](https://gitlab.com/ce72/vja/compare/2.0.0-beta.1...2.0.0-beta.2) (2023-04-02)


### Features

* rename lists to project within vja ([f757117](https://gitlab.com/ce72/vja/commit/f75711797d887ffee8cd5b3ab7ec7edb8044494e))

## [2.0.0-beta.1](https://gitlab.com/ce72/vja/compare/1.5.0...2.0.0-beta.1) (2023-04-01)


### ⚠ BREAKING CHANGES

* **api:** remove reminder_dates
* **api:** New projects api (only backend side)
* Preliminary support for new reminder array

### Features

* **api:** New projects api (only backend side) ([157aeb4](https://gitlab.com/ce72/vja/commit/157aeb483fa2b5d3b1d733f7682c97c8e449aebc))
* **api:** remove reminder_dates ([76ffb20](https://gitlab.com/ce72/vja/commit/76ffb2007cf77d87e41b8cdb8bf16a0f9d4edf26))
* defer reminder ([c493b07](https://gitlab.com/ce72/vja/commit/c493b07266affc2f6976a5682b1b33170c90e51b))
* Preliminary support for new reminder array ([eb7e819](https://gitlab.com/ce72/vja/commit/eb7e819b08b897eeb55e0a18320a03a11442ce91))
* **reminders:** Set relative reminders like "1h before due" ([f05438d](https://gitlab.com/ce72/vja/commit/f05438d9f8c61ee04cb5432b2e1e0d0a56ff2175))
* Support for new reminder array (read) ([c323c76](https://gitlab.com/ce72/vja/commit/c323c76fcb52541a00e35d1e5c31a668eb061405))


### Bug Fixes

* do not unset reminder if missing in vja edit ([a3b81b0](https://gitlab.com/ce72/vja/commit/a3b81b0bae08841fd92e204d5557cc1ad46a59b3))
* sharpen test ([4c59738](https://gitlab.com/ce72/vja/commit/4c59738a19bb4dabd1b871d54ba40f8833b2fe10))


### Misc

* Remove redundant test ([2901848](https://gitlab.com/ce72/vja/commit/29018480b6a11c2ec3495ce6e44c4955fe6b13ec))


### Documentation

* Add table of contents to Features.md ([3a87061](https://gitlab.com/ce72/vja/commit/3a87061f39b2bf4d2a1194197f5cfef3c8d7d46e))


### Automation

* automate beta releases ([8f19e48](https://gitlab.com/ce72/vja/commit/8f19e48db1312db3e6d27716a692b95805ef82d1))
* automate beta releases ([1c74fda](https://gitlab.com/ce72/vja/commit/1c74fdab9e9b02fc116a1532b081b562e9dbf832))
* automate beta releases ([8f7bb4f](https://gitlab.com/ce72/vja/commit/8f7bb4f9802ec6e199d5f7dd60790341550a1785))
* automate beta releases ([68bd7d8](https://gitlab.com/ce72/vja/commit/68bd7d8ee3b3579c3f48b3b8d13d2780f5194641))
* capture click output ([9aafa2c](https://gitlab.com/ce72/vja/commit/9aafa2c426757b2068a1199410db58899356eacd))
* cleanup gitlab-ci ([450d13f](https://gitlab.com/ce72/vja/commit/450d13fe43987c3cf33c72bfa2303e452ee7be8b))
* cleanup gitlab-ci ([543a479](https://gitlab.com/ce72/vja/commit/543a47928a9539982a91507ece4e9d3605bb2dbb))
* cleanup gitlab-ci ([7145451](https://gitlab.com/ce72/vja/commit/714545181a76b15c4341df3a4ff6830416ddf897))
* cleanup gitlab-ci ([9584cac](https://gitlab.com/ce72/vja/commit/9584cac6e18e81480231b34fabd46990249a2760))
* cleanup test setup ([5e5040a](https://gitlab.com/ce72/vja/commit/5e5040a3254b8cc5dc75f0391352e0e1358fdeaa))
* install coverage from requirements_dev.txt ([eab4b0f](https://gitlab.com/ce72/vja/commit/eab4b0f4ef879c64859c9796f2562b09eaa53320))
* pipeline on branches only manual ([43fa7df](https://gitlab.com/ce72/vja/commit/43fa7df6ec8fe69eb8d9d27589b65b9541b0b71a))
* pipeline on branches only manual ([8689f5e](https://gitlab.com/ce72/vja/commit/8689f5e0a36a536187a9df97dd38a2a0ece9ed01))
* remove build stage ([3294b83](https://gitlab.com/ce72/vja/commit/3294b83e1b75b2b6826333104d91e71ee1b8d478))
* remove build stage ([8bca866](https://gitlab.com/ce72/vja/commit/8bca866c60f3ed2cf62eeb87cd10dad06f9563e6))
* remove build stage ([4638743](https://gitlab.com/ce72/vja/commit/46387430fe4c92a02b818e200672c86ed4190e1a))
* remove build stage ([5b32e53](https://gitlab.com/ce72/vja/commit/5b32e53277c3ee95464eb1d60f2c270dccb5bf4b))
* remove build stage ([7dd6dcb](https://gitlab.com/ce72/vja/commit/7dd6dcbf9f8c373a9d8b33b8c17d29c559cc1075))
* remove redundant apk packages ([22a3f48](https://gitlab.com/ce72/vja/commit/22a3f48391bc8434fcb208d31e4db50f701b8c68))
* remove redundant apk packages ([efb7016](https://gitlab.com/ce72/vja/commit/efb701685d11bad90eb844ac8636117225ab2f7c))
* sleep 1s after starting api ([649a806](https://gitlab.com/ce72/vja/commit/649a8063a39f76f91196c0f6f8261f5033f95d52))
* update semantic-release configuration ([572f519](https://gitlab.com/ce72/vja/commit/572f519a10bc97e9badb017f90b5e723eecc8e42))

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
