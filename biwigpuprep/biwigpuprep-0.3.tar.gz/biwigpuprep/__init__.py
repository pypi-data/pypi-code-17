import os
import subprocess
import tensorflow as tf

def GPUSession(verbose=False):
    # run this beforehand
    # check if SGE_GPU variable is set
    if os.environ.get('SGE_GPU') is None:
        gpu_num = subprocess.check_output("grep -h $(whoami) /tmp/lock-gpu*/info.txt | sed  's/^[^0-9]*//;s/[^0-9].*$//'",
                    shell=True).decode('ascii').strip()
        os.environ['SGE_GPU'] = gpu_num
    os.environ["CUDA_VISIBLE_DEVICES"] = os.environ['SGE_GPU']
    # config
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True #Do not assign whole gpu memory, just use it on the go
    if verbose is True:
        config.log_device_placement = True
    config.allow_soft_placement = True #If a operation is not define it the default device, let it execute in another.
    return tf.Session(config=config)