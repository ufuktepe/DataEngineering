# Data Engineering Service for the Microbiome Platform
Data Engineering service processes 16s rRNA sequencing files (fastq) through Qiime2 and generates feature tables and taxonomy analysis results.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip install -r requirements.txt
```

Install Qiime2: https://docs.qiime2.org/2023.2/install/

## Usage

1. Create an empty folder. This will be the <parent_dir>.
2. <parent_dir> should include subfolders for each sample. 
3. Each subfolder must include sequencing (fastq) file(s).
4. Additionally, each subfolder must include a complete.txt file.
5. Please look at the data folder to see the folder structure and required files. 
7. cd into this project. 
8. Run the following commands.

```python
source venv/bin/activate  
python3 main.py
```
