from hera.v1.artifact import InputArtifact, OutputArtifact
from hera.v1.input import InputFrom
from hera.v1.task import Task
from hera.v1.workflow import Workflow
from hera.v1.workflow_service import WorkflowService


def writer():
    import json

    with open('/file', 'w+') as f:
        for i in range(10):
            f.write(f'{json.dumps(i)}\n')


def fanout():
    import json
    import sys

    indices = []
    with open('/file', 'r') as f:
        for line in f.readlines():
            indices.append({'i': line})
    json.dump(indices, sys.stdout)


def consumer(i: int):
    print(i)


ws = WorkflowService('my-argo-server.com', 'my-auth-token')
w = Workflow('artifact-with-fanout', ws)
w_t = Task('writer', writer, output_artifacts=[OutputArtifact(name='test', path='/file')])
f_t = Task(
    'fanout',
    fanout,
    input_artifacts=[InputArtifact(from_task='writer', artifact_name='test', name='test', path='/file')],
)
c_t = Task('consumer', consumer, input_from=InputFrom(name='fanout', parameters=['i']))
w_t >> f_t >> c_t
w.add_tasks(w_t, f_t, c_t)
w.submit()
