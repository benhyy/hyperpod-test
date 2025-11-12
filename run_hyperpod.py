import argparse
import boto3
import hydra
import subprocess
from jinja2 import Environment, FileSystemLoader
from omegaconf import DictConfig, OmegaConf
from sagemaker.fw_utils import tar_and_upload_dir

@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig) -> None:
    bucket = cfg.bucket
    source_dir = cfg.source_dir
    entry_point = cfg.script

    session = boto3.Session()

    uploaded_code = tar_and_upload_dir(
        session,
        bucket,
        "code",
        entry_point,
        source_dir,
    )

    print(uploaded_code)

    env = Environment(loader=FileSystemLoader('conf'))
    job_template = env.get_template('training_job.yaml.template')

    filled_template = job_template.render(
        script=uploaded_code.script_name,
        source_dir=source_dir,
        s3_prefix=uploaded_code.s3_prefix,
        model_dir=cfg.model_dir,
        model_local_dir=cfg.model_local_dir,
        job_name=cfg.job_name
    )

    print(filled_template)

    with open('job.yaml', 'w+') as f:
        f.write(filled_template)
        f.close()

    process = subprocess.Popen(
        ['kubectl', 'apply', '-f', 'job.yaml'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = process.communicate()

    return None

if __name__ == "__main__":
    main()