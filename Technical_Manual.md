# Technical Manual: Setting up an Information Retrieval System with Docker and Elasticsearch

**Date:** April 8 2025
**Author:** MERCY CHEPKEMOI KEMEI
**ADM NO:** 204820

## 1. Introduction

This manual provides a step-by-step guide for intermediate and advanced IT practitioners on how to set up a functional Information Retrieval (IR) system using Docker and Elasticsearch. Elasticsearch is a powerful open-source search and analytics engine built on Apache Lucene. Docker simplifies the deployment and management of Elasticsearch by encapsulating it within a container.
This manual will cover the following:

* Prerequisites for setting up the environment.
* Pulling and running the Elasticsearch Docker image.
* Preparing a sample corpus of documents.
* Indexing the documents into Elasticsearch.
* Performing basic and advanced queries against the indexed data.

## 2. Prerequisites

Before proceeding, ensure you have the following installed on your system:
* **You can find installation instructions for your operating system on the official software websites**

* **1. Docker:** Ensure Docker Engine and Docker Compose are installed and running. Website ([https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/) and [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)).
* **2. VS Code:** Website (https://code.visualstudio.com/download)
* **3. Git and Git Bash:** Website https://git-scm.com/downloads
* **4. GitHub Desktop:** Website https://github.com/apps/desktop
* **5. Python 3.X:** Website https://www.python.org/downloads/
* **6. VS Code extensions:** Docker and YAML ; Docker Website (https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker) and YAML Website ( https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml) 

## 3. Choosing the Document Corpus

For this manual, we will use a sample corpus of **Datasets for chicago public health statistics**. 
A directory with the files is shared in the directory `./index_ingest/health_manual` in your home directory and populate it with `.txt` files, where each file represents a user manual. For example:

./index_ingest/health_records/
├── Dataset_Description_Asthma_Hospitalization_PORTAL_ONLY.pdf      
├── Dataset_Description_Prenatal.pdf
└── Dataset_Description_Diabetes_Hospitalization.pdf
├── Dataset_Description_Preterm_Births.pdf
├── Dataset_Description_Fertility.pdf                               
└── Dataset_Description_Selected_indicators_file_PORTAL.pdf     
├── Dataset_description_Infant_Mortality_2005_2009_PORTAL_ONLY.pdf  
├── Dataset_Description_TEEN_Births.pdf
└── Dataset_Description_LBW.pdf                                     
├── Dataset_Description_Tuberculosis.pdf

The content of these files can be sample dataset extracted from https://www.kaggle.com/datasets/chicago/chicago-public-health-statistics

## 4. Setting up Elasticsearch with Docker

We will use a basic Elasticsearch Docker setup for this demonstration.

Ensure Docker, request module, git and Docker Compose(optional) are installed:

```
docker --version
docker-compose --version
requests module (pip install requests)
git --version
```

### 4.1. Pulling the Elasticsearch Image
On Visual studio code or prefered shell, Open your terminal and Clone the Git repository to local machine:

```
git clone https://github.com/ADB-course/204820-CAT2-INFORMATION-RETRIEVAL
```

sample output
```
Cloning into '204820-CAT2-INFORMATION-RETRIEVAL'...
remote: Enumerating objects: 23, done.
remote: Counting objects: 100% (23/23), done.
remote: Compressing objects: 100% (20/20), done.
remote: Total 23 (delta 2), reused 23 (delta 2), pack-reused 0 (from 0)
Receiving objects: 100% (23/23), 983.06 KiB | 1.05 MiB/s, done.
Resolving deltas: 100% (2/2), done.
```
Change directory into the repository working directory
```
cd ./204820-CAT2-INFORMATION-RETRIEVAL/
```

Pull the official Elasticsearch Docker image:

```
docker pull docker.elastic.co/kibana/kibana:8.17.4
```

(Note: We are using version 8.17.4. You can choose a different compatible version if needed.)

### 4.2. Create a docker network to be used for communication between Kibana and Elastic search
Create a network elastic using the below command

```
docker network create elastic
```

### 4.3 Running the Elasticsearch Container

Run the Elasticsearch container with the following command:
Ensure you are in the working directory 
.../204820-CAT2-INFORMATION-RETRIEVAL

```
docker run -d --name elasticsearch    --network elastic  -p 9200:9200 -p 9300:9300 -v ./index_ingest/health_reports:/usr/share/elasticsearch/data/records -e "discovery.type=single-node" -e "xpack.security.enabled=false"   -e "xpack.security.enrollment.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.17.4
```

NOTES: 
-d: Runs the container in detached (background) mode.
--name elasticsearch: Assigns the name "elasticsearch" to the container.
-p 9200:9200: Maps port 9200 on your host machine to port 9200 on the container (for HTTP access).
-p 9300:9300: Maps port 9300 on your host machine to port 9300 on the container (for inter-node communication, though we are in single-node mode).
-v ./index_ingest/health_records:/usr/share/elasticsearch/data/records: Mounts the ./index_ingest/health_records directory on your host machine to /usr/share/elasticsearch/data/records inside the container. This allows the container to access your document corpus. (Note: This mount point is for accessing the files from within the container if needed for custom ingestion scripts. For the basic setup, we will use the Elasticsearch API to ingest the data.)
-e "discovery.type=single-node": Configures Elasticsearch to run in single-node mode, which is suitable for development and demonstration purposes.
-e "xpack.security.enabled=false"  : This explicitly turns off Elasticsearch's security measures, such as requiring usernames and passwords for access.
-e "xpack.security.enrollment.enabled=false" : This prevents the Elasticsearch node from automatically trying to join a secure cluster.
docker.elastic.co/elasticsearch/elasticsearch:8.17.4: Specifies the Docker image to use.
--network : ataches container to network created earlier

**Note: ** Disabling Security features as used in the demonstration are only often used for simplicity in development or testing, but disabling security in production environments is highly discouraged due to significant security risks.

NOTE: DOCKER COMPOSE FILE HAS BEEN PROVIDED: TO USE THIS INSTEAD REFER TO GUIDE ON
https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#docker-compose-file 

###4.4. Verifying Elasticsearch is Running

```
docker ps
```

Sample Output

```
$ docker ps
CONTAINER ID   IMAGE                                                  COMMAND                  CREATED      STATUS      PORTS                                            NAMES
8de454891f4f   docker.elastic.co/elasticsearch/elasticsearch:8.17.4   "/bin/tini -- /usr/l…"   2 days ago   Up 2 days   0.0.0.0:9200->9200/tcp, 0.0.0.0:9300->9300/tcp   elasticsearch
```

You can verify that Elasticsearch is running by opening your web browser and navigating to http://localhost:9200. You should see a JSON response containing information about your Elasticsearch node.

### 4.5 Install Kibana

Pull the kibana docker container and run the container. For cersion compatibility, it is recommended to use the same Version as used by Elastic search

```
docker pull docker.elastic.co/kibana/kibana:8.17.4
docker run -d   --name kibana   --network elastic   -p 5601:5601   -e "ELASTICSEARCH_HOSTS=http://elasticsearch:9200"   -e "XPACK_SECURITY_ENABLED=false"   docker.elastic.co/kibana/kibana:8.17.4
```

Verify the Kibana is running as well

```
docker ps

```
Sample Output

```
$ docker ps
CONTAINER ID   IMAGE                                                  COMMAND                  CREATED      STATUS      PORTS                                            NAMES
b902c23ca3a2   docker.elastic.co/kibana/kibana:8.17.4                 "/bin/tini -- /usr/l…"   2 days ago   Up 2 days   0.0.0.0:5601->5601/tcp                           kibana
8de454891f4f   docker.elastic.co/elasticsearch/elasticsearch:8.17.4   "/bin/tini -- /usr/l…"   2 days ago   Up 2 days   0.0.0.0:9200->9200/tcp, 0.0.0.0:9300->9300/tcp   elasticsearch

```

Check status of both Kibana and Elastic Search on your browser or using CURL

Elasticsearch: http://localhost:9200
Kibana: http://localhost:5601

### 5. Indexing the Document Corpus
We will enable the **ingest-attachment plugin*** to give more capability to our elastic search for information retrieval.
This plugin allows you to index **PDFs, Word docs, PPTs, etc**. using the **Tika library (via base64-encoded content)**. It's super useful for document-based information retrieval.
By default, JSON and TXT files can be ingested without further processing.
NOTE : As of Elasticsearch 8.0, the Ingest Attachment Processor is now included in the default Elasticsearch distribution! This means you no longer need to install a separate plugin.
Elasticsearch 8.x handles file attachments through the Ingest Pipeline Processor exclusively. You should not define a field with the type attachment in your index mapping directly.


### 5.1 Now, we need to index the documents in our ~/index_ingest/health_records directory into Elasticsearch. We can achieve this using the Elasticsearch REST API and curl.

### 5.2 Create an Index (without the attachment field in the mapping)

You only need to define mappings for other fields you want to explicitly control, such as filename. The content extracted by the attachment processor will be automatically detected and indexed.

```
curl -XPUT 'localhost:9200/reports_index?pretty' -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "properties": {
      "filename": { "type": "keyword" },
      "data": { "type": "binary" }
    }
  }
}
'
```
This command creates an index with:

mappings: Defines the schema of our documents. We have two fields:
filename: Stores the name of the document (as a keyword for exact matching and sorting).
content: Stores the actual text content of the document (as text for full-text search).
data : We include the data field as binary to hold the Base64 encoded content before the ingest pipeline processes it.

You should get a success response like:

```
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "reports_index"
}
```

### 5.3  Create Ingest Pipeline for attachment


```
curl -XPUT 'localhost:9200/_ingest/pipeline/attachment?pretty' -H 'Content-Type: application/json' -d'
{
  "description": "Extracts content from PDF files",
  "processors": [
    {
      "attachment": {
        "field": "data",
        "target_field": "file_content"
      }
    }
  ]
}
'
```
You should get a success response like:

```
{
  "acknowledged": true
}
```


### 5.4 Ingesting the Documents

We need to read each file in the ./index_ingest/health_records directory and send its content to Elasticsearch for indexing.
You can use a simple script (e.g., in Python or Bash) to automate this process. We will use a python script to ingesr all pdf files at once.

Example using a Manual steps: (Upload a Document (Base64-encoded))

```
curl -X PUT "localhost:9200/reports_index/_doc/1?pipeline=attachment" -H "Content-Type: application/json" -d'
{
  "filename": "diabetes_report.pdf",
  "data": "BASE64_ENCODED_CONTENT_HERE"
}'
```

In this lab, we use the script in the folder index_ingest/upload_pdfs.py

```
 python upload_pdfs.py index_ingest/health_reports/ 
```

Sample Output
```
Indexing Dataset_Description_Asthma_Hospitalization_PORTAL_ONLY.pdf - Status Code: 201
Response: {"_index":"reports_index","_id":"Dataset_Description_Asthma_Hospitalization_PORTAL_ONLY","_version":1,"result":"created","_shards":{"total":2,"successful":1,"failed":0},"_seq_no":0,"_primary_term":1}
Indexing Dataset_Description_Diabetes_Hospitalization.pdf - Status Code: 201
Response: {"_index":"reports_index","_id":"Dataset_Description_Diabetes_Hospitalization","_version":1,"result":"created","_shards":{"total":2,"successful":1,"failed":0},"_seq_no":1,"_primary_term":1}
Indexing Dataset_Description_Fertility.pdf - Status Code: 201
Response: {"_index":"reports_index","_id":"Dataset_Description_Fertility","_version":1,"result":"created","_shards":{"total":2,"successful":1,"failed":0},"_seq_no":2,"_primary_term":1}
Indexing Dataset_description_Infant_Mortality_2005_2009_PORTAL_ONLY.pdf - Status Code: 201
Response: {"_index":"reports_index","_id":"Dataset_description_Infant_Mortality_2005_2009_PORTAL_ONLY","_version":1,"result":"created","_shards":{"total":2,"successful":1,"failed":0},"_seq_no":3,"_primary_term":1}
Indexing Dataset_Description_LBW.pdf - Status Code: 201
Response: {"_index":"reports_index","_id":"Dataset_Description_LBW","_version":1,"result":"created","_shards":{"total":2,"successful":1,"failed":0},"_seq_no":4,"_primary_term":1}
Indexing Dataset_Description_Prenatal.pdf - Status Code: 201
Response: {"_index":"reports_index","_id":"Dataset_Description_Prenatal","_version":1,"result":"created","_shards":{"total":2,"successful":1,"failed":0},"_seq_no":5,"_primary_term":1}
Indexing Dataset_Description_Preterm_Births.pdf - Status Code: 201
Response: {"_index":"reports_index","_id":"Dataset_Description_Preterm_Births","_version":1,"result":"created","_shards":{"total":2,"successful":1,"failed":0},"_seq_no":6,"_primary_term":1}
Indexing Dataset_Description_Selected_indicators_file_PORTAL.pdf - Status Code: 201
Response: {"_index":"reports_index","_id":"Dataset_Description_Selected_indicators_file_PORTAL","_version":1,"result":"created","_shards":{"total":2,"successful":1,"failed":0},"_seq_no":7,"_primary_term":1}
Indexing Dataset_Description_TEEN_Births.pdf - Status Code: 201
Response: {"_index":"reports_index","_id":"Dataset_Description_TEEN_Births","_version":1,"result":"created","_shards":{"total":2,"successful":1,"failed":0},"_seq_no":8,"_primary_term":1}
Indexing Dataset_Description_Tuberculosis.pdf - Status Code: 201
Response: {"_index":"reports_index","_id":"Dataset_Description_Tuberculosis","_version":1,"result":"created","_shards":{"total":2,"successful":1,"failed":0},"_seq_no":9,"_primary_term":1}
Finished processing PDF files.
```

This script iterates through each .pdf file in the ./index_ingest/health_records directory, reads its content, and sends a POST request to the Elasticsearch index API to add a new document with the filename and content.

### 6. Performing Queries
Now that the documents are indexed, we can perform various types of queries using the Elasticsearch REST API.

First we can start with checking the Mapping: You can verify the mapping of your index to see how the extracted content is being stored:

```
curl -XGET 'localhost:9200/reports_index/_mapping?pretty'

```

This will show you the structure of your index and the fields that Elasticsearch has created.

Sample output for our case

```
$ curl -XGET 'localhost:9200/reports_index/_mapping?pretty'
{
  "reports_index" : {
    "mappings" : {
      "properties" : {
        "data" : {
          "type" : "binary"
        },
        "file_content" : {
          "properties" : {
            "author" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "content" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "content_length" : {
              "type" : "long"
            },
            "content_type" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "creator_tool" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "date" : {
              "type" : "date"
            },
            "format" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "language" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            },
            "metadata_date" : {
              "type" : "date"
            },
            "modified" : {
              "type" : "date"
            },
            "title" : {
              "type" : "text",
              "fields" : {
                "keyword" : {
                  "type" : "keyword",
                  "ignore_above" : 256
                }
              }
            }
          }
        },
        "filename" : {
          "type" : "keyword"
        }
      }
    }
  }
}
```
Specifically, you can see that file_content is an object containing various sub-fields, including:

* **content:* This is where the main text content of the PDF has been extracted.
* **author:* If the PDF has author metadata, it will be here.
* **title:* The title of the PDF, if available.
* **date:* The creation date of the PDF.
* **content_type:* The MIME type of the attachment (e.g., application/pdf).
* **content_length:* The size of the attachment.

And potentially other metadata fields.
Therefore, to search for the word "fertility", you should indeed target the file_content.content field in your query, as we discussed previously.

```
curl -X POST "localhost:9200/reports_index/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "file_content.content": "fertility"
    }
  }
}'
```

If this query still returns no results, it means that the word "fertility" was either not present in the content of the PDF you expected it to be in, or there might be some subtle differences in the text (e.g., case sensitivity, stemming) that are preventing a direct match.

### **Further Troubleshooting if the Corrected Query Still Fails:**

* **Verify the PDF Content:** Open the PDF file "Dataset_Description_Fertility.pdf" and double-check if the word "fertility" actually exists in its text content.
* **Case Sensitivity:** Elasticsearch's match query is case-insensitive by default. However, if you have specific case-sensitive requirements, you might need to adjust your query.
* **Search All Fields:** If you're unsure where the content might be, you can try a simple search across all fields:

```
curl -X POST "localhost:9200/reports_index/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "query_string": {
      "query": "fertility"
    }
  }
}
'
```

This is less efficient but can help you locate the term.

Sample output
```
//truncated
          "file_content" : {
            "date" : "2013-05-29T20:14:19Z",
            "content_type" : "application/pdf",
            "author" : "12467",
            "format" : "application/pdf; version=1.4",
            "modified" : "2013-05-29T20:16:13Z",
            "language" : "en",
            "metadata_date" : "2013-05-29T20:16:13Z",
            "title" : "Microsoft Word - Dataset_Description_Selected_indicators_file_PORTAL.doc",
            "creator_tool" : "PScript5.dll Version 5.2.2",
           -----//truncated
            "content_length" : 9475
          },
          "filename" : "Dataset_Description_Selected_indicators_file_PORTAL.pdf"
        }
      }
    ]
  }
}
```

### 6.1. Basic Keyword Search
To search for documents containing a specific keyword (e.g., "fertility"):

```
curl -XPOST 'localhost:9200/reports_index/_search?pretty' -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "file_content.content": "fertility"
    }
  }
}
'
```
### 6.2. Phrase Search
To search for documents containing a specific phrase (e.g., "remote desktop connection"):

```
curl -XPOST 'localhost:9200/reports_index/_search?pretty' -H 'Content-Type: application/json' -d'
{
  "query": {
    "match_phrase": {
      "file_content.content": "premature death among individuals"
    }
  }
}
'
```

### 6.3. Boolean Queries
To combine multiple search conditions using must, should, and must_not (e.g., find documents containing "troubleshooting" but not "network"):

```
curl -XPOST 'localhost:9200/reports_index/_search?pretty' -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": [
        { "match": { "file_content.content": "teens" } }
      ],
      "must_not": [
        { "match": { "file_content.content": "preterm" } }
      ]
    }
  }
}
'
```

Sample output 
```
//truncated
          "file_content" : {
            "date" : "2012-10-05T17:08:14Z",
            "content_type" : "application/pdf",
            "author" : "LD630-XPPRO",
            "format" : "application/pdf; version=1.5",
            "modified" : "2012-10-05T17:08:14Z",
            "language" : "en",
            "creator_tool" : "Microsoft® Word 2010",
            "content" : "1 \n\n \n\nOn October 5, 2012 a revised version of this dataset was posted to the Open Data Portal. See Version \n\nHistory on page 2 of this document for details.
            ----//truncated
            "content_length" : 6901
          },
          "filename" : "Dataset_Description_TEEN_Births.pdf"
        }
      }
    ]
  }
}
```

### 6.4. Wildcard Queries
To search for terms with wildcard characters (e.g., find files with titles conatining term "pre"):

```
$ curl -XPOST 'localhost:9200/reports_index/_search?pretty' -H 'Content-Type: application/json' -d'
{
  "query": {
    "wildcard": {
      "file_content.title": "*pre*"
    }
  }
}
'
```
Sample output for files with 2 hits:

```

$ curl -XPOST 'localhost:9200/reports_index/_search?pretty' -H 'Content-Type: application/json' -d'
{
  "query": {
    "wildcard": {
      "file_content.title": "*pre*"
    }
  }
}
'
{
  "took" : 4,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "reports_index",
        "_id" : "Dataset_Description_Prenatal",
        "_score" : 1.0,
        "_ignored" : [
          "file_content.content.keyword"
        ],
        "_source" : {
          "data" : " ---//trincated
          "file_content" : {
            "date" : "2012-01-09T04:02:53Z",
            "content_type" : "application/pdf",
            "author" : "12467",
            "format" : "application/pdf; version=1.4",
            "modified" : "2012-01-09T04:02:53Z",
            "language" : "en",
            "title" : "Microsoft Word - Dataset_Description_Prenatal.doc",
            "creator_tool" : "PScript5.dll Version 5.2.2",
            "content" : ---//truncated
          },
          "filename" : "Dataset_Description_Prenatal.pdf"
        }
      },
      {
        "_index" : "reports_index",
        "_id" : "Dataset_Description_Preterm_Births",
        "_score" : 1.0,
        "_ignored" : [
          "file_content.content.keyword"
        ],
        "_source" : {
          "data" : //truncated",
          "file_content" : {
            "date" : "2012-01-09T04:03:54Z",
            "content_type" : "application/pdf",
            "author" : "12467",
            "format" : "application/pdf; version=1.4",
            "modified" : "2012-01-09T04:03:54Z",
            "language" : "en",
            "title" : "Microsoft Word - Dataset_Description_Preterm_Births.doc",
            "creator_tool" : "PScript5.dll Version 5.2.2",
            "content" : "1 \n\n \n\nTitle: Preterm births in Chicago, by year, 1999 – 2009 \n\nBrief Description: ---//truncated \n\nRelated Applications: N/A \n\n ",
            "content_length" : 5382
          },
          "filename" : "Dataset_Description_Preterm_Births.pdf"
        }
      }
    ]
  }
}

```
### 6.5. Fuzzy Queries
To find terms that are similar to the search term (allowing for typos): e.g prterm --> preterm

```
curl -XPOST 'localhost:9200/reports_index/_search?pretty' -H 'Content-Type: application/json' -d'
{
  "query": {
    "fuzzy": {
      "file_content.content": {
        "value": "prterm",
        "fuzziness": 1
      }
    }
  }
}
'
```

This returns the file:  filename" : "Dataset_Description_Selected_indicators_file_PORTAL.pdf"  as expected


### 7. Kibana provides a more user friendly way to perform searches as compared to the Elastic search API
By using Kibana's Discover interface and the methods described above, you can perform the same types of searches you were doing with curl in a more visual and interactive way.
Remember to select the correct index pattern and target the appropriate fields in your queries.

### 7.1 First create a data view for the reports_index

What is a Data View?

A Data View tells Kibana which Elasticsearch indices you want to explore. It defines a set of one or more index names (or patterns) and configures how Kibana should interpret the fields in those indices, especially the timestamp field if you have time-based data.

Steps to Create a Data View:

a. Open Kibana in your web browser. The URL is typically http://localhost:5601 if you are running Kibana locally.

b. Navigate to *Stack Management*: In the left-hand navigation menu, look for *"Stack Management"* (it might be represented by a gear icon or labeled as such). Click on it.

c. Go to *Data Views*: Within *Stack Management*, under the *"Kibana"* section, you will find *"Data Views"*. Click on *"Data Views"*.

Click *"Create data view"*: On the *Data Views page*, you will see a button labeled *"Create data view"*. Click on this button.

d. Define the Index Pattern:

In the *"Index pattern name"* field, enter the name or pattern that matches your Elasticsearch index(es).
For a specific index: If you want to create a Data View for your **reports_index**, simply type reports_index.
For multiple indices with a pattern: You can use wildcards (*) to match multiple indices. For example, logstash-* would match all indices starting with "logstash-". If you wanted to include all indices, you could use *.

In our case, to work with the reports_index you've been using, you would enter: **reports_index**
As you type, Kibana will show you a list of matching indices in Elasticsearch. Verify that your intended index (reports_index) is listed.
Configure the Timestamp Field (Optional but Recommended for Time-Based Data): We will not use this for now.
If your index contains a field that represents a timestamp, Kibana will ask you to configure it as the "Timestamp field". This is crucial for time-based visualizations and analysis.
In your current scenario of indexing PDF reports, you might not have an explicit timestamp field within the extracted content or the metadata you've explicitly mapped. However, Elasticsearch automatically adds @timestamp when a document is indexed. You can try selecting @timestamp from the dropdown menu.
If you have a specific date field within your file_content (like file_content.date or file_content.modified), you can select that field if you want to analyze your reports based on their extracted dates.
If your data is not inherently time-based, you can choose *"I don't want to use a Time Filter".*

e. Click "Create data view": Once you have entered the index pattern and (optionally) configured the timestamp field, click the "Create data view" button.

Data View Created: You will be redirected back to the Data Views list, and your newly created Data View (reports_index) should now be listed.

f. Using Your Data View:

Once your Data View is created, you can use it in various Kibana applications:

*Discover:* When you go to "Discover", you can select your reports_index Data View from the dropdown menu to explore and search your indexed PDF data.
*Visualize:* When creating visualizations, you will choose your reports_index Data View as the data source.
*Dashboard:* You can build dashboards using visualizations based on your reports_index Data View.
*Canvas:* For creating pixel-perfect presentations.

By following these steps, you can successfully create a Data View in Kibana that points to your **reports_index**, allowing you to visually explore and analyze the content of your indexed PDF files. Remember to select the correct index pattern name.


### 7. 2 We can then perform Information retrieval from Kibana
Accessing Kibana's Discover Interface

The primary tool for searching and exploring your data in Kibana is the Discover interface. You can usually find it in the main navigation menu on the left-hand side.

### 7.2.1 Basic Keyword Search ("fertility")

Open Discover: Click on the *"Discover"* icon in the Kibana navigation.

Select Index Pattern: If you haven't already, you'll be prompted to select an index pattern. Choose reports_index. If it's not listed, you might need to create it in Kibana's Index Management (gear icon in the navigation). When creating the index pattern, simply type reports_index* to match your index.

Search Bar: You'll see a search bar at the top. To perform a basic keyword search, simply type your keyword directly into the search bar and press Enter or click the magnifying glass icon.

* fertility*

Kibana will search across all indexed fields for this term.

### 7.2.2 Targeting a Specific Field: To specifically search within the file_content.content field, use the following syntax in the search bar:### 

Paste on search tab:  file_content.content: "death"

Press Enter or click the magnifying glass.

### 7.2.3 Phrase Search ("premature death among individuals")

Paste on search tab: file_content.content: "premature death among individuals"

Press Enter or click the magnifying glass. Kibana will look for this exact sequence of words.

### 7.2.4 Boolean Queries (containing "teens" but not "preterm")

Search Bar: You can construct boolean queries using the AND, OR, and NOT operators (they must be in uppercase).

To find documents containing "teens" and NOT containing "preterm" in file_content.content:

Paste on search tab:  file_content.content: "teens" AND NOT file_content.content: "preterm"

Press Enter or click the magnifying glass.


Paste on search tab:  file_content.content: teens or file_content.content: preterm

### 7.2.4 Wildcard Queries (titles containing "pre")

Open Discover and Select Index Pattern.

Search Bar: To perform a wildcard search on the file_content.title field for titles containing "pre", use the * wildcard character:

file_content.title : *pre*

Click "Run".

### 8. Conclusion
This manual provides a comprehensive guide to setting up a basic Information Retrieval system using Docker and Elasticsearch. By following these steps and exploring the advanced functionalities, you can build a powerful search solution for your document corpus. Remember to practice your live demonstration to ensure a smooth and informative presentation.

Further Practise:
Please refer to elastic search documentation for more functionalities.
NB: This Lab focused on using pdf files. The GIT repository also contains a file *diabeste.json* file and *index_documents.py* script that can be used to index the document and perform searches for JSON format data/nvsr/nvsr48/nvs48_03


### References:

1. https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html
2. https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html
3. https://www.elastic.co/guide/en/elasticsearch/reference/current/documents-indices.html
4. https://www.elastic.co/guide/en/elasticsearch/reference/current/es-ingestion-overview.html
5. https://www.elastic.co/guide/en/elasticsearch/reference/current/attachment.html
6. https://www.kaggle.com/datasets/chicago/chicago-public-health-statistics?resource=download&select=Dataset_description_Infant_Mortality_2005_2009_PORTAL_ONLY.pdf
