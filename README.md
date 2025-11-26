<div id="top"></div>

<!-- PROJECT SHIELDS -->

<!--
[![PyPI](https://img.shields.io/pypi/v/steam-market-history?style=flat-square)](https://pypi.org/project/steam-market-history/)
[![GitHub pipeline status](https://img.shields.io/github/actions/workflow/status/fabieu/steam-market-history/build.yml?style=flat-square)](https://github.com/fabieu/steam-market-history/actions) 
-->
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/steam-market-history?style=flat-square)](https://pypi.org/project/steam-market-history/)
[![GitHub issues](https://img.shields.io/github/issues-raw/fabieu/steam-market-history?style=flat-square)](https://github.com/fabieu/steam-market-history/issues)
[![GitHub merge requests](https://img.shields.io/github/issues-pr/fabieu/steam-market-history?style=flat-square)](https://github.com/fabieu/steam-market-history/pulls)
[![GitHub](https://img.shields.io/github/license/fabieu/steam-market-history?style=flat-square)](https://github.com/fabieu/steam-market-history/blob/main/LICENSE)

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/fabieu/steam-market-history">
    <img src="https://raw.githubusercontent.com/fabieu/steam-market-history/main/docs/images/logo.svg" alt="Logo" width="120" height="120">
  </a>

<h2 align="center">steam-market-history</h2>

  <p align="center">
    An easy-to-use CLI to export your steam market history to various formats
    <br />
    <a href="https://github.com/fabieu/steam-market-history/issues">Report Bug</a>
    ·
    <a href="https://github.com/fabieu/steam-market-history/issues">Request Feature</a>
  </p>
</div>

<!-- ABOUT THE PROJECT -->

## About The Project

steam-market-history is a command line tool written in Python which allows you to extract your entire Steam Market History with all transaction (sales/purchases) in a CSV or HTML file.

### Key features

- Extract your **entire** Steam Market History with all transactions to a HTML, CSV or JSON file
- Overview of _all_ transactions on a user-friendly webpage with searchable and filterable results

## Demo
<img src="https://raw.githubusercontent.com/fabieu/steam-market-history/main/docs/demo.gif">

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

- Python >= 3.8

### Installation

Install manually using Poetry (recommended):

1. Clone the repo
   ```sh
   git clone https://github.com/fabieu/steam-market-history.git
   ```
2. Install poetry (if not already installed)
   ```sh
   pip install poetry
   ```
3. Install dependencies and start virtual environment
   ```sh
   poetry install && poetry shell
   ```

> [!WARNING]
> PyPI installation (`pip install steam-market-history`) is currently not available due to changes in Steam's authentication mechanism. The package relies on a fork of the steam library that cannot be published to PyPI. Please use the manual installation method above. See [#16](https://github.com/fabieu/steam-market-history/issues/16) for more details.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

Currently, the following commands are supported:

### `export`

Export your steam market history to an HTML, JSON or CSV file

> [!NOTE] 
> When running the tool you will be prompted to insert your steam credentials. All processing is done locally on your computer. This package does not save your credentials in any way.

Options:

- `--csv` - Export market transactions to csv file
- `--html` - Export market transactions to html file
- `--json` - Export market transactions to json file
- `--path` - Output directory for all file based operations (default: current working directory)
- `--launch` / `--no-launch` - Automatically open file(s) after export (default: `--launch`)
- `--cache` / `--no-cache` - Create a file cache for all market transactions (default: `--no-cache`)
- `--interactive` / `--non-interactive` - Interactive or non-interactive steam authentication [default: `--interactive`]

Examples:

Export your steam market history to a HTML file:
```shell
steam-market-history export --html
```

Export your steam market history to a CSV file in a specific directory:
```shell
steam-market-history export --csv --path /tmp/steam-market-history
```

### `version`

Display detailed information about this package. This includes the version, the license and the authors.

```
steam-market-history version
```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- BUILD WITH -->
## Built With

- [Python](https://www.python.org/)
- [Typer](https://typer.tiangolo.com/)

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

- [Typer](https://typer.tiangolo.com/)
- [Choose a license](https://choosealicense.com/)

<p align="right">(<a href="#top">back to top</a>)</p>

## Disclaimer:

The Steam Market History Exported is a community project and is not affiliated with Valve or Steam.

<p align="right">(<a href="#top">back to top</a>)</p>
