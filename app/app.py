import copy
import datetime
import enum
import io
import json
import os
import os.path
import shutil
from collections import defaultdict
from http import HTTPStatus

import flask
from flask import Flask, request
from flask_cors import CORS
from google.cloud import automl
from google.protobuf.json_format import MessageToDict, MessageToJson

app = Flask(__name__)
CORS(app)

DEFAULT_ROOT_DIR = '/Users/Alien/workspace/project/private/dolphin-id/data/test'
DEFAULT_IMG_PATH = '/Users/Alien/workspace/project/private/dolphin-id/data/test/HL20100702_01_Gg_990702 (99).JPG'


class FileType(enum.Enum):
    UNKNOWN = 'unknown'
    IMAGE = 'image'
    LABEL_VIA = 'label_via'


def _is_image(ext: str) -> bool:
    return ext.lower() in ('.jpg', '.jpeg', 'png')


def _is_label_via(ext: str) -> bool:
    return ext.lower() in ('.json')


def _get_type(file_path: str) -> FileType:
    _, ext = os.path.splitext(file_path)
    print('Filepath: {}, Ext: {}'.format(file_path, ext))
    if _is_image(ext):
        return FileType.IMAGE

    if _is_label_via(ext):
        return FileType.LABEL_VIA

    return FileType.UNKNOWN


def _is_eligible(file_tp: FileType) -> bool:
    return (file_tp == FileType.IMAGE or file_tp == FileType.LABEL_VIA)


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
    out['files'] = sorted(
        [f for f in out['files'] if _is_eligible(_get_type(f))]
    )

    return flask.json.jsonify({
        'root_dir': root_dir,
        'contents': out,
    })


@app.route('/img', methods=['GET'])
def get_img():
    img_path = request.args.get('img_path', DEFAULT_IMG_PATH)
    print('Image file path:', img_path)
    if not os.path.exists(img_path):
        resp = flask.make_response(
            {
                'comment': 'No file for path input: {}'.format(img_path),
            }
        )
        resp.status_code = HTTPStatus.BAD_REQUEST
        return resp

    return flask.send_file(
        img_path,
        mimetype='image/jpeg',
    )


@app.route('/label', methods=['GET'])
def get_label():
    file_path = request.args.get('file_path', DEFAULT_IMG_PATH)
    print('Label file path:', file_path)
    if not os.path.exists(file_path):
        resp = flask.make_response(
            {
                'comment': 'No file for path input: {}'.format(file_path),
            }
        )
        resp.status_code = HTTPStatus.BAD_REQUEST
        return resp

    file_type = _get_type(file_path)
    if file_type != FileType.LABEL_VIA:
        resp = flask.make_response(
            {'comment': 'File format is wrong: {}'.format(file_path)}
        )
        resp.status_code = HTTPStatus.BAD_REQUEST
        return resp

    return flask.send_file(
        file_path,
        mimetype='application/json',
    )


@app.route('/save', methods=['POST'])
def save_data():
    try:
        req_json = request.json

        folder = req_json.get('folder', '')
        filename = req_json.get('filename', '')
        is_force = bool(req_json.get('is_force', 0))
        data = req_json.get('data', {})

        if not folder:
            resp = flask.make_response(
                {'comment': 'One needs to specify folder.'}
            )
            resp.status_code = HTTPStatus.BAD_REQUEST
            return resp

        if not os.path.exists(folder) or not os.path.isdir(folder):
            resp = flask.make_response(
                {
                    'comment':
                        'Folder specified does not exist: {}'.format(folder)
                }
            )
            resp.status_code = HTTPStatus.BAD_REQUEST
            return resp

        if not data:
            resp = flask.make_response({'comment': 'No data in the request.'})
            resp.status_code = HTTPStatus.BAD_REQUEST
            return resp

        if not filename:
            dt = datetime.datetime.now()
            filename = '{}.json'.format(dt.strftime('%Y%m%d_%H%M%S'))

        full_path = os.path.join(folder, filename)
        if os.path.exists(full_path) and not is_force:
            resp = flask.make_response(
                {
                    'comment':
                        'File specified is already existed: {}'.
                        format(full_path)
                }
            )

        with open(full_path, 'w') as f:
            json.dump(data, f)

        resp = flask.make_response(
            {'comment': 'Data is already written to {}'.format(full_path)}
        )
        resp.status_code = HTTPStatus.OK
        return resp
    except Exception as e:
        resp = flask.make_response(
            {'comment': 'Some error happens: {}'.format(e)}
        )
        resp.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        return resp
