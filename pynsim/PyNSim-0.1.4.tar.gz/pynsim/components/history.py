class History():
    def set(value, timestep):
        """
            Set a value at a given timestep
        """
        pass

    def get(attr, timestep=None):
        """
            Get the history for an attribute. If the timestamp (or timestamps)
            are set, then return a list of values

            Params:
                attr (string): The name of the attribute whose history you want
                timestep (string or List(string))

            Returns:
                int or List(int)* depending on whether a single timestamp is supplied
                or none. 
                *The return type will change depending on the type of data
        """

