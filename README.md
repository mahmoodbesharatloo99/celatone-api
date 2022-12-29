# Cosmos Registry API

This repository contains the implementation of an API wrapper around the Alles Labs' [Cosmos Registry](https://github.com/alleslabs/cosmos-registry).

## Routes

### Global

#### Entities

- Entity list: `/entities`
- Entity by slug: `/entity/<ENTITY_SLUG>`

### By Chain and Network

#### Projects

- Project list by chain name/network pair: `/<CHAIN>/<NETWORK>/projects`
- Project by ID: `/<CHAIN>/<NETWORK>/project/PROJECT_ID`

### Contracts

- Contracts list by chain name/network pair: `/<CHAIN>/<NETWORK>/contracts`
- Contract by contract address: `/<CHAIN>/<NETWORK>/contract/CONTRACT_ADDRESS`

### Codes

- Codes list by chain name/network pair: `/<CHAIN>/<NETWORK>/codes`
- Code by code ID: `/<CHAIN>/<NETWORK>/code/CODE_ID`

### Accounts

- Accounts list by chain name/network pair: `/<CHAIN>/<NETWORK>/addresses`
- Account by address: `/<CHAIN>/<NETWORK>/address/ACCOUNT_ADDRESS`

### Assets

- Assets list by chain name/network pair: `/<CHAIN>/<NETWORK>/assets`
- Assets list by entity slug: `/<CHAIN>/<NETWORK>/assets/slug/<ENTITY_SLUG>`
- Assets list by type ('native' vs 'cw20'): `/<CHAIN>/<NETWORK>/assets/type/<ASSET_TYPE>`
- Asset by id: `/<CHAIN>/<NETWORK>/asset/<ASSET_ID>`
