import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ['ROOT_DIR'] = ROOT_DIR

from upload_to_elasticsearch.elastic import run_elastic_upload

run_elastic_upload()