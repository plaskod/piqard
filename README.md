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

### Usage from cmd
* basic usage for Question-Answer system inference
```bash
python main.py [-h] --query QUERY
```
* testing on a selected benchmark (default RealTimeQA)
```bash
python test.py [-h] [--output] BENCHMARK
```