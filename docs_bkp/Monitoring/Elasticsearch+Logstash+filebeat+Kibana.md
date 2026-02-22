# ![ELK Stack Architecture](https://www.softwaretestinghelp.com/wp-content/qa/uploads/2021/07/1ELK-Stack-Architecture.png)

# <mark>Data Storing - ELASTICSEARCH </mark>

## Setting up Elasticsearch and Kibana on macOS and Linux

```
#Setting up Elasticsearch and Kibana on macOS and Linux
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.7.0-linux-x86_64.tar.gz

wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.7.0-linux-x86_64.tar.gz.sha512

shasum -a 512 -c elasticsearch-8.7.0-linux-x86_64.tar.gz.sha512 

tar -xzf elasticsearch-8.7.0-linux-x86_64.tar.gz

cd elasticsearch-8.7.0/


- Reset default password for super user "elastic"
./bin/elasticsearch-reset-passowrd -u elastic

- Generate a new Kibana Enrollment token
./bin/elasticsearch-create-enrollment-token --scope kibana

- Generate an enrollment token for Elasticsearch nodes with
./bin/elasticsearch-create-enrollment-token -s node

- start the elasticsearch
./bin/elasticsearch

- check the elasticsearch is running
curl --cacert $ES_HOME/config/certs/http_ca.crt -u elastic https://localhost:9200

- Elasticsearch now uses a self signed certificate, which HTTP clients (including cURL) will reject by default.
- If your endpoint was previously http://localhost:9200, it is now https://localhost:9200. That's all. 🙂 

#Setting up kibana
wget https://artifacts.elastic.co/downloads/kibana/kibana-8.7.0-linux-x86_64.tar.gz

tar -xzf kibana-8.7.0-linux-x86_64.tar.gz

cd kibana-8.7.0

- start the kibana
./bin/kibana

- access the kibana by below URL in browser
http://localhost:5601/

- paste the Enrollment token generated from elasticsearch which generated on elasticsearch running terminal
- click on "Configure Elastic"

- Login in kibana with Credential 
user : elastic
paswd: hfdjkfhskfdjkhjf8605mfdklgfl (It is generated on elasticsearch running terminal)

#Elastic Search Summary
- Nodes are stored the data that we add to Elasticsearch
- A cluster is collection of nodes
- Data is stored as documents , which are JSON objects
- Document are grouped together with indices
- Cloud deployment consist of multiple nodes by default
- Elasticsearch name can be configured in elasticsearch.yml file
$ES_HOME > config > elasticsearch.yml

#Inspecting the Cluster
- Elasticsearch works with Rest API
Kibana Home-->Navigation Menu-->Management-->Dev Tools-->Console will be Open
```

```-
GET      - Rest API 
_cluster - API
health   - command
```

Get the central node information

```Get
GET /_cat/nodes?v
```

Get the indices details

```
GET /_cat/indices?v
```

Get the details all available system indices

```
GET /_cat/indices?v&expand_wildcards=all
```

Send Request with Curl Command

```
curl --cacert $ES_HOME/config/certs/http_ca.crt -u elastic:password -X GET https://localhost:9200

curl --cacert $ES_HOME/config/certs/http_ca.crt -u elastic:password -X GET -H "Content-Type:application/json"  https://localhost:9200/products/_search -d '{ "query": { "match_all": {} } }'
```

### Sharding

- It is a way to devide indices into smaller pieces.

- Each piece referred to as a shard.

- Sharding is done at the index level.

- The main purpose is to horizontally scale the data volume.

- pri : It is referred as Primary Shards in GET /_cat/indices?v output coloumn

- An index containing a single shard by default.

- Indices in ES < 7.0.0 were created with five shards. This often led to over-sharding

- We can increase the number of shards with split API

- We can reduce the number of shards with shrink API

- the default number of replicas per shard : 1

- Factor includess for Optimal Shards
  
  1. Number of Nodes and their capacity
  
  2. Number of Indices and their Sizes
  
  3. Number of Queries

### adding more node to the cluster

```
vi Elasticsearch.yml
node-name: third-node
../bin/elasticsearch --enrollment-token fljurhsdgkljietjgotrhrntinbtir
```

Delete Index and Put

```
Delete /pages
PUT /produts
{
    "settings" {
        "number_of_shards": 2,
        "number_of+replica": 1
    }
}
```

Create Index

```
POST /products/_doc
{
    "name": "coffeeMaker",
    "price": 400,
    "in_stock": 10
}
```

create index by id=100

```
PUT /products/_doc/100
{
    "name": "Toaster",
    "price": 49,
    "in_stock": 4
}
```

Retrieve index by id

```
GET /products/_doc/100
```

importing data with CURL url

```
- Download Curl
https://curl.se/download.html
- upload bulkdata
curl -H "content-Type: application/x-ndjson" -XPOST http://localhost:9200/products/_bulk --data-binary "@product-bulk.json"
```

Analyze text

```
- It will analyze the text and convert the text charcter into tokens.
POST /_analyze
{
    "text": "2 guys walk"
    "analyzer": "standard"
}
output:
{
    "tokens": [
    {
        "token": "2",
        "start_offset": 0,
        "end_offset": 1,
        "type": <NUM>,
        "position": 0
    },
    {
        "token": "guys",
        "start_offset": 2,
        "end_offset": 6,
        "type": <APHANUM>,
        "position": 1
    },
    {
        "token": walk,
        "start_offset": 7,
        "end_offset": 11,
        "type": <ALPHANUM>,
        "position": 2
    },
}
```

Searching for data for exact matcing on structure data

```
- by terms
GET /products/_search
{
    "query": {
        "term": {
            "tags.keywords": "vegetables"
        }
    }
}

- By boolean 
GET /products/_search
{
    "query": {
        "term": {
            "is_active": true
        }
    }
}

- By Number
GET /products/_search
{
    "query": {
        "term": {
            "in_Stocks": 2
        }
    }
}

- By date timestamp
GET /products/_search
{
    "query": {
        "term": {
            "created": "2007/10/14 12:34:56"
        }
    }
}

- By documents IDs
GET /products/_search
{
    "query": {
        "ids": {
            "values": ["100", "200", "300"]
        }
    }
}

- By Range 
gt >    greater than
gte>=   greater than equal to
lt <    Less than 
lts<=   Less than equal to

date stored in ES as UTC format.

GET /products/_search
{
    "query": {
        "range": {
            "created": {
                "time_zone": "+10:00",
                "gte": "2020/01/01 01:00:00",
                "lte": "2020/01/31 00:59:00"
            }
        }
    }
}

- By prefix
GET /products/_search
{
    "query": {
        "prefix": {
            "name.keywords": {
                "value": "past",
                "case_sensitive": true
            }
        }
    }
}


- By Wildcard(?)
GET /products/_search
{
    "query": {
        "wildcard": {
            "tags.keywords": {
                "value": "Bee?",
                "case_sensitive": true
            }
        }
    }
}

- By Regular Expression
GET /products/_search
{
    "query": {
        "wildcard": {
            "tags.keywords": {
                "value": "Bee*",
                "case_sensitive": true
            }
        }
    }
}
{
    "query": {
        "wildcard": {
            "tags.keywords": {
                "value": "Bee(f|r)+",
                "case_sensitive": true
            }
        }
    }
}
{
    "query": {
        "wildcard": {
            "tags.keywords": {
                "value": "Bee[a-zA-Z]+",
                "case_sensitive": true
            }
        }
    }
}

- By field existance
GET /products/_search
{
    "query": {
        "exist": {
            "field": "tags.keywor





- Full Text Queries used for Unstructured Data
- FTQ are analyzed queries
- FTQ is not used for exact matching
- Match Query is widely used FTQ
GET /products/_search
{
    "query": {
        "match": {
            "name": "pasta"
            }
        }
    }
}
{
    "query": {
        "match": {
            "name": "PASTA CHICKEN",
            "operator": "AND"
            }
        }
    }
}

- Multi Match
GET /products/_search
{
    "query": {
        "multi_match": {
            "query": "vegetables",
            "field": ["name", "tags" ]
            }
        }
    }
}

- phrase match
GET /products/_search
{
    "query": {
        "match_phrase": {
            "nam
- Full Text Queries used for Unstructured Data
- FTQ are analyzed queries
- FTQ is not used for exact matching
- Match Query is widely used FTQ
GET /products/_search
{
    "query": {
        "match": {
            "name": "pasta"
            }
        }
    }
}
{
    "query": {
        "match": {
            "name": "PASTA CHICKEN",
            "operator": "AND"
            }
        }
    }
}

- Multi Match
GET /products/_search
{
    "query": {
        "multi_match": {
            "query": "vegetables",
            "field": ["name", "tags" ]
            }
        }
    }
}

- phrase match
GET /products/_search
{
    "query": {
        "match_phrase": {
            "nam- Full Text Queries used for Unstructured Data
- FTQ are analyzed queries
- FTQ is not used for exact matching
- Match Query is widely used FTQ
GET /products/_search
{
    "query": {
        "match": {
            "name": "pasta"
            }
        }
    }
}
{
    "query": {
        "match": {
            "name": "PASTA CHICKEN",
            "operator": "AND"
            }
        }
    }
}

- Multi Match
GET /products/_search
{
    "query": {
        "multi_match": {
            "query": "vegetables",
            "field": ["name", "tags" ]
            }
        }
    }
}

- phrase match
GET /products/_search
{
    "query": {
        "match_phrase": {
            "name": "Complete Guide to ES"
            }
        }
    }
}e": "Complete Guide to ES"
            }
        }
    }
}e": "Complete Guide to ES"
            }
        }
    }
}ds"
            }
        }
    }
}
{
    "query": {
    "bool": {
        "must_not": [ 
        {
            "exist": {
                "field": "tags.keywords"
                }
            }
        }
      ]
    } 
  }
}
```

```
- Full Text Queries used for Unstructured Data
- FTQ are analyzed queries
- FTQ is not used for exact matching
- Match Query is widely used FTQ
GET /products/_search
{
    "query": {
        "match": {
            "name": "pasta"
            }
        }
    }
}
{
    "query": {
        "match": {
            "name": "PASTA CHICKEN",
            "operator": "AND"
            }
        }
    }
}

- Multi Match
GET /products/_search
{
    "query": {
        "multi_match": {
            "query": "vegetables",
            "field": ["name", "tags" ]
            }
        }
    }
}

- phrase match
GET /products/_search
{
    "query": {
        "match_phrase": {
            "name": "Complete Guide to ES"
            }
        }
    }
}
```

[Boolean query | Elasticsearch Guide [8.9] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html)

Create a new index

```
PUT /department
{
  "mappings": {  
    "properties": {
      "name": {
        "type": "text"
      },
      "employees": {
        "type": "nested"
      }
    }
  }
}
```

Add two test documents

```
PUT /department/_doc/1
{
  "name": "Development",
  "employees": [
    {
      "name": "Eric Green",
      "age": 39,
      "gender": "M",
      "position": "Big Data Specialist"
    },
    {
      "name": "James Taylor",
      "age": 27,
      "gender": "M",
      "position": "Software Developer"
    },
    {
      "name": "Gary Jenkins",
      "age": 21,
      "gender": "M",
      "position": "Intern"
    },
    {
      "name": "Julie Powell",
      "age": 26,
      "gender": "F",
      "position": "Intern"
    },
    {
      "name": "Benjamin Smith",
      "age": 46,
      "gender": "M",
      "position": "Senior Software Engineer"
    }
  ]
}
PUT /department/_doc/2
{
  "name": "HR & Marketing",
  "employees": [
    {
      "name": "Patricia Lewis",
      "age": 42,
      "gender": "F",
      "position": "Senior Marketing Manager"
    },
    {
      "name": "Maria Anderson",
      "age": 56,
      "gender": "F",
      "position": "Head of HR"
    },
    {
      "name": "Margaret Harris",
      "age": 19,
      "gender": "F",
      "position": "Intern"
    },
    {
      "name": "Ryan Nelson",
      "age": 31,
      "gender": "M",
      "position": "Marketing Manager"
    },
    {
      "name": "Kathy Williams",
      "age": 49,
      "gender": "F",
      "position": "Senior Marketing Manager"
    },
    {
      "name": "Jacqueline Hill",
      "age": 28,
      "gender": "F",
      "position": "Junior Marketing Manager"
    },
    {
      "name": "Donald Morris",
      "age": 39,
      "gender": "M",
      "position": "SEO Specialist"
    },
    {
      "name": "Evelyn Henderson",
      "age": 24,
      "gender": "F",
      "position": "Intern"
    },
    {
      "name": "Earl Moore",
      "age": 21,
      "gender": "M",
      "position": "Junior SEO Specialist"
    },
    {
      "name": "Phillip Sanchez",
      "age": 35,
      "gender": "M",
      "position": "SEM Specialist"
    }
  ]
}
```

# <mark>Data Processing - LOGSTASH & FILEBEAT</mark>

- open source events processing engine.
- support many data sources and destination.
- It works on pipeline model with many plugins which collecting, receiving, manipulating and pushing data.
- Process events are sent to stashes. A stash is destination e.g. Elasticsearch or Kibana.
- It not limited to Logs only but handles files like Json, XML, CSV, etc.

### Installing LogStash in MAC/ Linux

```
- Download Java8 https://www.oracle.com/java/technologies/downloads/
- Download LogStash binaries file https://www.elastic.co/downloads/logstash
- Extract the file "tar -zxvf logstash.tar.gz"
- Go to LogStash directory "cd logstash"
- Go to logstash/bin directory "cd bin"
- Start the LogStash " logstash -e "input { stdin { } } output { stdout { } }"
```

### Installing logstash in Windows

```
- Make sure you have Java 8 installed. If not, you can download it here. You can proceed and attempt to start up Logstash and you will find out if Java is installed.
- Go to the download page and download Logstash (you should download the zip file, and make sure you download version 6.x)
- Unzip the zip archive
- Open up the Command Prompt (start menu > search > "cmd")
- Navigate to the extracted archive (e.g. cd C:\path\to\logstash )
- Run the following command: bin\logstash -e "input { stdin { } } output { stdout { } }"
```

### Create Pipeline data for logstash

```
- cd logstash/event-data
apache_access.log

- cd logstash/config
pipeline.conf 
input {
    stdin {
    path => "/logstash/event-data/apache_access.log
    start_position => "beginning"
    }
}
output {
    stdout {
    codec => rubydebug
    }
}

- reload the configuration
bin/logstash -f config/pipeline/pipeline.conf --config.reload.automatic

- Remove flushing data by removing .sincedb file
rm data/plugin/input/file/.sincedb_*
```

### Log Collecting - Filebeat

### Configure and install FILEBEAT for logstash

```
- Download filebeat from URl "https://www.elastic.co/downloads/beats/filebeat"
- open filebeat.yaml
- Comment the Elasticsearch section and uncomment the logstash section
output.logstash:
    hosts: ["localhost:5044"]
- Enable Apache module in filebeat "./filebeat module enable apache"
- cd modules.d/ and open & edit apache2.yaml file
- module: apache2
access:
    enabled: true
    var.path: ["/path/to/system/apache/log/file/apache_access_*.log"]
errors:
    enabled: true
    var.path: ["/path/to/system/apache/log/file/apache_errors_*.log"]

- Configure Logstash pipeline to use filebeat collecting logs
- start filebeat "./filebeat -e"
- specifying the "-e" flag at startup to output error to stderr
- Enable KIbana Dashboards by enable kibana section dont use in production grade environment
- Open and edit filebeat.yml
setup.dashboards.enabled: true
setup.kibana:
    host: "localhost:5601"
- run command to enable dashboards "./filebeat setup --dashboards"
```

delete all old filebeat logs from kibana registry

```
DELETE /filebeat-*
```

Manual input configuration for filebeat open and edit filebeat.yml

```
filebeat.input:
- type: log
  enabled: true
  paths:
    - /file/log/for/system/log/*.log
excludes_files: ['.gz$']
fields:
    event:
        module: apache
        dataset: "apache.access"
fields_under_root: true
multiline.pattern: '^(\s+|\t)|(Caused by:)'
multiline.negate: true
multiline.match: after
```

<mark>overview of mechanism ELK</mark>
file beat  ----------->    Log Stash  ------------->       Elasticsearch  -----------------> Kibana
(Log Collection)     (Event Processing)             (Data Storage)       (Visulization/Dashboards)

# <mark>Data Visulization/Dashboards - KIBANA</mark>

**Activating trial license in local system**
Kibana --> Dock Navigation --> Management --> Stack Management --> stack --> License Management --> Start a 30-day trial --> start my trial

<u>**index patterns have been renamed to data views in recent versions of Kibana.
So instead of "Index patterns", look for "Data views" within the UI and you should be all good! 🙂**</u>

**Creating index pattern**
Kibana --> Dock Navigation --> Management --> Stack Management --> Kibana -->Index Pattern -->[+] Create Index Pattern --> [Index Pattern Name : access-log* | Time Field : @timestamp | Create INdex Pattern ]

**KQL - Kibana Query Language**

KQL used throughout Kibana i.e. number of apps

Can be ised to apply filter on dashboards

Can be used to filter data within visualization

**Changing time_zone in kibana**

Kibana --> Dock Navigation --> Management --> Stack Management --> kibana --> Advanced setting --> Timezone for date formatting --> UTC(Change TZ according ot your requirements

### Enable security feature in kibana

```
- open and edit elasticsearch.yml
xpack.security.enabled: true
- generate password "bin/elasticsearch-setup-passowrd auto" shown in console
- open and edit kibana.yml
elasticsearch.username: "kibana_system"
elasticsearch.passowrd: "fdskhfjfhdklbgklbjkfl"
- login kibana UI with user credentials with elastic
user: elastic
passowrd: "paSswOrDPriNtInElastIcSeArhConsOle"
```

### Drilldown : Panel Feature to more analysis

```
- Drilldown is simple but powerful feature
- create navigation paths between dashboards
preserve context ,being KQL , filter , and time filter
- You will typically interact with dashboards
e.g. explore data or troubleshoot issue
- Without drilldown we would have to transfer context manually
for complex use cases, this would be a hassle
```

### Spaces

```
- It is like Profile or Own UI space for different team like QA, Developer, Engineer , sales etc.
- It is defined feature visiblity and organize saved objects.
- saved objects are dashboards , visualization , index pattern etc.
```

**We'll get back to what it means to organize these objects**
Kibana --> Dock Navigation --> Management --> Stack Management --> kibana --> space --> create new space [ QA, Dev, Test , sales ]

**We can copy object from one space to another**
Kibana --> Dock Navigation --> Management --> Stack Management --> kibana --> saved object --> select object --> Copy to Space --> select destination space

### Creating and Managing users

Kibana --> Dock Navigation --> Management --> Stack Management --> security --> Users --> Create User --> [ username | Password | Confirm Password | Full Name | Email Address | Roles | Create User ]

### Create Roles

- **kibana_admin and superuser built-in roles**
  Kibana --> Dock Navigation --> Management --> Stack Management --> security --> Roles --> create role --> Space Privileges

### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**

##### Thank you for your support!💚
