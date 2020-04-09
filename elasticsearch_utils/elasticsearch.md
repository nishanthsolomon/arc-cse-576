# Curl requests used in elastic search

#### 1. List the indices

    curl 'localhost:9200/_cat/indices?v'

#### 2. Creating a index with shingle analyzer

  1. Defining a custom analyzer<br>
    
    curl -XPUT 'localhost:9200/arc_corpus_shingle?pretty' -H 'Content-Type: application/json' -d'
    {
        "settings": {
            "number_of_shards": 2,  
            "analysis": {
                "filter": {
                    "my_stop": {
                        "type":       "stop",
                        "stopwords":  "_english_"
                    },
                    "my_shingle_filter": {
                        "type":             "shingle",
                        "min_shingle_size": 2, 
                        "max_shingle_size": 2, 
                        "output_unigrams":  false   
                    }
                },
                "analyzer": {
                    "my_shingle_analyzer": {
                        "type":             "custom",
                        "tokenizer":        "standard",
                        "stopwords": "_english_",
                        "filter": [
                            "lowercase",
                            "my_stop",
                            "my_shingle_filter"
                        ]
                    }
                }
            }
        }
    }
    '
  2. Testing the custom analyzer

    curl -XPOST 'localhost:9200/arc_corpus_shingle/_analyze?pretty' -H 'Content-Type: application/json' -d'
    {
        "analyzer": "my_shingle_analyzer",
        "text": "Large international companies are involved in bauxite, iron ore, diamond, and gold mining operations."
    }
    '
  3. Mapping to the index

    curl -XPUT 'localhost:9200/arc_corpus_shingle/_mapping?pretty' -H 'Content-Type: application/json' -d'
    {
        "properties": {
            "data": {
                "type": "text",
                "fields": {
                    "shingles": {
                        "type":     "text",
                        "analyzer": "my_shingle_analyzer"
                    }
                }
            }
        } 
    }
    '
  4. Checking the mapping of the index

    curl -X GET "localhost:9200/arc_corpus_shingle/_mapping?pretty"

#### 3. Searching using the custom analyzer

    curl -XGET 'http://localhost:9200/arc_corpus_shingle/_search?pretty' -H 'Content-Type: application/json' -d'
    {
        "size": 10,
        "query": {
            "bool": {
                "must": {
                    "match": {
                    "data": "Clean and organize around the house."
                    }
                },
                "should": {
                    "match": {
                    "data.shingles": "Clean and organize around the house."
                    }
                }
            }
        }
    }
    '