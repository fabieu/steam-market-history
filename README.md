<div id="top"></div>

<!-- PROJECT SHIELDS -->

![PyPI](https://img.shields.io/pypi/v/steam-market-history?style=for-the-badge)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/steam-market-history?style=for-the-badge)
![Gitlab pipeline status](https://img.shields.io/gitlab/pipeline-status/sustineo/steam-market-history?style=for-the-badge)
![GitLab issues](https://img.shields.io/gitlab/issues/open/sustineo/steam-market-history?style=for-the-badge)
![GitLab merge requests](https://img.shields.io/gitlab/merge-requests/open-raw/sustineo/steam-market-history?style=for-the-badge)
![GitLab](https://img.shields.io/gitlab/license/sustineo/steam-market-history?style=for-the-badge)

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://gitlab.com/sustineo/steam-market-history">
    <img src="https://gitlab.com/sustineo/steam-market-history/-/raw/main/docs/images/logo.svg" alt="Logo" width="120" height="120">
  </a>

<h3 align="center">steam-market-history</h3>

  <p align="center">
    An easy-to-use CLI to export your steam market history to various formats
    <br />
    <a href="https://gitlab.com/sustineo/steam-market-history/-/raw/main/docs/demo.gif">View Demo</a>
    ·
    <a href="https://gitlab.com/sustineo/steam-market-history/-/issues">Report Bug</a>
    ·
    <a href="https://gitlab.com/sustineo/steam-market-history/-/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

steam-market-history is a command line tool written in Python which allows you to extract your entire Steam Market History with all transaction (sales/purchases) in a CSV or HTML file.

### Key features

- Extract your **entire** Steam Market History
- Create a CSV-File with all transactions
- Overview of _all_ transactions on a user-friendly webpage with searchable and filterable results

### Built With

- [Python](https://www.python.org/)
- [Typer](https://typer.tiangolo.com/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

- Python >= 3.8

### Installation

Pip (recommended):

```python
pip install steam-market-history
```

Manual:

1. Clone the repo
   ```sh
   git clone https://gitlab.com/sustineo/steam-market-history.git
   ```
2. Install poetry (if not already installled)
   ```sh
   pip install poetry
   ```
3. Install dependencies and start virtual environment
   ```sh
   poetry install && poetry shell
   ```
4. Start virtual environment
   ```sh
   poetry shell
   ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

Currently the following commands are supported:

### `export`

Export your steam market history to a CSV or HTML file

> When running the tool you will be prompted to insert your steam credentials. All processing is done locally on your own computer. This package does not save your credentials in any way.

Options:

- `--csv` - Export to csv file
- `--html` - Export to html file
- `--path` - Output directory for all file based operations (default: current working directory)
- `--launch` / `--no-launch` - Automatically open file(s) after export (default: `--launch`)
- `--cache` / `--no-cache` - Create a file cache for all market transactions (default: `--no-cache`)
- `--interactive` / `--non-interactive` - Interactive or non-interactive steam authentication [default: `--interactive`]

Example:

```
steam-market-history export --csv --path /tmp/out
```

### `version`

Display detailed information about this package

```
steam-market-history version
```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

- [ ] Add options of verbosity
- [ ] Export to JSON

See the [open issues](https://gitlab.com/sustineo/steam-market-history/-/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>

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

<!-- CONTACT -->

## Contact

sustineo\_ - [@sustineo\_](https://twitter.com/sustineo_) - dev@sustineo.de

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

- [Typer](https://typer.tiangolo.com/)
- [Choose a license](https://choosealicense.com/)

<p align="right">(<a href="#top">back to top</a>)</p>

## Disclaimer:

The Steam Market History Exported is a community project and is not affiliated with Valve or Steam.

<p align="right">(<a href="#top">back to top</a>)</p>
