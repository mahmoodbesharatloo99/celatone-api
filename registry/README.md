# Alles Cosmos Registry

## Entities

Entities list in [data/entities.json](data/entities.json) is the main list of all of the labelled actors (projects, protocols, individuals) that the registry is aware of. Each entity has a corresponding `slug` that is used as the reference key for all of its related data points and information (accounts, codes, contracts, etc).

```ts
type Social = {
    // The name of the social media
    name: string,
    // The corresponding link to the entity's social media page
    url: string,
}

type Entity = {
    // The slug identifier for the entity
    slug: string,
    // The human-readable name of the entity
    name: string,
    // The entity's main website
    website: string,
    // The entity's GitHub organization/account slug
    github: string,
    // The filename of the entity's logo located in assets/entities
    logo: string,
    // The list of the entity's supported social media info
    socials: Social[3]
}
```

For each network, there are then 4 JSON files that outlines the on-chain data relating to one or more of the entities, tied together by the entity's `slug`

- codes
- contracts
- accounts
- projects

### Codes

Contains all of the labelled contract code IDs on the network belonging to the known entities.

```ts
type Code = {
    // The slug identifier for the owner entity
    slug: string
    // The name describing the code
    name: string
    // The ID of the code on-chain
    id: string
    // A short description of the code
    description: string | undefined
}
```

### Contracts

Contains all of the labelled contract addresses on the network belonging to the known entities.

```ts
type Contract = {
    // The slug identifier for the contract's owner entity
    slug: string
    // The short description of the smart contract
    name: string
    // The address of the smart contract
    address: string
    // A short description of the contract
    description: string | undefined
}
```

### Assets

Contains information related to on-chain assets on each network

```ts
type Asset = {
    // The slug identifier for the asset's entity
    slug: string
    // Name of the asset
    name: string
    // Asset symbol
    symbol: string
    // URL link to image file. 
    logo: string
    // Type of assets. Either 'native' or 'cw20'
    type: string
    // Denom for 'native' or contract address for 'cw20'
    id: string
    // Asset precision
    precision: string
}
```

### Accounts

Contains all of the labelled accounts on the network belonging to the known entities.

```ts
type Account = {
    // The slug identifier for the account's owner entity
    slug: string
    // The short description of the account
    name: string
    // The address of the account
    address: string
    // A short description of the account
    description: string | undefined
}
```

### Projects

Contains aggregated information on all of the contracts, codes, and accounts belonging to the known entites on the network.

```ts
type Project = {
    // The slug identifier for the owner project
    slug: string,
    // The list of contracts belonging to the project
    contracts: Contract[]
    // The list of codes belonging to the project
    codes : Code[]
    // The list of accounts belonging to the project
    accounts: Account[]
}
```
