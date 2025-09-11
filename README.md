<!--

SPDX-FileContributor: [Author Name(s)] <[Optional: Email Address(es)]>

SPDX-License-Identifier: CC0-1.0
-->

# Cryptographic Algorithms Open Dataset

This data set, which includes a list of cryptography algorithms with an open source implementation, was originally the output of SCANOSS mining efforts across its entire data base, which includes all relevant open source software published. Today, the intention is to turn this repository into a collaborative project to enrich and maintain this data set, not just for export control, the original target activity, but for other purposes as well, like quantum safe or compliance with a variety of regulations.


### SPDX Crypto algorithms definitions

The [Taxonomy](taxonomy) Is a link to SPDX cryptographic algorithms definitions. 

You can find the index of the cryptography algorithms and their corresponding algorithId in the [algorithms](/algorithms) folder. If you want to contribute definining a new algorithm you should do [there](https://github.com/spdx/crypto-algorithms) and not in this project.
Also, you can take a look on the current supported [algorithms](algorithms.md)

#### Detection

The [detection](detection) folder contains a set of YAML files which define all the available cryptography algorithms. Every file contains the keywords used for detection of that algorithm inside source files.


### Utilities

The [utilities](utilities) folder contains some helper utility scripts written in Python to illustrate how these definitions can be leveraged.

The primary example is [crypto_detect.py](utilities/crypto_detect.py).
More details on how to use it can be found [here](utilities/README.md)


## Contributing New Cryptographic Data

If you find a missing/invalid keyword, please do the following:
- Fork the [repo](https://github.com/scanoss/crypto_algorithms_open_dataset)
- Update or Add the affected YAML files inside the [definitions](definitions_crypto_algorithms) folder
- Create a Pull Request with the details of the update

If you want to define a missing algorithm:
- Contribute to [SPDX](https://github.com/spdx/crypto-algorithms.git) crypto definitions first, we will add an initial set of keywords once your PR has been merged.
- Enrich the new algorithm adding keywords

The team will review these requests and accept them into repo for everyone to benefit from.

## License

This project is released under the Creative Commons Public Domain CC0-1.0 license. 
Full details can be found [here](LICENSE).
