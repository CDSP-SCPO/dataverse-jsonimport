# DV json process/import tool

Removes custom controlled vocabulary fields from json with existing doi and can also import it into dv.

- Set up virtual env: `python3 -m venv .venv`
- Activate env: `source .venv/bin/activate`
- Install requirements: `pip install -r requirements.txt`
- Run the script: `python process.py --help`

The files to be processed/imported have to be in a `input` folder at the root of this directory. Processed files will appear in a `output` directory.
