# Introduction to Data Analysis with Python

This course was put together for a Human Sciences student who already works with data in Stata and wants to get started with Python. It assumes no prior Python experience, but does assume familiarity with the basics of data analysis — variables, summary statistics, distributions, and simple regression — through prior use of Stata.

The approach is practical and hands-on: four one-hour sessions, each built around a Jupyter notebook that you run on your own Mac. Each session uses a real-world dataset from social science or public health, and introduces Python by drawing direct comparisons with what you already know from Stata. The goal is to reach the point where you can load, explore, visualise, and analyse a dataset independently in Python.

---

## Before you start

Read **[Prerequisites.md](Prerequisites.md)** first. It walks you through everything you need to install and set up on your laptop before opening any of the notebooks. The short version: install [Anaconda](https://www.anaconda.com/download), download this repository, and launch JupyterLab. The full instructions cover what to do if anything goes wrong.

---

## Sessions

| # | Topic | Notebook | Dataset |
|---|-------|----------|---------|
| 1 | Python and Jupyter: Getting Oriented | [Session 1](Session_01_Python_and_Jupyter.ipynb) | `car-sales.csv` |
| 2 | Data Wrangling with pandas | [Session 2](Session_02_Data_Wrangling.ipynb) | `ukhls_individual.csv`, `ukhls_household.csv` |
| 3 | Exploratory Data Analysis and Visualisation | [Session 3](Session_03_EDA_and_Visualisation.ipynb) | `wdi_2019.csv` |
| 4 | Statistical Analysis | [Session 4](Session_04_Statistical_Analysis.ipynb) | `hse_adults.csv` |

> **Tip:** GitHub renders Jupyter notebooks in the browser, so you can read through any session before downloading anything.

---

## How to use this repository

**If you are new to git and GitHub**, the simplest approach is:

1. Click the green **Code** button near the top of this page
2. Click **Download ZIP**
3. Extract the ZIP somewhere on your laptop (e.g. `Documents/PythonSessions`)
4. Follow the instructions in [Prerequisites.md](Prerequisites.md) to launch JupyterLab from that folder

**If you are comfortable with git**, clone the repository:

```bash
git clone https://github.com/malminhas/python-data-analysis.git
cd python-data-analysis
jupyter lab
```

Work through the sessions in order — each one builds on the previous.

---

## What is in this repository

### Notebooks

| File | Session |
|------|---------|
| `Session_01_Python_and_Jupyter.ipynb` | Python basics, Jupyter environment, first steps with pandas |
| `Session_02_Data_Wrangling.ipynb` | Cleaning, recoding, grouped summaries, merging files |
| `Session_03_EDA_and_Visualisation.ipynb` | Histograms, scatter plots, heatmaps, saving figures, CRAFT |
| `Session_04_Statistical_Analysis.ipynb` | t-tests, chi-square, OLS regression, exporting results |

### Datasets

| File | Used in | Description |
|------|---------|-------------|
| `car-sales.csv` | Session 1 | Global new car sales by type (electric vs non-electric), 2010-2025. Source: IEA via Our World in Data. |
| `ukhls_individual.csv` | Session 2 | 520 individuals — demographics, employment, income. Modelled on UK Household Longitudinal Study. |
| `ukhls_household.csv` | Session 2 | 280 households — region, tenure, amenities. Links to individual file via `hidp`. |
| `wdi_2019.csv` | Session 3 | ~100 countries, 10 development indicators (2019). Modelled on World Bank WDI. |
| `hse_adults.csv` | Session 4 | 600 English adults — health, lifestyle, blood pressure. Modelled on Health Survey for England. |

### Scripts

| File | What it does |
|------|-------------|
| `car_sales_craft.py` | A standalone CRAFT pipeline (Collect, Refine, Analyse, Fact-check, Transform) applied to the Session 1 dataset. Run with `python car_sales_craft.py`. |

---

## The CRAFT framework

Sessions 3 and 4 introduce **CRAFT** as a discipline for working with data responsibly:

| Step | What it means |
|------|--------------|
| **C**ollect | Bring your data together in one place |
| **R**efine | Clean, standardise, and de-duplicate |
| **A**nalyse | Ask questions of your data |
| **F**act-check | Verify figures against the source before publishing |
| **T**ransform | Convert your output into the format you need |

---

## Data sources

> Note: the UKHLS, WDI, and HSE datasets included here are synthetic teaching datasets with realistic structure and values. They are not the original survey data.

| Dataset | Original source |
|---------|----------------|
| Car sales | [IEA Global EV Outlook 2025](https://www.iea.org/reports/global-ev-outlook-2026) via [Our World in Data](https://ourworldindata.org/grapher/car-sales) (CC BY 4.0) |
| UKHLS-style data | Modelled on [Understanding Society](https://www.understandingsociety.ac.uk/) (UK Data Service) |
| WDI-style data | Modelled on [World Development Indicators](https://databank.worldbank.org/source/world-development-indicators) (World Bank, CC BY 4.0) |
| HSE-style data | Modelled on [Health Survey for England](https://ukdataservice.ac.uk/) (NHS England / UK Data Service) |
