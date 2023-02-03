# Celatone API

This repository contains two main parts:

- `./registry`: a registry containing information related to in the Cosmos ecosystem, currently mainly used by [Celatone](https://celat.one) and other Alles Labs products
- `./server`: An implementation of a simple Flask server to expose the registry data as a REST API Endpoint

## Registry

### Overarching Data

#### Chains

Chains are the network information used by Celatone and other products.

```ts
enum NetworkType {
    Testnet = "testnet",
    Mainnet = "mainnet"
}

type FaucetProvider = {
    // name of faucet provider
    provider: string
    // faucet provider logo
    logo: string
    // link to faucet
    url: string
}

type NodeProvider = {
    // name of the node provider
    provider: string
    // node provider logo
    logo: string
    // node URL
    url: string
    // whether the node is an archive node
    archive: bool
}

type Network = {
    // type of network
    type: NetworkType,
    // celatone link
    celatone: string
    // chain ID
    chainId: string
    // prettified chain name
    chainName: string
    // URL of public LCD
    publicLCD?: string
    // link to public LCD Swagger
    lcdSwagger?: string
    // URL of public RPC
    publicRPC?: string
    // link to public RPC Swagger
    rpcSwagger?: string
    // URL of public GRPC Gateway
    publicGRPC?: string
    // list of third-party LCDs
    lcds: Provider[]
    // list of third-party RPCs
    rpcs: Provider[]
    // list of faucets
    faucets: Faucet[]
}
```

#### Entities

Entities are the list of known individuals, teams, companies, protocols, and other actors. These are used to link together the different information types in the [netework-specific](#network-specific-information) section below.

```ts
type Social = {
    name: string
    url: string
}

type Entity = {
    // the slug used to identify the entity
    slug: string
    // the prettified entity name
    name: string
    // brief description of the entity
    description: string
    // url link to the entity's website
    website?: string
    // url link to the entity's github repository/organization
    github: string
    // the filename of the entity's logo in /registry/assets/entities
    logo: string
    // list of social media channel belonging to the entity
    // currently supports twiter, discord, and telegram
    socials: Social[]
}
```

### Network Specific Information

### Accounts

```ts
type Account = {
    // the slug of the entity who the account belongs to
    slug: string
    // the name/label of the account
    name: string
    // the address of the account
    address: string
    // short description of the account
    description: string
}
```

### Assets

```ts
enum AssetType {
    Native = "native"
    Cw20 = "cw20"
}

type Asset = {
    // list of entity slugs that the asset is associated with
    slugs: string[]
    // the id of the assets. denom for native tokens and token contract address for cw20
    id: string
    // human readable name for the asset
    name: string
    // short description of the asset
    description: string
    // url link to the asset's logo
    logo: string
    // the type of the asset. either "native" or "cw20"
    type: AssetType
    precision: number
}
```

### Codes

```ts
type Code = {
    // entity slug string that the code belongs to
    slug: string
    // name/label for the code
    name: string
    // on-chain code ID
    id: number
    // short description of the code
    description: string
}
```

### Contracts

```ts
type Contract = {
    // entity slug string that the contract belong to
    slug: string
    // name/label for the contract
    name: string
    // address of the contract deployed on chain
    addresss: string
    // short description of the code
    description: string
}
```

## Server

The server then is a simple Python [Flask](https://flask.palletsprojects.com) server that is used to served the data in the registry over REST API. The registry data is appended by data from other external sources including:

- general data from each chain's publci LCD
- code and contract data from our indexer
- pricing data from [CoinGecko](https://coingecko.com)
- Terra CW20 data from Terra's Hive
- code verification information from [ScanWork](https://www.scanworks.org/)'s [cw-contracts-registry](https://github.com/teamscanworks/cw-contracts-registry) repository.

## Contributing Data

For those interested in adding chain data to the registry, please see [CONTRIBUTING.md](./CONTRIBUTING.md).
