import argparse
import json
import os
import shutil

import requests

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'

REMOVE_FIELDS = [
    'keyword',
    'topicClassification',
    'kindOfData',
    'samplingProcedure',
    'collectionMode',
    'unitOfAnalysis',
    'timeMethod',
    'researchInstrument',
]

def main(args):
    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for filename in os.listdir(INPUT_DIR):
        with open(os.path.join(INPUT_DIR, filename), 'r') as file:
            file_str = file.read().replace('Catalogues', 'data Sciences Po')
            metadata = json.loads(file_str)
            for block in metadata['datasetVersion']['metadataBlocks'].values():
                block['fields'] = [field for field in block['fields'] if field['typeName'] not in REMOVE_FIELDS]

            ouput_filename = os.path.join(OUTPUT_DIR, filename)
            with open(ouput_filename, 'w+') as output:
                json.dump(metadata, output)

            print("file processed")

            if args.upload:
                print("importing file to dv")
                doi = os.path.join(metadata['authority'], metadata['identifier'])
                response = upload(ouput_filename, doi, api_key=args.api_key, dv_id=args.dv_id)
                print(response.content.decode())

def upload(filename, doi, api_key=None, dv_id=None, release='no'):
    url = f'https://dataspire-test.sciencespo.fr/api/dataverses/{dv_id}/datasets/:import?pid=doi:{doi}&release={release}'
    with open(filename, 'r') as payload:
        headers = {'X-Dataverse-key': api_key}
        return requests.post(url, data=payload.read(), headers=headers)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Removes custom controlled vocabulary fields from json with existing doi and can also import it into dv.')
    parser.add_argument('-u', '--upload', dest='upload', action='store_true', help='import files in dataverse')
    parser.add_argument('-d', '--dest', dest='dv_id', help='destination dataverse id')
    parser.add_argument('-k', '--key', dest='api_key', help='api key')
    args = parser.parse_args()
    main(args)
