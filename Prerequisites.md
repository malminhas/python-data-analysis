# Prerequisites

**Introduction to Data Analysis with Python**
*Setup guide for Session 1*

Complete all steps below before your first session. This should take around 20–30 minutes and only needs to be done once.

---

## Step 1: Install Anaconda

Anaconda is a free software bundle that installs Python, JupyterLab, and all the data analysis libraries used in this course in one go. You do not need to install anything else separately.

1. Go to [https://www.anaconda.com/download](https://www.anaconda.com/download)
2. Download the **macOS graphical installer** (the `.pkg` file)
3. Open the downloaded file and follow the on-screen instructions, accepting all defaults
4. When the installer finishes, you can delete the `.pkg` file

### Verify the installation

Open the **Terminal** app (press `Command + Space`, type `Terminal`, press Return) and run:

```bash
conda --version
```

You should see something like `conda 24.x.x`. If you see "command not found", try closing Terminal and opening it again — the PATH update sometimes needs a fresh session to take effect.

---

## Step 2: Download the course files

First, create a folder called `CODE` on your Desktop — this will be your home for all the course files:

```bash
mkdir ~/Desktop/CODE
```

### Option A: Clone with git (recommended)

If you have git installed, open Terminal and run:

```bash
cd ~/Desktop/CODE
git clone https://github.com/malminhas/python-data-analysis
```

This creates a `python-data-analysis` folder inside `CODE` containing all the course files.

### Option B: Download as a ZIP

1. Go to [https://github.com/malminhas/python-data-analysis](https://github.com/malminhas/python-data-analysis)
2. Click the green **Code** button
3. Click **Download ZIP**
4. Double-click the downloaded ZIP to extract it
5. Move the extracted folder into `~/Desktop/CODE` so the path is `Desktop/CODE/python-data-analysis`

---

## Step 3: Check the folder contents

After downloading, your folder should contain at least:

```
Session_01_Python_and_Jupyter.ipynb
car-sales.csv
Prerequisites.md
```

> **Important:** the notebook and `car-sales.csv` must be in the **same folder**. The notebook loads the CSV using a relative path (`pd.read_csv("car-sales.csv")`), so it looks in whichever folder it is sitting in.

---

## Step 4: Launch JupyterLab

In Terminal, navigate to the `python-data-analysis` folder inside your `CODE` folder and launch JupyterLab:

```bash
cd ~/Desktop/CODE/python-data-analysis
jupyter lab
```

A browser window will open automatically showing the JupyterLab interface. You should see the course files listed in the panel on the left.

> **Tip:** keep this Terminal window open while you work. JupyterLab runs from it in the background. When you are finished, come back to the Terminal window and press `Control + C` to shut it down.

---

## Step 5: Open the Session 1 notebook

In the JupyterLab file browser (left panel), double-click:

```
Session_01_Python_and_Jupyter.ipynb
```

The notebook will open in a new tab. You are ready to begin.

---

## Troubleshooting

### "command not found: jupyter"

Anaconda may not have been added to your PATH. Try running:

```bash
conda init zsh
```

Then close Terminal completely, reopen it, and try `jupyter lab` again.

If your Mac uses an older `bash` shell (common on older macOS), run `conda init bash` instead.

### The browser opens but shows an error page

JupyterLab may be trying to open on a port that is already in use. Try:

```bash
jupyter lab --port 8889
```

### "ModuleNotFoundError: No module named 'pandas'"

This should not happen with a standard Anaconda install, but if it does:

```bash
conda install pandas
```

### The notebook opens but `car-sales.csv` is not found

Check that `car-sales.csv` is in the same folder as the notebook file. In JupyterLab you can see all files in the left-hand panel.

---

## Libraries used in this course

All of the following are included with Anaconda and do not need to be installed separately:

| Library | What it does |
|---------|-------------|
| `pandas` | Data loading, cleaning, and analysis |
| `matplotlib` | Plotting and charts |
| `scipy` | Statistical tests |
| `statsmodels` | Regression models |
| `numpy` | Numerical computing (used internally by the above) |

---

## Quick reference: useful Terminal commands

| Command | What it does |
|---------|-------------|
| `pwd` | Print the current directory (where you are) |
| `ls` | List files in the current directory |
| `cd foldername` | Move into a folder |
| `cd ..` | Move up one level |
| `cd ~` | Go to your home directory |
| `jupyter lab` | Start JupyterLab in the current directory |
