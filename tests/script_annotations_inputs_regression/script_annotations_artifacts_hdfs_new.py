"""Regression test: compare the new Annotated style inputs declaration with the old version."""

try:
    from typing import Annotated  # type: ignore
except ImportError:
    from typing_extensions import Annotated  # type: ignore

from hera.shared import global_config
from hera.workflows import Workflow, script
from hera.workflows.artifact import Artifact, HDFSArtifact
from hera.workflows.steps import Steps

global_config.experimental_features["script_annotations"] = True


@script()
def read_artifact(
    my_artifact: Annotated[
        str,
        HDFSArtifact(
            name="my_artifact",
            path="tmp/file",
            addresses=[
                "my-hdfs-namenode-0.my-hdfs-namenode.default.svc.cluster.local:8020",
                "my-hdfs-namenode-1.my-hdfs-namenode.default.svc.cluster.local:8020",
            ],
            force=True,
            hdfs_user="root",
            krb_c_cache_secret={"name": "krb", "key": "krb5cc_0"},
            krb_config_config_map={"name": "my-hdfs-krb5-config", "key": "krb5.conf"},
            krb_keytab_secret={"name": "krb", "key": "user1.keytab"},
            krb_realm="MYCOMPANY.COM",
            krb_service_principal_name="hdfs/_HOST",
            krb_username="user1",
            hdfs_path="/tmp/argo/foo",
        ),
    ]
) -> str:
    return my_artifact


with Workflow(generate_name="test-artifacts-", entrypoint="my_steps") as w:
    with Steps(name="my_steps") as s:
        read_artifact(arguments=[Artifact(name="my_artifact", from_="somewhere")])
