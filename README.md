# Time Series Analysis Project

## Overview
This project focuses on time series analysis, including data preprocessing, decomposition, and forecasting using statistical and machine learning techniques. The primary goal is to analyze and forecast the daily mean temperature in Delhi.

## Table of Contents
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

## Project Structure
The project is organized into the following directories:

- `data`: Contains the datasets used for training and testing.
- `src`: Houses the source code for time series analysis.
  - `time_series`: The main package for the time series analysis.
    - `analysis.py`: Module for time series decomposition and forecasting.
    - `preprocessing.py`: Module for data preprocessing.
    - `validation.py`: Module for validation metrics.
    - `app.py`: Script to run a web app with Dash
- `tests`: Includes test files for exploratory analysis.

## Installation
Follow these steps to set up and install the project:


### 1. Clone the Repository
```bash
git clone <repository-url>
cd time-series-analysis
```
### 2. Install poetry 
If you don't have Poetry installed, follow the instructions on Poetry's official website https://python-poetry.org/ to install it.

### 3. Install Project Dependencies with Poetry
```bash
poetry install
```
This command reads the dependencies from the pyproject.toml file and creates a virtual environment with the required packages.


