# PIQARD - Prompted Intelligent Question Answering with Retrieval of Documents
### Setting Up the Environment
1. Create the virtual environment using `virtualenv`
```bash
virtualenv env --python==python3.9
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

### Prepare modules
To reach the full potential of the PIQARD you should prepare several module configurations.
#### Google Custom Search
##### Credentials
To use `GoogleCustomSearch` class you have to put a `google_custom_search.json` file containing `engineID` and `APIkey` in `assets\credentials` directory.
```json
{
  "engineID": "",
  "APIkey": ""
}
```

* **Custom Search Engine** - if you don't have access to google search engine you should visit [SearchEngine](https://programmablesearchengine.google.com/controlpanel/all) and create a new one.

* **API key** - to get your own API key you have to visit [APIkey](https://developers.google.com/custom-search/v1/introduction).


#### BLOOM 176b API and GPT-j6b API
##### API key
Model works thanks to [huggingface](https://huggingface.co/settings/tokens) Inference API.

To use `BLOOM176bAPI` or `GPTj6bAPI` class you have to put a `huggingface.json` file containing `APIkey` in `assets\credentials` directory.
```json
{
  "APIkey": ""
}
```

### Usage from cmd
* basic usage for Question-Answer system inference
```bash
python main.py [-h] [--config CONFIG] [--output OUTPUT] query
```
* testing on a selected benchmark (default RealTimeQA)
```bash
python test.py [-h] [--config CONFIG] [--output OUTPUT] benchmark
```

### Custom configuration
* to create custom configuration use the template below:
```yaml
information_retriever: !VectoreRetriever
  database: openbookqa
prompt_template: prompting/templates/context_prompt.txt
context_builder: !TruncatedContextBuilder
language_model: !BLOOM176bAPI
```
####Available modules
  * **information_retriever:**
    * !GoogleCustomSearch
    * !RankingRetriever
    * !VectoreRetriever
    * None (if you don't want to include retriever you need to comment the retriever part)
      ```yaml
      #      information_retriever: 
      #    database: 
      ```

  * **prompt_template:**
    * choose one from `assets/prompting_templates` directory
  * **context_builder:**
    * !TruncatedContextBuilder
    * !MergedContextBuilder
  * **language_model:**
    * !BLOOM176nAPI
    * !GPTj6bAPI
  

### PIQARD platform
We create user interface in React, which allow to play around custom configurations, prompts and questions.
To run the web application:
1. Install dependencies in `piqard-app` directory:
```bash
npm install
```
2. Run app and api instances:
```bash
run_piqard_platform.bat
```
