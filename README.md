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
3. Each subfolder must include sequencing (fastq) and metadata (csv) files.
4. The sample name in the csv file must match the subfolder name.
5. Additionally, each subfolder must include a complete.txt file.
6. Please look at the data folder to see the folder structure, required files, and the metadata format. 
7. cd into this project. 
8. Run the following commands.

```python
source venv/bin/activate  
python3 data_engineering.py <parent_dir>
```

9. Results will be saved in an output folder in each sub-folder.
