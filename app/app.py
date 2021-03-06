import copy
import datetime
import os
import os.path
import shutil
from collections import defaultdict
from http import HTTPStatus
import json
import io

import flask
from flask import Flask, request
from flask_cors import CORS
from google.cloud import automl
from google.protobuf.json_format import MessageToJson, MessageToDict

app = Flask(__name__)
CORS(app)

DEFAULT_ROOT_DIR = '/Users/Alien/workspace/project/private/dolphin-id/data/test'
DEFAULT_IMG_PATH = '/Users/Alien/workspace/project/private/dolphin-id/data/test/HL20100702_01_Gg_990702 (99).JPG'


def _is_image(file_path: str) -> bool:
    _, ext = os.path.splitext(file_path)
    print('Filepath: {}, Ext: {}'.format(file_path, ext))
    return ext.lower() in ('.jpg', '.jpeg', 'png')


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


@app.route('/predict', methods=['POST'])
def predict():
    #     print(request.data)
    #
    #     if not request.data:
    #         return flask.make_response({
    #             'payload': [],
    #         })

    project_id = 'dolphin-170615'
    location = 'us-central1'
    model_id = 'IOD5909958562179710976'
    file_path = '/Users/Alien/workspace/project/private/dolphin-id-backend/data/HL20100702_01_Gg_990702_97.jpg'

    prediction_client = automl.PredictionServiceClient()

    # Get the full path of the model.
    model_full_id = automl.AutoMlClient.model_path(
        project_id, location, model_id
    )

    # Read the file.
    with open(file_path, "rb") as content_file:
        content = content_file.read()


#     image = automl.Image(image_bytes=content)

    if request.data:
        content = request.data

    print(request.data)
    print(request.get_data())
    image = automl.Image(image_bytes=content)
    payload = automl.ExamplePayload(image=image)

    # params is additional domain-specific parameters.
    # score_threshold is used to filter the result
    # https://cloud.google.com/automl/docs/reference/rpc/google.cloud.automl.v1#predictrequest
    params = {
        'score_threshold': '0.01',
    }

    pred_req = automl.PredictRequest(
        name=model_full_id,
        payload=payload,
        params=params,
    )

    pred_resp = prediction_client.predict(request=pred_req)
    pred_resp_json = pred_resp.__class__.to_json(pred_resp)

    resp = flask.make_response(json.loads(pred_resp_json))
    resp.status_code = HTTPStatus.OK
    return resp


@app.route('/cp', methods=['GET'])
def cp():
    from_path = request.args.get('from', '')
    to_path = request.args.get('to', '')
    if not from_path or not to_path:
        resp = flask.make_response(
            {
                'msg':
                    'One of from and to is empty: from(%s), to(%s)'.format(
                        from_path, to_path
                    ),
            },
        )
        resp.status_code = HTTPStatus.BAD_REQUEST
        return resp

    if not os.path.exists(from_path):
        resp = flask.make_response(
            {
                'msg': 'File does not exist in from path: %s'.format(from_path),
            },
        )
        resp.status_code = HTTPStatus.BAD_REQUEST
        return resp

    shutil.copyfile(
        src=from_path,
        dst=to_path,
    )
    resp = flask.make_response(
        {'msg': 'Copy file from %s to %s'.format(from_path, to_path)}
    )
    resp.status_code = HTTPStatus.OK
    return resp
