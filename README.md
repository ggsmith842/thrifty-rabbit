# thrifty-rabbit

[![Pylint](https://github.com/ggsmith842/thrifty-rabbit/actions/workflows/pylint.yml/badge.svg)](https://github.com/ggsmith842/thrifty-rabbit/actions/workflows/pylint.yml)

![Logo](https://github.com/ggsmith842/thrifty-rabbit/blob/main/thirfyRabbit.jpg?raw=true)

# Modern Portfolio Methods in Python

This repository provides a set of Python modules that implement modern portfolio methods. The modules can be used to collect price data, use goal-based advising techniques, analyze a portfolio for diversification, and visualize the efficient frontier of a portfolio.

## Installation

To install the modules, simply clone the repository and run the following command:

*(coming in release 1.0)*
pip install -e . 

## Usage
The modules in this repository can be used as follows:

To build a portfolio of assets using the ```Portfolio``` class. The ```Portfolio``` class can:
* get historical closing price data for assets 
* analyze a portfolio for diversification, using the ```correlation_report()``` class method.
* visualize the efficient frontier of a portfolio using the ```show_efficient_frontier()``` class method.
  
To use goal-based advising techniques, using the  goals and riskevaluation modules.

## Examples
The repository includes a number of examples in Jupyter notebooks that demonstrate how to use the modules. The examples can be found in the examples directory.

## Documentation
The documentation for the modules can be found in the docs directory. The documentation includes detailed descriptions of the functions and classes in the modules.

## Contributing
Contributions to this repository are welcome. To contribute, simply fork the repository and submit a pull request.

## License
This repository is licensed under the MIT [License](https://github.com/ggsmith842/thrifty-rabbit/blob/main/LICENSE).
## Credits

This package uses the following packages:

* yfinance: https://pypi.org/project/yfinance/
* pypfopt: https://pypfopt.readthedocs.io/en/stable/

## References
* [Robo-Advisor with Python: A hands-on guide to building and operating your own Robo-advisor](https://github.com/aki-ranin/robo-advisor-with-python) 
* [yfinance documentation](https://pypi.org/project/yfinance/)
* [pypfopt documentation](https://pypfopt.readthedocs.io/en/stable/)



