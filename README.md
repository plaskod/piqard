# PIQARD - Prompted Intelligent Question Answering with Retrieval of Documents
We present PIQARD, a question answering system and library that allows users to easily ask open-domain questions and retrieve information from databases and other sources.
The system uses advanced natural language processing techniques to understand and provide human-like answers.
With its easy-to-use and integrate interface, PIQARD makes it simple for developers to add question answering capabilities to their projects.



### Setting Up the Environment
1. Create the virtual environment using `virtualenv`
```bash
virtualenv env --python=python3.9
```
2. Activate the environment
* Windows
```bash
env\scripts\activate
```
3. Install the requirements in the environment:
```bash
pip install -r requirements.txt
```

### PIQARD library
1. Build the PIQARD library
```bash
python setup.py bdist_wheel
```

2. Install the PIQARD library
```bash
pip install dist/piqard-0.0.1-py3-none-any.whl
```

### Setting up environment variables
To reach the full potential of the PIQARD you should prepare several environment variables. 
Below we provide a list of all the variables and their description. You can set them up in cmd using:
```bash
set VARIABLE_NAME=VARIABLE_VALUE
```
or in python files when needed:
```python 
import os
os.environ["VARIABLE_NAME"] = "VARIABLE_VALUE"
```

 
#### Google Custom Search
To use `GoogleCustomSearch` class you have to set up the following environment variables:
* `GOOGLE_CUSTOM_SEARCH_API_KEY` - API key for Google Custom Search API. To get your own API key you have to visit [APIkey](https://developers.google.com/custom-search/v1/introduction).
* `GOOGLE_CUSTOM_SEARCH_ENGINE_ID` - ID of the search engine. If you don't have access to google search engine you should visit [SearchEngine](https://programmablesearchengine.google.com/controlpanel/all) and create a new one.


#### BLOOM 176b API and GPT-j6b API
Models work thanks to [huggingface](https://huggingface.co/settings/tokens) Inference API.

To use `BLOOM176bAPI` or `GPTj6bAPI` class you have to set up the following environment variables:
* `HUGGINGFACE_API_TOKEN` - API token for huggingface. To get your own API token you have to visit [huggingface](https://huggingface.co/settings/tokens) and create a new one.


### Additional assets
In the assets directory, you'll find all the additional files needed for prompt templates and configs.
We've also included two pre-prepared benchmark datasets with questions and documents.
You can download them from the [provided link](https://mega.nz/folder/SMB11YIL#NjNnHwcgICj7yDyvGaql1g)

### Basic usage of PIQARD library
To get started with PIQARD, check out the example below.
This will give you a basic understanding of how to use the library.
For more advanced usage, refer to the other examples provided in the `examples/base_usage.ipynb` notebook.

```python
from piqard.utils.prompt_template import PromptTemplate
from piqard.language_models import CohereAPI
from piqard.information_retrievers import WikiAPI
from piqard import PIQARD

prompt_template = PromptTemplate('./../assets/prompting_templates/like_chat_gpt/with_context.txt')
llm = CohereAPI(stop_token="\n")
ir = WikiAPI(k=10)

piqard = PIQARD(prompt_template=prompt_template,
                language_model=llm,
                information_retriever=ir)

result = piqard("Who is the current CEO of twitter?")
print(result['chain_trace'])
```




### PIQARD config file
PIQARD and extended strategies can be configured using a YAML config file.
The file should be set up as a dictionary, with the keys being the names of the components and the values being the parameters for those components.

To help you get started, we've included an example config file for PIQARD. This will give you an idea of how to set up your own file to customize and optimize the tool for your specific needs.

* example config file: `./assets/configs/example.yaml`

```yaml
prompt_template: !PromptTemplate
  template: assets/prompting_templates/like_chat_gpt/without_context.txt
language_model: !CohereAPI
  stop_token: "\n"
information_retriever: !AnnoyRetriever
  k: 2
  database: "openbookqa"
  database_path: "./../assets/benchmarks/openbookqa/corpus.jsonl",
  database_index: "./../assets/benchmarks/openbookqa/corpus_annoy_index_384.ann"
```

* loading PIQARD from config file:
```python
from piqard.PIQARD_loader import PIQARDLoader

piqard = PIQARDLoader().load("./assets/configs/example.yaml")


result = piqard("Who is the current CEO of twitter?")
print(result['chain_trace'])
```


### PIQARD platform
We create user interface in React, which allow playing around custom configurations, prompts and questions.
Additionally, we propose example configuration which use `SelfAware` strategy.
* **PIQARD API server**
1. Create `config.json` file with required API keys and configuration in `piqard_api` directory.
```json
{
  "COHERE_API_KEY": "",
  "HUGGINGFACE_API_KEY": "",
  "GOOGLE_CUSTOM_SEARCH_API_KEY": "",
  "GOOGLE_CUSTOM_SEARCH_ENGINE_ID": "",
  "OPEN_SYSTEM_CONFIG": "./assets/configs/self_aware_config_piqard_react.yaml"
}
```
2. Run the following command from project root directory:
```bash 
python piqard_api/api.py
```

* **PIQARD APP**
1. Go to `piqard_app` directory and run the following commands:
```bash
npm install
npm start
```


### About 
PIQARD is a project created by [Dawid Plaskowski](), [Mateusz Politycki](), [Marcin Korcz]() and [Alex Terentowicz]() from Poznan University of Technology.
To see our thesis and learn more about the project, visit our [website]().

If you have any questions, feel free to contact us.