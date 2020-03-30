#!/bin/bash


export LC_ALL="en_US.UTF-8"

main()
{
    set -e
    SetVariables
    execution
}
SetVariables()
{
    CUR_DIR=`pwd`
    MODEL_DIR=${CUR_DIR}/models
    DATASET_DIR=${CUR_DIR}/dataset

    TEXTUAL_ENTAILMENT_PATH=${MODEL_DIR}/decomposable-attention-elmo-2018.02.19.tar.gz
    TEXTUAL_ENTAILMENT_URL=https://s3-us-west-2.amazonaws.com/allennlp/models/decomposable-attention-elmo-2018.02.19.tar.gz
    
    ARC_DATASET_PATH=${DATASET_DIR}/ARC-V1-Feb2018
    ARC_DATASET_URL=https://s3-us-west-2.amazonaws.com/ai2-website/data/ARC-V1-Feb2018.zip

}


execution()
{
    #Download Models

    if [ -e ${TEXTUAL_ENTAILMENT_PATH} ]
    then
        echo "TEXTUAL ENTAILMENT MODEL OK."
    else
        mkdir -p -- "${DATASET_DIR}"
        cd ${DATASET_DIR}
        wget $TEXTUAL_ENTAILMENT_URL
        echo "Downloaded TEXTUAL ENTAILMENT MODEL"
    fi

    #Download Dataset

    if [ -e ${ARC_DATASET_PATH} ]
    then
        echo "ARC DATASET OK."
    else
        mkdir -p -- "${DATASET_DIR}"
        cd ${DATASET_DIR}
        wget $ARC_DATASET_URL
        unzip ARC-V1-Feb2018.zip
        echo "Downloaded ARC DATASET"
    fi

}

main $*
