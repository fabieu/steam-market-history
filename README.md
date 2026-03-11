<div id="top"></div>

<!-- PROJECT SHIELDS -->

[![GitHub Release](https://img.shields.io/github/v/release/fabieu/steam-market-history)](https://github.com/fabieu/steam-market-history/releases/latest)
[![GitHub Issues](https://img.shields.io/github/issues/fabieu/steam-market-history)](https://github.com/fabieu/steam-market-history/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/fabieu/steam-market-history)](https://github.com/fabieu/steam-market-history/pulls)
[![License](https://img.shields.io/github/license/fabieu/steam-market-history)](https://github.com/fabieu/steam-market-history/blob/main/LICENSE)

[![PyPI Version](https://img.shields.io/pypi/v/steam-market-history)](https://pypi.org/project/steam-market-history/)
[![Python Versions](https://img.shields.io/pypi/pyversions/steam-market-history)](https://pypi.org/project/steam-market-history/)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=fabieu_steam-market-history&metric=alert_status)](https://sonarcloud.io/summary/overall?id=fabieu_steam-market-history)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=fabieu_steam-market-history&metric=security_rating)](https://sonarcloud.io/summary/overall?id=fabieu_steam-market-history)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=fabieu_steam-market-history&metric=reliability_rating)](https://sonarcloud.io/summary/overall?id=fabieu_steam-market-history)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=fabieu_steam-market-history&metric=sqale_rating)](https://sonarcloud.io/summary/overall?id=fabieu_steam-market-history)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=fabieu_steam-market-history&metric=vulnerabilities)](https://sonarcloud.io/summary/overall?id=fabieu_steam-market-history)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=fabieu_steam-market-history&metric=sqale_index)](https://sonarcloud.io/summary/overall?id=fabieu_steam-market-history)

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

steam-market-history is a command line tool written in Python which allows you to extract your entire Steam Market
History with all transaction (sales/purchases) in a CSV or HTML file.

### Key features

- Extract your **entire** Steam Market History with all transactions to a HTML, CSV or JSON file
- Overview of _all_ transactions on a user-friendly webpage with searchable and filterable results

## Demo

<img src="https://raw.githubusercontent.com/fabieu/steam-market-history/main/docs/screenshot-html-export.png" alt="HTML Export Screenshot">

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

- Python >= 3.10

### Installation

Pip (recommended):

```shell
pipx install steam-market-history
```

Manual:

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

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

Currently, the following commands are supported:

### `export`

Fetch your Steam market history and export it to one or more file formats.

> [!NOTE]
> On the first run you will be prompted for your Steam credentials. After a successful login the session is cached
> locally so subsequent runs do not require you to log in again. All processing is done locally on your machine —
> credentials are never stored in plain text.

Options:

- `--csv` - Export market history as a CSV file
- `--html` - Export market history as an interactive HTML file
- `--json` - Export market history as a JSON file
- `--path` - Directory to write exported files into (default: `./export`)
- `--cache` - Cache fetched transactions to disk and reuse on subsequent runs (default: disabled)

Exported filenames include a unique ID (e.g. `steam-market-history-3f2e1a....csv`) to avoid overwriting previous
exports.

Examples:

Export your steam market history to a HTML file:

```shell
steam-market-history export --html
```

Export to CSV and JSON in a specific directory:

```shell
steam-market-history export --csv --json --path /tmp/steam-market-history
```

Export using a cached copy of your transaction history:

```shell
steam-market-history export --html --cache
```

### `version`

Display package version, author, and license information.

```shell
steam-market-history version
```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- BUILD WITH -->

## Built With

- [Python](https://www.python.org/)
- [Typer](https://typer.tiangolo.com/)
- [Rich](https://github.com/Textualize/rich)

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any
contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also
simply open an issue with the tag "enhancement".
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
