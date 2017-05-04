class Account(object):
    '''
    Author: 
        Alex Katona
        
    Description: 
        This class will create a LinkedIn 
        Account that can have a network of
        connections that is searchable.
      
    parameters:
        none
    
    methods:
        add: Add a User to your network
        number_of_connections: Return the number of connections in your network
        search: Search your network using a string keyword
        store: Save the current state of your account
        restore: Restore a previous state of your account
    '''
    def __init__(self,storer=None):
        '''This class creates a new LinkedIn Account.
        There are no connections/users in the network
        when the account is created'''
        self.network = []
        self.storer = storer
    
    def add(self, name):
        '''Add a user to the account's network if they 
        are not already LinkedIn connections'''
        for user in self.network:
            if user.name == name:   
                return self
                
        self.network.append(User(name))
        return self
    
    def number_of_connections(self):
        '''Return the number of connections 
        that are in the account's network'''
        return len(self.network)
    
    def search(self,keyword):
        '''Search the names of the connections
        in the account's network using a string keyword 
        and return a list of those connections'''        
        return [i.name for i in self.network if keyword.upper() in i.name.upper()]

    def store(self):
        '''Save an account's state 
        to the database'''
        return self.storer.store_account(self)

    def restore(self, id):
        '''Restore an account's state 
        from the database'''
        self.network = self.storer.retrieve_account(id).network
        return self

class User(object):
    '''This class creates a new LinkedIn User'''
    def __init__(self, name):
        self.name = name
  
class DataAccess(object):
    def store_account(self, account):
        '''Save the account's state in the database as 
    a backup and return an id'''
        pass

    def retrieve_account(self, id):
        '''Restore an account's state
    from the database based on the id
    created by the store_account method'''
        pass