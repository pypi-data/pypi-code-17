import lasagne


''' 
    define experiment config structure
    expt = {}
    expt['db_name']
    expt['data_dir']
'''

def fill_net_from_caffe_net(net_caffe, net):
    # Copy parameters
    layers_caffe = dict(zip(list(net_caffe._layer_names), net_caffe.layers))
    for name, layer in net.items():
        try:
            if type(layer) == lasagne.layers.special.ParametricRectifierLayer:
                # Slope: caffe in layers_caffe[name].blobs[0].data
                print "Setting pReLU slope for", name
                layer.alpha.set_value(layers_caffe[name].blobs[0].data)
            else:
                if type(layer)==lasagne.layers.dense.DenseLayer:
                    print "Transposing weights for layer",name
                    layer.W.set_value(layers_caffe[name].blobs[0].data.transpose())
                elif type(layer)==lasagne.layers.Conv2DLayer: # We should check if ConvLayer is cudnn or not...
                    # flip filters when not using cudnn
                    print "Flipping fitlers because we do not use Conv2DDNNLayer for",name
                    layer.W.set_value(layers_caffe[name].blobs[0].data[..., ::-1, ::-1])
                else:
                    layer.W.set_value(layers_caffe[name].blobs[0].data)
                layer.b.set_value(layers_caffe[name].blobs[1].data)
        except Exception as e:
            print "Issue when setting weights for layer", name, str(e)
            continue
    return net

def fill_net_from_caffe_protxt(caffe_model_prototxt,caffe_model_path,net):
    # Load caffe net
    import caffe
    # No need for GPU to load parameters
    caffe.set_mode_cpu()
    net_caffe = caffe.Net(caffe_model_prototxt, caffe_model_path, caffe.TEST)
    net = fill_net_from_caffe_net(net_caffe,net)
    return net