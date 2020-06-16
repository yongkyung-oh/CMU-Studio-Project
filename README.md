# CMU-Studio-Project
Check the information in the [page](https://yongkyung-oh.github.io/CMU-Studio-Project/).

--------------------------------------------------------------------------------


<p align="center"><img width="70%" src="docs/source/\_static/img/parlai.png" /></p>

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/facebookresearch/ParlAI/blob/master/LICENSE) [![CircleCI](https://circleci.com/gh/facebookresearch/ParlAI.svg?style=shield)](https://circleci.com/gh/facebookresearch/ParlAI/tree/master) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/facebookresearch/ParlAI/blob/master/CONTRIBUTING.md) [![Twitter](https://img.shields.io/twitter/follow/parlai_parley?label=Twitter&style=social)](https://twitter.com/parlai_parley)


--------------------------------------------------------------------------------


This repository is the implementation example of BST (Blended Skill Talk) model based on [Recipes for building an open-domain chatbot](https://parl.ai/projects/recipes/). It has minor modification of websocket and browser examples in the [original source](https://github.com/facebookresearch/ParlAI). Following files are modified.

#### modify `parlai/chat_service/tasks/chat_test/` from `~/chatbot/`
- Changed `config.yml`: Original code is using seq2seq model. In the modification, BST model(Blender 90M) is used.
- Changed `worlds.py`: Cusomize the messages. Add Google searching function by query and quick replies script.

#### modify `parlai/chat_service/services/browser_chat_test/` from `~/browser_chat/`
- Changed `client.py`: Instead of original script code, web_test code is used (interactive_web_test.py).

#### modify `parlai/scripts/interactive_web_test.py` from `~/interactive_web.py`
- Instead of `bulma`, `bootstrap` is implemented. 
- Customize the outlook and JavaScript functions.
- Add timestamp and custom information from `client.py`.


--------------------------------------------------------------------------------


## Installing ParlAI using this repo

ParlAI currently requires Python3.6 and [Pytorch](https://pytorch.org) 1.4. *It does not work with pytorch 1.5*.
Dependencies of the core modules are listed in [`requirements.txt`](https://github.com/facebookresearch/ParlAI/blob/master/requirements.txt). Some
models included (in [`parlai/agents`](https://github.com/facebookresearch/ParlAI/tree/master/parlai/agents)) have additional requirements.

Run the following commands to clone the repository and install ParlAI:

```bash
git clone https://github.com/yongkyung-oh/CMU-Studio-Project.git
cd ~/CMU-Studio-Project; python setup.py develop
```

This will link the cloned directory to your site-packages.

This is the recommended installation procedure, as it provides ready access to the examples and allows you to modify anything you might need. This is especially useful if you want to submit another task to the repository.

All needed data will be downloaded to `~/ParlAI/data`, and any non-data files if requested will be downloaded to `~/ParlAI/downloads`. If you need to clear out the space used by these files, you can safely delete these directories and any files needed will be downloaded again.

This repo is tested with following ParlAI version. `parlai==0.1.20200609`


## Running websocket server and browser example
Original code is referred from [ParlAI document](https://parl.ai/docs/tutorial_chat_service.html). You may need to install 'tornado' to operate websocket by typing `pip install tornado`.

```bash
python parlai/chat_service/services/websocket/run.py --config-path parlai/chat_service/tasks/chat_test/config.yml
```
Running the websocket in the local. It is the same as running the `~/chat_service/services/browser_chat/run.py`. Default port number is 35496.


```bash
python parlai/chat_service/services/browser_chat_test/client.py --host=0.0.0.0
```
Running the web-browser chatbot, which communicate with websocket. Default port number is 8080.


--------------------------------------------------------------------------------

## License
ParlAI is MIT licensed. See the LICENSE file for details.
