# arc-cse-576
Repository for CSE 576 course project

1. Install the required packages as in requirements.txt
2. Run the installer.sh to download the required files.
3. Run python main.py --path --num_rows to analyze the ARC Challenge test corpus.

## Installer

Run installer.sh to download the models and the dataset.

## ElasticSearch and Kibana configuration

Installation: https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html, https://www.elastic.co/guide/en/kibana/current/install.html

Run both Elasticsearch and Kibana locally: https://www.elastic.co/guide/en/elasticsearch/reference/current/starting-elasticsearch.html, https://www.elastic.co/guide/en/kibana/current/start-stop.html

Download the ARC dataset (https://s3-us-west-2.amazonaws.com/ai2-website/data/ARC-V1-Feb2018.zip) and place the files in the `./dataset` folder. 

## Indexing

Ensure Elasticsearch is running. Use the curl requests in [elasticsearch.md](./elasticsearch_utils/elasticsearch.md) to create the index. Run the script indexer.py, it creates 1 index in the elastic search node running locally -- `arc_corpus`. Use Kibana's dashboard or curl to query for the stored indices.
