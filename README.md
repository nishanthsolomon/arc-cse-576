# arc-cse-576
Repository for CSE 576 course project

1. Install the required packages as in requirements.txt
2. Run the installer.sh to download the required models.
3. Run textual_entailment.py to check the entailment score.

## ElasticSearch and Kibana configuration

Installation: https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html, https://www.elastic.co/guide/en/kibana/current/install.html

Run both Elasticsearch and Kibana locally: https://www.elastic.co/guide/en/elasticsearch/reference/current/starting-elasticsearch.html, https://www.elastic.co/guide/en/kibana/current/start-stop.html

Download the ARC dataset (https://leaderboard.allenai.org/arc/submissions/get-started) and place the three files in the `./data` folder. Name them appropriately as per the script -- `train.jsonl`, `dev.jsonl`, `test.jsonl`.

## indexer.py

Ensure Elasticsearch is running. The script creates 3 indices in the elastic search node running locally -- `train_data`, `dev_data` and `test_data`. Use Kibana's dashboard or curl to query for the stored indices.
