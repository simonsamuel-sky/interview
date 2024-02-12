from flask import Flask
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Asset Management API', description='API for asset management')

# Dummy data for demonstration purposes
assets = [
    {'id': 'M000001', 'name': 'Beekeeper'},
    {'id': 'M000002', 'name': 'Jurassic World'},
    {'id': 'M000003', 'name': 'Barbie'},
    {'id': 'M000004', 'name': 'Oppenheimer'},
    {'id': 'M000005', 'name': 'Aquaman'},
    {'id': 'M000006', 'name': 'Transformers'},
    {'id': 'M000007', 'name': 'The Marvels'},
    {'id': 'M000008', 'name': 'Avengers'},
]
workflows = [
]

workflow_sequence = 0


def add_workflow(asset_id, workflow_type):
    global workflow_sequence
    found = False
    for obj in assets:
        if obj['id'] == asset_id:
            found = True
            break
    if found:
        workflow_sequence += 1
        workflows.append({'id': workflow_sequence, 'assetId': asset_id, 'type': workflow_type, 'status': 'Pending'})

    return found


add_workflow("M000001", 'qc')
add_workflow("M000002", 'qc')


def complete_workflow(workflow_id):
    found = False
    for obj in workflows:
        if obj['id'] == workflow_id and obj['status'] == 'Pending':
            obj['status'] = 'Complete'
            found = True
            break
    return found


asset_model = api.model('Asset', {
    'id': fields.String(required=True, description='The asset ID'),
    'name': fields.String(required=True, description='The asset name'),
})

workflow_model = api.model('Workflow', {
    'id': fields.Integer(required=True, description='The workflow ID'),
    'assetId': fields.String(required=True, description='The asset ID associated with the workflow'),
    'type': fields.String(required=True, description='The type of the workflow'),
    'status': fields.String(required=True, description='The status of the workflow'),
})


@api.route('/assets')
class AssetsResource(Resource):
    @api.marshal_with(asset_model, as_list=True)
    def get(self):
        return assets


@api.route('/assets/<string:asset_id>/initiate-workflow/<string:workflow_type>')
class InitiateWorkflowResource(Resource):
    @api.doc(responses={
        200: 'Success',
        404: 'Not found'
    })
    def post(self, asset_id, workflow_type):
        success = add_workflow(asset_id, workflow_type)
        if not success:
            return {'message': 'Asset not found'}, 404
        return {'message': 'Workflow initiated successfully'}


@api.route('/workflows/list')
class WorkflowsResource(Resource):
    @api.marshal_with(workflow_model, as_list=True)
    def get(self):
        return workflows


@api.route('/workflows/<int:workflow_id>/complete')
class CompleteWorkflowResource(Resource):
    @api.doc(responses={
        200: 'Success',
        404: 'Not found'
    })
    def put(self, workflow_id):
        success = complete_workflow(workflow_id)
        # Dummy implementation for completing workflow
        # Implementation for completing workflow
        if success == False:
            return {'message': 'Cannot find workflow'}, 404
        return {'message': 'Workflow completed successfully'}


if __name__ == '__main__':
    app.run(debug=True)
