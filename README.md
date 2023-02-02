# Cosmos Registry

This repository contains two main parts:

- `./registry`: a registry containing information related to in the Cosmos ecosystem, currently mainly used by [Celatone](https://celat.one) and other Alles Labs products
- `./server`: An implementation of a simple Flask server to expose the registry data as a REST API Endpoint

Detailed information on these two sections and guide on how to add relevant chain data to the registry can be found on the Celatone [documentation](https://docs.celat.one)

## Registry

## Server

The server then is a simple Python [Flask](https://flask.palletsprojects.com) server that is used to served the data in the registry over REST API. The registry data is appended by data from other external sources including:

- general data from each chain's publci LCD
- code and contract data from our indexer
- pricing data from [CoinGecko](https://coingecko.com)
- Terra CW20 data from Terra's Hive
- code verification information from [ScanWork](https://www.scanworks.org/)'s [cw-contracts-registry](https://github.com/teamscanworks/cw-contracts-registry) repository.
