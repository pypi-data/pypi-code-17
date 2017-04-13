from sklearn.tree import _tree
import matplotlib.pyplot as plt

def leaf_depths(tree, node_id = 0): 

    left_child = tree.children_left[node_id]
    right_child = tree.children_right[node_id]

    if left_child == _tree.TREE_LEAF: 
        depths = np.array([0])

    else:
        left_depths = leaf_depths(tree, left_child) + 1
        right_depths = leaf_depths(tree, right_child) + 1
        depths = np.append(left_depths, right_depths)
 
    return depths

def leaf_samples(tree, node_id = 0):
    
    left_child = tree.children_left[node_id]
    right_child = tree.children_right[node_id]

    if left_child == _tree.TREE_LEAF:
        samples = np.array([tree.n_node_samples[node_id]])

    else:
        left_samples = leaf_samples(tree, left_child)
        right_samples = leaf_samples(tree, right_child)

        samples = np.append(left_samples, right_samples)

    return samples

def draw_tree(ensemble, tree_id=0, plot=False):

    plt.figure(figsize=(8,8))
    plt.subplot(211)

    tree = ensemble.estimators_[tree_id].tree_

    depths = leaf_depths(tree)
    plt.hist(depths, histtype='step', color='#9933ff', 
            bins=range(min(depths), max(depths)+1))

    plt.xlabel("Depth of leaf nodes (tree %s)" % tree_id)

    plt.subplot(212)

    samples = leaf_samples(tree)
    plt.hist(samples, histtype='step', color='#3399ff', 
            bins=range(min(samples), max(samples)+1))

    plt.xlabel("Number of samples in leaf nodes (tree %s)" % tree_id)

    if plot:
        plt.show()

def draw_ensemble(ensemble, plot=False):

    plt.figure(figsize=(8,8))
    plt.subplot(211)

    depths_all = np.array([], dtype=int)

    for x in ensemble.estimators_:
        tree = x.tree_
        depths = leaf_depths(tree)
        depths_all = np.append(depths_all, depths)
        plt.hist(depths, histtype='step', color='#ddaaff', 
                  bins=range(min(depths), max(depths)+1))

    plt.hist(depths_all, histtype='step', color='#9933ff', 
            bins=range(min(depths_all), max(depths_all)+1), 
            weights=np.ones(len(depths_all))/len(ensemble.estimators_), 
            linewidth=2)
    plt.xlabel("Depth of leaf nodes")

    samples_all = np.array([], dtype=int)

    plt.subplot(212)

    for x in ensemble.estimators_:
        tree = x.tree_
        samples = leaf_samples(tree)
        samples_all = np.append(samples_all, samples)
        plt.hist(samples, histtype='step', color='#aaddff', 
              bins=range(min(samples), max(samples)+1))

    plt.hist(samples_all, histtype='step', color='#3399ff', 
          bins=range(min(samples_all), max(samples_all)+1), 
          weights=np.ones(len(samples_all))/len(ensemble.estimators_), 
          linewidth=2)
    plt.xlabel("Number of samples in leaf nodes")

    if plot:
        plt.show()
