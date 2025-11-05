

cd code && tar -czf ../sourcedir.tar.gz . && cd ..

aws s3 cp sourcedir.tar.gz s3://andjsmi-data-testing/hyperpod-prebiult/

export SAGEMAKER_SUBMIT_DIRECTORY="s3://andjsmi-data-testing/hyperpod-prebiult/sourcedir.tar.gz"

cat trainer.yaml.template | envsubst > trainer.yaml

kubectl delete -f trainer.yaml &&  kubectl apply -f trainer.yaml

kubectl logs -f -l training.kubeflow.org/job-name=pytorch-prebuilt