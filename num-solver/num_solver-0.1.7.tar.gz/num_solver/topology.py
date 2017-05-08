def num_links(R):
    pass

def num_flows(R):
    pass

def remove_extra_constraints(R, capacity):
    min_R = []
    min_capacity = []
    for i,v in enumerate(R):
        x = num_solver.solve_num_problem(lambda x: np.dot(v,x), R, capacity)
        if np.abs(np.dot(v,x) - capacity[i]) < 0.0001:
            min_R.append(v)
            min_capacity.append(capacity[i])
    return np.array(min_R, dtype='int'), np.array(min_capacity)
