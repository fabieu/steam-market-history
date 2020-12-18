# Steam Market History Exporter

The Steam Market History Exporter is a command line tool written completly in Python which allows you to extract your entire Steam Market History with all transaction (sales/purchases) in a reusable csv file. In addition a html file is generated automatically to view your transactions directly in the web browser.

## Features

- Extract your **entire** Steam Market History
- Creation of a .csv file with all transactions
- Overview of all transactions represented user friendly in your web browser
- Filtering of transcations via price, name and/or date of sale respectivly purchase
- (_Soon:_ Automatic calculation of the sum of the prices for the transactions selected)

## Requirements

- **Python 3.X:**
  - [Download Python](https://www.python.org/downloads/)
- **pip - The Python Package Installer:** (pip is already installed if you are using Python 3 >=3.4 downloaded from python.org)
  - Otherwise you can install pip by using the following [instructions](https://pip.pypa.io/en/stable/installing/)

## Installation

Navigate to the cloned repo and run the following command to install all required dependencies:

If you dont want to install the packages in your main package repository you can use a virtual environment. For more instructions visit the official Python documentation.

```bash
pip install -r requirements.txt
```

### Usage:

1. Start the tool by double-clicking the _app.<span></span>py_ file
2. A command prompt should open which will guide you through the sequence of steps neccessary to fetch your data from Steam and convert the data into the appropriate files.
3. After the tool is finished it will close itself and open a browser window for you to view your transactions

## Configuration

Currently there are not many configuration options available.
For now you can only customize the printed table via the _./libary/view.css_ file. The table has the attribut _id="data"_

## Licence

The MIT License (MIT)  
Copyright &copy; 2020 Fabian Eulitz

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

The software is provided “as is”, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the software.

#### Note: The Steam Market History Exported is a community project and is not affiliated with Valve or Steam.
