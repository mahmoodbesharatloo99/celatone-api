# Contributing Chain Data

The guide below outlines how to contribute and add/modify data to the registry

## First Steps

1. Fork the repository
2. Add an upstream so that you can update your fork
3. Clone the fork to yoru computer
4. Create a branch and name it appropriately

## Adding Data

### Chain Information

The chain [chain.json](./registry/data/chains.json) is meant to be used for Celatone and other related products. Thus, while we will accept PRs related to chains that Celatone currently does not support, note that the information will not be used nor shown anywhere in that case.

## Chain Specific Information

For adding/modifying chain specific informations (accounts, assets, codes, contracts), make the necessary additions or changes to the files in the respective chain/network folder. When adding information related to entites that is not in the registry, please also an entry to [entities.json](./registry/data/entities.json) in the PR with as much information as possible.

## Submitting the Changes

Once you've made the desired changes, create a PR on the Celatone API reposistory. Wait for your changes to be reviewed. Once the PR has been approved, the modifications will be merged and the API will be updated to match the changes shortly.
