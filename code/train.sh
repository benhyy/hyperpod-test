cd /opt/ml/code

/usr/local/bin/python -m pip install -r requirements.txt
# /usr/local/bin/python sft_train.py
torchrun \
    --nproc_per_node 4 \
    --nnodes 2 \
    sft_train.py