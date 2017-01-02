# What is all this?

Recently, Watson released a product called 'Discovery'.  This repo is a working example
of an application using Discovery, Bluemix, Cloudant, and OpenWhisk.  

# Our application

You have been tasked to build a system that lets a non-technical user visit
a simple application to search these and see the current keywords, companies,
and other entities mentioned in the [SEC Investor Alerts and Bulletins](https://www.sec.gov/investor/alerts).

In order to accomplish this, you'll have to download the
[RSS feed from the SEC](https://www.sec.gov/rss/investor/alerts) and get the documents
they've published.   After you get the documents, you'll need to load these
into a full text search engine of some kind and apply some text categorization and
entity extraction.  

# Enter the Discovery Service

The Discovery Service does all of this and more.  This lets you focus on your problem
domain and integration without needing to become an expert in search and text
processing.

You can see the application running here:  LINKME

# Step 0:  Setup your bluemix account

None of this will work without a Bluemix account.  
You should also install the [OpenWhisk CLI](https://console.ng.bluemix.net/openwhisk/cli)
The examples I'm showing here
will use the `cf` command line tool and the `wsk` command line tool for OpenWhisk.

The programing examples are in Python.

# Step 1: Configure an instance of the Discovery Service
## Create Environment
## Create Collection
## Create configuration, with enrichments
## Set configuration as the default for the Collection.  
## Record the GUIDs of all that stuff and the credentials.

# An Overview of OpenWhisk
# Step 2: Your First Action: Get the RSS feed.
# Step 3: Second Action:  Record the metadata about the links
# Step 4: Fetch each article and ingest it
# Step 5: Profit!
