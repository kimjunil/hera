"""Regression test: compare the new Annotated style inputs declaration with the old version."""

try:
    from typing import Annotated  # type: ignore
except ImportError:
    from typing_extensions import Annotated  # type: ignore

from hera.shared import global_config
from hera.workflows import Workflow, script
from hera.workflows.artifact import Artifact, GCSArtifact
from hera.workflows.steps import Steps

global_config.experimental_features["script_annotations"] = True


@script()
def read_artifact(
    my_artifact: Annotated[
        str,
        GCSArtifact(
            name="my_artifact",
            path="tmp/file",
            bucket="my-bucket-name",
            key="path/in/bucket",
            service_account_key_secret={"name": "my-gcs-credentials", "key": "serviceAccountKey"},
        ),
    ]
) -> str:
    return my_artifact


with Workflow(generate_name="test-artifacts-", entrypoint="my_steps") as w:
    with Steps(name="my_steps") as s:
        read_artifact(arguments=[Artifact(name="my_artifact", from_="somewhere")])
