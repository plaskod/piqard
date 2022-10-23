# Google Custom Search

### Usage from cmd
```bash
gcs.py [-h] --query QUERY [--start-date START_DATE] [--end-date END_DATE] [--out-file OUT_FILE]
```

### Credentials
To use `GoogleCustomSearch` class you have to put a `credentials.json` file containing `engineID` and `APIkey` in this directory.
```json
{
  "engineID": "",
  "APIkey": ""
}
```

#### Custom Search Engine 
If you don't have access to google search engine you should visit [SearchEngine](https://programmablesearchengine.google.com/controlpanel/all) and create a new one.

#### API key
To get your own API key you have to visit [APIkey](https://developers.google.com/custom-search/v1/introduction).

