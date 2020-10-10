import copy
import os
import os.path
from collections import defaultdict

import flask
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DEFAULT_ROOT_DIR = '/Users/Alien/workspace/project/private/dolphin-id/data/test'


def _is_image(file_path: str) -> bool:
    _, ext = os.path.splitext(file_path)
    print('Filepath: {}, Ext: {}'.format(file_path, ext))
    return ext.lower() in ('.jpg', '.jpeg')


@app.route('/dir', methods=['GET'])
def dir():
    root_dir = request.args.get('root_dir', DEFAULT_ROOT_DIR)
    print('Folder name:', root_dir)
    results = defaultdict(list)
    for item in os.listdir(root_dir):
        full_path = os.path.join(root_dir, item)
        if os.path.isdir(full_path):
            results['dirs'].append(full_path)
        else:
            results['files'].append(full_path)

    out = copy.deepcopy(results)
    out['dirs'] = sorted(out['dirs'])
    out['files'] = sorted([f for f in out['files'] if _is_image(f)])

    resp = flask.json.jsonify({
        'root_dir': root_dir,
        'contents': out,
    })
    print('Resp:', resp.get_json())

    return resp
