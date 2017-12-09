## Sanic and Redis backend for www.flowersync.com
---
Server that uses Python Sanic and Redis to generate api responses. This together with the front end code reachable from the website put together a complete software one can use.

The APIs used to be built on Django with a lot of other different routes scraping sources other than Yahoo Finance. But since Yahoo Finance provides the best public data available, I have decided to use it as the only data source for now, and ported to the allegedly blazing fast Sanic framework.
---
Rewriting this same thing in Node to scale better using AWS Lambda/GCP Cloud Function.
