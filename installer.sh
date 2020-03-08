#!/bin/bash

model_directory="./models"
decomposable_attention_model="decomposable-attention-elmo-2018.02.19.tar.gz"
decomposable_attention_model_path="${model_directory}/${decomposable_attention_model}"
decomposable_attention_model_url="https://s3-us-west-2.amazonaws.com/allennlp/models/decomposable-attention-elmo-2018.02.19.tar.gz"

if [ -e $decomposable_attention_model_path ]
then
    echo "ok"
else
    mkdir -p -- "$model_directory"
    cd $model_directory
    wget $decomposable_attention_model_url
fi