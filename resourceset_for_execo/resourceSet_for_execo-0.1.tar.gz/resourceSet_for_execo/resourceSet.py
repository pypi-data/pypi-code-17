"""
	Authors : Timothee Lemaire & Nicolas Homberg
	
"""
import copy
import xml.etree.ElementTree as ET
import execo
from xml.etree import ElementTree
from xml.dom import minidom


"""
    ``ResourceSet`` module
    ======================
 
    Used to gather resources into an object with several usefull functions 
 
    :Example:
 
    >>> from resourceSet import *
    >>> resource_set = parser_xml("resourceSet.xml")
    >>> for i in resource_set :
    >>>     print i 
    node1
    node2
    node3
    node4

 
    important features :
    -------------------
 
    Resource_set is made iterable by using the class ResourceSetIterator(resource_set,"type ask")
    resource_set behave like a usual python list
    Most of the list function are available : 
        del 
        resourceSet[indice]
        resourceSet.append(..)
        len(resourceSet)

    Every functions embodied documentation, and to acces documention simply call help(function ) in python shell
 
 
"""


#A Resource maps a computational resource to an object which keeps 
#Certains characteritics such as type, name, gateway.
class Resource(object):
    """
        Class Resource 

        Attributes:
            type         type of the resource of type string
            properties   properties of the resources of type dict

    """

    def __init__(self,typ=None, prop=None , name = None, host = None):
        """ Creates a new Resource Object.


            :param typ: the type of the object could be "node"  or "Resource_set"
            :param prop:  object property
            :param name: String name
            :param host: Host to convert
            :type typ: string
            :type prop: dict
            :type name: string
            :type host: execo.host
            :return: Resource Object
            :rtype: Resource

            :Example:

            >>> r = Resource("node",name="toto")
            <resourceSet.Resource object at .... >
        """
        if host :
            if typ :
                self.type = typ
            else :
                self.type = 'node'
            self.properties = {'address':host.address,'user':host.user,'keyfile':host.keyfile,'port':str(host.port)}
            if prop : 
                self.properties.update(prop)
            if name :
                self.properties["name"] = name

        elif typ :
            self.type = typ #type of the resource
            self.properties = dict()  #properties of the resources
            if prop : 
                self.properties = prop

            if name :
                self.properties["name"] = name 


    def name(self) :
        """ Return the name of the resource.

            :return: the name of the resource
            :rtype: str


        """
        return self.properties["name"]

    def __str__(self) :
        """ Return the name of the resource.

            :return: the name of the resource
            :rtype: str

            call with str(obj)

             :Example:

            >>> str(r)
            toto
        """
        if "name" in self.properties :
            return self.properties["name"]
        else : return "nameless"

    def name_equal(self,name):
        """ Sets the name of the resource.

            :param name: String name
            :type name: string
        """
        self.properties["name"] = name
        return self
    

    def ssh_user(self):
        """ Return propertie ssh_user.

            :return: propertie ssh_user.
        """
        if "ssh_user" in self.properties :
            return self.properties["ssh_user"]
        return None
    
    def gw_ssh_user(self):
        """ Return propertie gw_ssh_user.

            :return: properties gw_ssh_user.
        """
        if "gw_ssh_user" in self.properties :
            return self.properties["gw_ssh_user"]
        return None
        
    def corresponds(self, props ):
        """ check if a resource corresponds to the props
           
            Also test whenever a value of the properties are callable: test the callable value with key as an argument


            :param prop:  object property
            :type prop: dict

            :return: True if the resource have the same properties than the parameters 
            :rtype: Bool
        """        
        for key,value in props.items():
            if callable(value) :
                if key in self.properties :
                    if not value(self.properties[key]):
                        return False
                else : 
                    return False
            else :
                if key in self.properties :
                    if (self.properties[key] != value):
                        return False
                else :
                    return False
        return True  # return props == self.preperties ? 

    
  
    def copy(self):
        """Creates a copy of the resource object.
            
            :return: copy of the resource
            :rtype: Resource object

        """
        result = Resource(self.type)
        result.properties =  self.properties 
        return result
    

    def __eq__( self,res ): 
        """
            Equality, Two Resource objects are equal if they have the 
            same type and the same properties as well.
            

            :return: result of the test
            :rtype: boolean

        """
        return self.type == res.type and self.properties == res.properties
    

    def eql( self,res ):
        """
            Equality, Two Resource objects are equal if they have the 
            same type and the same properties as well.
            

            :return: true if self and other are the same object.
            :rtype: boolean

        """
        if self.type == res.type and self.__class__ == res.__class__:
            for key,value in self.properties.items():
                if(res.properties[key] != value):
                    return False 
            return True 
        else :
            return False

    def gateway(self):
        """ Returns the name of the gateway

            :return: Returns the name of the gateway
            :rtype: string
        """
        if "gateway" in self.properties:
            return self.properties["gateway"] 
        return "localhost"
    

    def gateway_equal(self,host):
        """ set the getaway
            
    
            :param host:  host to be set
            :type host: string
    
        """
        self.properties["gateway"] = host
        return self
    
    #alias gw gateway
    gw = gateway


    def job(self):
        """ get the id of the resource 

            :return: Returns id 
            :rtype: int

        """
        if "id" in self.properties:
            return self.properties["id"] 
        return 0



    def make_taktuk_command(self,cmd) :
        """
            Use to make the list of machines for
    
            :return: the taktuk command
            :rtype: string
        """
        return " -m " +self.name()
    
    def host(self) :
        """
            try to convert the ressource as an execo host
            use the properties : gateway, user, keyfile and port
            default gateway is localhost.

            :return: an execo Host
            :rtype: execo.Host
        """
        if "gateway" in self.properties :
            address = self.properties["gateway"]
        else :
            address = "localhost"
        if "user" in self.properties :
            user = self.properties["user"]
        else :
            user = False
        if "keyfile" in self.properties :
            keyfile = self.properties["keyfile"]
        else :
            keyfile = False
        if "port" in self.properties :
            port = int(self.properties["port"])
        else :
            port = False
        return execo.Host(address,user,keyfile,port)


    #TODO Convertion into and from execo Process. relevant ? 
    

#class ResourceSetIterator

"""********************************
classe resourceSet  : 
    

***********************************"""


class ResourceSet(Resource):
    """
        Class ResourceSet heret from Resource

        Attributes: 
            type         (inheret from Resource) type of the resource of type string
            properties   (inheret from Resource) properties of the resources of type dict
            Resource     list of the resources
            resrouces_files  

    """
    
    def __init__(self, name = None ):
        """ Creates a new ResourceSet Object.


            :param name: String name
            :type name: string


            :return: Resourceset Object
            :rtype: ResourceSet

            :Example:

            >>> r = ResourceSet("node",name="toto")
            <resourceSet.ResourceSet object at .... >
        """
        super(ResourceSet, self).__init__("resource_set", None, name )
        self.resources = []
        self.resource_files = dict()
        


    def copy(self):
        """Creates a copy of the ResourceSet Object
            :return: Resourceset Object
            :rtype: ResourceSet
        """
        result = ResourceSet()
        result.properties = self.properties 
        for resource in self.resources :
            result.resources.append(copy.deepcopy(resource))

        return result
        

    def append(self, resource ):
        """Add a Resource object to the ResourceSet
        

        :param resource: the resource or ResourceSet to add to the atributes resources of the current resourceSet
        :type resource : Objet ( can be Resource or ResourceSet )
        named append to stick with the usel python function 
        
        """      
        self.resources.append( resource )
        return self
        

    def first (self, type=None ):
        """ Return the first element which is an object of the Resource Class

            :param type:  the type of the object could be "node"  or "Resource_set"
            :type type: string

            :return: 
            :rtype: Resource
        """
        for resource in self.resources:
            if (resource.type == type) :
                return resource
            elif isinstance(resource,ResourceSet):
                res = resource.first( type )
                if (res) :
                    return res 
            elif (not type) :
                return resource
        return None
        

    def select_resource(self, props ):
        """ Return the first element which correspond to the properties given in parameters

            :param props: props which the ressource should correspond to
            :type props: string

            :return: return the selected Resource Object
            :rtype: Resource
        """
        for resource in self.resources:
            if resource.corresponds( props ) :
                return resource


    def select(self, type=None, props=None , block=None):
        """ select every resource of the given type which correspond to the props or the block ( see warnings ) and wrap it in a ResourceSet
            

            :param type:  the type of the object could be "node"  or "Resource_set"
            :param props: props which the ressource should correspond to
            :param block:  function or lambda function which return boolean 
            :type type: string
            :type props: dict
            :type block: function or lambda function which return boolean


            :return: return a ResourceSet with all the resources which are selected
            :rtype: Resource

            :Example:
            >>> r2 = r.select('node',block = (lambda x : x.name()=='tutu'))
            >>> r1 = r.select('node',({'name': 'tutu'}))
            r1 = r2

            .. seealso:: correspond
            .. warning:: if both parameters props and block are given only props will be treated 
        """
        set = ResourceSet()
        if not props :
            set.properties = self.properties 
            for resource in self.resources :
                if not type or resource.type == type :
                    if block( resource ) :
                        set.resources.append( resource.copy() )
                        
                elif type != "resource_set" and isinstance(resource,ResourceSet) :
                    set.resources.append( resource.select( type, props , block) )
        else :
            set.properties = self.properties 
            for resource in self.resources :
                if not type or resource.type == type :
                    if resource.corresponds( props ) :
                        set.resources.append( resource.copy() )
                elif type != "resource_set" and isinstance(resource,ResourceSet) :
                    set.resources.append( resource.select( type, props ) )
        
        return set
    

    def delete_first(self,resource):
        """ delete the first resource equal to the parameters resource 
            return None if it has failed to found the resource

            :param resource: the resource which have to be deleted
            :type resource: ResourceSet or Resource


            :return: the resource or None if none found
            :rtype: Resource

        """
        for i in range(len(self.resources)) :
            if self.resources[i] == resource :
                self.resources.pop(i)
                return resource
            elif isinstance(self.resources[i],ResourceSet) :
                if self.resources[i].delete_first( resource ) :
                    return resource
        return None
        

    def delete_first_if(self,block=None):
            """ delete the first resource which return True with the given function in the block parameter
            return None if it has failed to found the resource

            :param block: function or lambda function which take a resource in parameter and return Boolean
            :type block: callable object


            :return: the resource or None if none found
            :rtype: Resource
            """
            for i in range(len(self.resources)) :
                if block(self.resources[i]) :
                    return self.resources.pop(i)
                elif isinstance(self.resources[i],ResourceSet) :
                    res = self.resources[i].delete_first_if( block )
                    if (res) :
                        return res
            return None
        

    def delete(self,resource):
            """ delete all resources equal to the parameters resource 
            return None if it has failed to found one

            :param resource: the resource which have to be deleted
            :type resource: ResourceSet or Resource


            :return: the last resource deleted or None if none found
            :rtype: Resource

            """
            res = None
            for i in range(len(self.resources)) :
                if self.resources[i] == resource :
                    self.resources.pop(i)
                    res = resource
                elif isinstance(self.resources[i],ResourceSet) :
                    #if self.resources[i].delete_all( resource ) :
                    if self.resources[i].delete( resource ) :
                        res = resource
            return res
        

    def delete_if(self,block=None):            
        """ delete all resource which return True with the given function in the block parameter
        return None if it has failed to found the resource

        :param block: function or lambda function which take a resource in parameter and return Boolean
        :type block: callable object


        :return: the last resource or None if none found
        :rtype: Resource
        """
        for i in range(len(self.resources)) :
            if block(self.resources[i]) :
                self.resources.pop(i)
            elif isinstance(self.resources[i],ResourceSet) :
                self.resources[i].delete_if( block )
        return self
        

    
    def flatten(self, type = None ):
        """Puts all the resource hierarchy into one ResourceSet.

        :param type:  the type of the object could be either "node"  or "Resource_set"
        :type type: string

        :return: the ResourceSet with all resource faltened
        :rtype: ResourceSet
        """
        set = ResourceSet()
        for resource in self.resources:
            if not type or resource.type == type :
                set.resources.append( resource.copy() )
                if isinstance(resource,ResourceSet) :
                    del set.resources[-1].resources[:]
            if isinstance(resource,ResourceSet) :
                set.resources.extend( resource.flatten(type).resources )
        return set
    

    def flatten_not (self,type = None ):
        """flatten the current resourceSet

        :param type:  the type of the object could be either "node"  or "Resource_set"
        :type type: string
        
        .. seealso:: flatten
        """
        set = self.flatten(type)
        self.resources = set.resources 
        return self
    


        # alias all flatten


    def each_slice( self,type = None, slice_step = 1, block=None):
        """ Creates groups of increasing size based on the slice_step paramater. 
            This goes until the size of the ResourceSet.

        :param type:  the type of the object could be either "node"  or "Resource_set"
        :param slice_step: int or function or lambda function which explicit the way how resources are browsed
        :param block: function or lambda function which will be call on every resource
        :type type: string
        :type slice_step: int or function
        :type block: callable object

        .. todo:: test this function
        .. note:: this kind of resource browsing stick more with ruby functionnality than python one because Bloc are limited in python
        """
        i = 1
        number = 0
        while True :
            resource_set = ResourceSet()
            it = ResourceSetIterator(self, type)
            #----is slice_step a block? if we call from
            #----each_slice_power2 : yes
            
            #if isinstance(slice_step,Proc) :
            if callable(slice_step):
                number = slice_step(i)

            elif isinstance(slice_step,list) :
                number = slice_step.shift.to_i
            else :
                number += slice_step
            if (number == 0):
                return None 
            for j in range(1,number) :
                resource = it.resource()
                if resource :
                        resource_set.resources.append( resource )
                else :
                    return None
                
                it.next()
            
            block( resource_set );
            i += 1
                 
        

    #Invokes the block for each set of power of two resources.
    def each_slice_power2(self, type = None, block=None ):
        """ Browse the resourceSet exponentialy . 
            This goes until the size of the ResourceSet.

        :param type:  the type of the object could be either "node"  or "Resource_set"
        :param block: function or lambda function which will be call on every resource
        :type type: string
        :type block: callable object

        .. todo:: test this function
        .. note:: this kind of resource browsing stick more with ruby functionnality than python one because Bloc are limited in python
        """
        self.each_slice( type, lambda i :  i*i , block )
        

    def each_slice_double( self,type = None, block=None ):
        """ Browse the resourceSet two per two . 
            This goes until the size of the ResourceSet.

        :param type:  the type of the object could be either "node"  or "Resource_set"
        :param block: function or lambda function which will be call on every resource
        :type type: string
        :type block: callable object

        .. todo:: test this function
        .. note:: this kind of resource browsing stick more with ruby functionnality than python one because Bloc are limited in python
        """
        self.each_slice( type, lambda i :  2**i , block )
    
    ## Fix Me  is the type really important , or were are going to deal always with nodes
    def each_slice_array( self,slices=1, block=None):
        self.each_slice( None,slices, block)
        

    #Calls block once for each element in self, depending on the type of resource.
    #if the type is :resource_set, it is going to iterate over the several resoruce sets defined.
    #:node it is the default type which iterates over all the resources defined in the resource set.
    #
    # ********************************
    #  deprecated 
    #  ********************************
    #   
    #def each( self,type = None, block=None ):
    #     it = ResourceSetIterator(self, type)
    #     while it.resource() :
    #         block( it.resource() )
    #         it.next()
    #         
    #         ************************************
            
    def each( self,type = None, block=None ):
        """ Browse the resourceSet  . 
            This goes until the size of the ResourceSet.

        :param type:  the type of the object could be either "node"  or "Resource_set"
        :param block: function or lambda function which will be call on every resource
        :type type: string
        :type block: callable object

        .. todo:: test this function
        .. note:: this kind of resource browsing stick more with ruby functionnality than python one because Bloc are limited in python 
                    prefer a \"for resource in ResourceSetIterator(self, "node") \"  to browse every node
        """
        for resource in ResourceSetIterator(self, type):
            block( resource )            

    def __len__(self):
        """Returns the number of node in the ResourceSet

            can be called the python way : len( resourceSet)

            :return:  the number of resources
            :rtype: Integer

        """
        count = 0 
        for resource in ResourceSetIterator(self, "node"):
            count +=1
        return count


    def __getitem__( self,index ):
        """Returns a subset of the ResourceSet.
            
        :param  index: [Range] Returns a subset specified by the range, [String] index Returns a subset which is belongs to the same cluster, [Integer] Returns just one resource   .
        
        :return: a ResourceSet object
        :rtype: ResourceSet     
        

        :Example: 
        
        >>> all[range(1,6)] #extract resources from 1 to 5
        >>> all["lyon"]  #extract the resources form lyon cluster
        >>> all[0] #return just one resource.

        .. note:: It can be used with a range(or int list) as a parameter or a string .
        .. warning:: Raise StopIteration if call with a wrong parameter or looking for an inexistant resource.
        """
        count=0
        resource_set = ResourceSet()
        #it = ResourceSetIterator()
        it = ResourceSetIterator(self,"node")
        if isinstance(index,list) : #Range
            for node in ResourceSetIterator(self,"node") :
                resource=it.resource()
                if resource :
                    if (count >= index[0] ) and (count <= index.max) :
                        resource_set.resources.apppend( resource )
                        count+=1
                        it.next()
            resource_set.properties=copy.deepcopy(self.properties)
            return resource_set

        if isinstance(index,str) :
            it = ResourceSetIterator(self,"resource_set")
            for resource in ResourceSetIterator(self,"resource_set") :
                if resource.properties["alias"] == index :
                    return resource

          #For this case a number is passed and we return a resource Object
        for resource in ResourceSetIterator(self,"node"): 
            #resource = it.resource()
            #if resource :
            if count==index :
                #resource_set.resources.push( resource )
                return resource
            count+=1
            #it.next()
        
        raise StopIteration #utile pour rendre Resource Set iterable 
        return  

        
    

    
    def to_resource(self)  :
        """
        Returns a resouce or an array of resources.
        
        :return: a resource or array of resources
        :rtype: Resource
        """
        if len(self) == 1 :
            #la boucle n'est pas necessaire mais cela est simmilaire au ruby avec un each
            for resource in ResourceSetIterator(self,"node"):
                return resource
        else :
            resource_list = []
            for resource in ResourceSetIterator(self,"node"):
                resource_list.append( resource )
            return resource_list
        
    
    def __eq__(self, set ):
        """
        test if current set are equal with parameter

        :param set: 
        :type set: ResourceSet or Resource

        :return: result of the test
        :rtype: boolean


        .. note:: can be called the python way with == 
        """

        if not super(ResourceSet, self).__eq__(set) or len(self.resources)!=len(set.resources) :
            return False

        for i in range(0,len(self.resources)-1) :
            if self.resources[i] != set.resources[i] :
                return False
        return True

    def __ne__(self, set ):
        """
        test if current set are non equal with parameter

        :param set: 
        :type set: ResourceSet or Resource

        :return: result of the test
        :rtype: boolean

        .. note:: can be call the python way with != 
        """
        return not (self==set)

    
    def eql( self, set ) :
        """
        Equality between to resoruce sets.

        :param set: 
        :type set: ResourceSet or Resource

        :return: result of the test
        :rtype: boolean
        """
        if not super(ResourceSet, self).__eq__(set) or len(self.resources)!=len(set.resources) :
            return False

        for i in range(1,len(self.resources)-1) :
            if not self.resources[i].eql(set.resources[i]) :
                return False

        return True

    # 
    def uniq(self):
        """
        Returns a ResourceSet with unique elements.

        :return: ResourceSet with unique elements
        :rtype: ResourceSet     
        """
        set = self.copy()
        return set.uniq_aux()
    

    def uniq_aux(self):
        """
        Returns same ResourceSet with unique elements.

        :return: same ResourceSet with unique elements
        :rtype: ResourceSet     
        """
        i = 0
        # while i < len(self.resources) -1 :
        for i in range(len(self.resources) -1):
            pos = []
            for j in range(i+1,len(self.resources)):
                if self.resources[i].eql(self.resources[j]) :
                    pos.append(j)
                      
            for p in reversed(pos):
                del (self.resources[p])
            
            # i += 1 

        for resource in self.resources :
            if isinstance(resource, ResourceSet):
                resource.uniq_aux()
 
        return self
        

    # Generates and return the path of the file which contains the list of the type of resource
    #specify by the argument type.

    # def resource_file( type=None, update=False ) :
    #     if (( not self.resource_files[type] ) or update) :

    #             self.resource_files[type] = Tempfile("#{type}")
    #             resource_set = self.flatten(type)
    #             resource_set.each { |resource|
    #                     self.resource_files[type].puts( resource.properties[:name] )
    #             }( not self.resource_files(type) ) or update
    #             self.resource_files[type].close
        
    #     return self.resource_files[type].path
        

    #Generates and return the path of the file which contains the list  of the nodes' hostnames. Sometimes it is handy to have it.
    #eg. Use it with mpi.    
    #def node_file( update=False ):
    #    resource_file( "node", update )
        




    #alias nodefile node_file
    


    def make_taktuk_command(self,cmd):
        """Creates the taktuk command

        Creates the taktuk command to execute on the ResourceSet
        It takes into account if the resources are grouped under
        different gatways in order to perform this execution more
        efficiently.

        ..todo:: verify this function
        """
        str_cmd = ""
        #pd : separation resource set/noeuds
        if self.gw != "localhost" :
            sets =False
            sets_cmd = ""
            for resource in self.resources:
               if isinstance(resource,ResourceSet) :
                   sets = True
                   
               sets_cmd += resource.make_taktuk_command(cmd)
            if sets :
                str_cmd += " -m "+ self.gw() +"-[ " + sets_cmd + " -]" 
            nodes = False
            nodes_cmd = ""
            
            for resource in self.resources:
                if resource.type == "node" :
                    nodes = True
                    nodes_cmd += resource.make_taktuk_command(cmd)
            if nodes :
                str_cmd += " -l "+  self.gw_ssh_user() +" -m "+ self.gw()+" -[ -l "+self.ssh_user()+" " + nodes_cmd + " downcast exec [ "+cmd+" ] -]" 
        else :
            nodes = False
            nodes_cmd = ""
            first = ""
            for resource in self.resources :
                if resource.type == "node" :
                    if not nodes :   
                        first = resource.name 
                    nodes = True
                    nodes_cmd += resource.make_taktuk_command(cmd)
            
            print (" results of the command "+nodes_cmd )
            if nodes :
                str_cmd += " -l "+ self.gw_ssh_user()+" -m "+ first +" -[ " + nodes_cmd + " downcast exec [ "+cmd+" ] -]" 
                sets = False
                sets_cmd = ""

                for resource in self.resources :
                    if isinstance(resource,ResourceSet) :
                        sets = True
                        sets_cmd += resource.make_taktuk_command(cmd)
                if sets :
                        if nodes : 
                                str_cmd += " -m "+first + " -[ " + sets_cmd + " -]"
                        else:
                                str_cmd += sets_cmd
        return str_cmd


    def hosts(self) :
        """
            try to convert the resourceSet as a list of execo host
            use the properties : gateway, user, keyfile and port
            default gateway is localhost.

            :return: a list of execo Host
            :rtype: list of execo.Host
        """
        hostlist = list()
        for r in self :
            if (r.type=='node') :
                hostlist.append(r.host())

        return hostlist
        
class ResourceSetIterator:
        """
            Class ResourceSet heret from Resource
        
            it will look in every resourceSet contained in the initial resourceSet
            usefull to make a resourceSet iterable see example 
    
            Attributes: 
                current : index for the '(<current element 
                iterator : a resourceSet element to browset element from a sub resourceSet 
                resource_set: initial resoureSet
                type : type of the init resourceSet
    
    
            :Example:
    
            >>> from resourceSet import *
            >>> resource_set = parser_xml("resourceSet.xml")
            >>> for i in ResourceSetIterator(resource_set :
            >>>     print i 
            node1
            node2
            node3
            node4
    
    
        """

        def __init__(self, resource_set, type=None):
            """ Creates a new Resource Object.


                :param resource_set:  resourceset on which the iterator will be created 
                :param typ: the type of the object could be "node"  or "Resource_set"
                :type resource_set: dict
                :type typ: string

                :return: Resource Object
                :rtype: Resource

                .. note:: if no type are given it will give every kind of object contained

            """

            self.resource_set = resource_set
            self.iterator = None
            self.type = type
            self.current = 0
            self.debut = True 
            for i in range(len(resource_set.resources)) :
                if self.type == self.resource_set.resources[i].type :
                    self.current = i
                    return 
                elif isinstance(self.resource_set.resources[i],ResourceSet) :
                    self.iterator = ResourceSetIterator(self.resource_set.resources[i], self.type)
                    if self.iterator.resource :
                        self.current = i
                        if i!= 0 :
                            self.debut = False
                        return
                    else :
                        self.iterator = None
                            
                elif not self.type :
                    self.current = i
                    if i!= 0 :
                        self.debut = False
                    return
            self.current = len(self.resource_set.resources)
        
        def resource(self):
            """ Give the current resource 

                :return: the current resource
                :rtype: resource of the same type as the attributes type
                
            """
            if( self.current > len( self.resource_set.resources) ):
                return None 
            if self.iterator :
                res = self.iterator.resource()

            else :
                res = self.resource_set.resources[self.current]
            
            return res
        

        def next(self):
            """
            place the index current on the next element and return it 
            
            :return: the next resource
            :rtype: resource of the same type as the attributes type 

            :Example:

            it = ResouceSetIterator(resource_set,"node")
            try :
            it.next()
            except StopIteration :
            ...

            .. warning:: Raise a Stopiteration at the end
            """
            res = None
            if not self.iterator and not self.debut  :
                self.current += 1
            while not res and self.current < len(self.resource_set.resources) : 
                if self.iterator :
                        try :
                            res =self.iterator.next()
                        except StopIteration :
                            self.iterator = None
                            self.current += 1
                        self.debut = False
                        
                elif self.type == self.resource_set.resources[self.current].type :
                        res = self.resource_set.resources[self.current]
                        if self.type == "resource_set" :
                            self.iterator = ResourceSetIterator(self.resource_set.resources[self.current], self.type)


                        self.debut = False
                elif isinstance(self.resource_set.resources[self.current],ResourceSet) :
                        self.iterator = ResourceSetIterator(self.resource_set.resources[self.current], self.type)
                        try :
                            res =self.iterator.next()
                        except StopIteration :
                            self.iterator = None
                            self.current += 1
                            
                        self.debut = False
                elif not self.type :
                        res = self.resource_set.resources[self.current]
                        self.debut= False
                else:
                        self.current += 1
                    
            if not res:
                self.current = 0
                raise StopIteration
                return None 
            return res
                    
        def __iter__(self):
            """ method to make ResourceSetIterator iterable
            """
            return self




def res_from_xml(tree):
    """function for xml parsing which return a Resource
            
        :param tree: tree created with element tree
        :type tree:  ElementTree

        :return:  Resource creatinf
        :rtype: Resource
    """
    name = None

    d_prop= dict()
    for child in tree :
        #print child.tag
        if child.tag == "properties":
            n_prop = child
        if child.tag =="type":
            type =  child.text
        
    for child in n_prop :
       d_prop[child.tag] = child.text
       if child.tag == "name":
           name = child.text
    
    res = Resource(type,prop=d_prop,name=name)

    return res 


def RS_from_xml(tree):
    """function for xml parsing which return a ResourceSet
            
        :param tree: tree is a node of a resourceSet 
        :type tree:  ElementTree

        :return:  Resource creatinf
        :rtype: ResourceSet
    """
    resource_set = ResourceSet()
    
    for child in tree :
        if child.tag == "properties":
            n_prop = child
        elif child.tag == "resources":
            n_resources = child            
            
        elif child.tag =="type"  :
            resource_set.type = child.text
            
    for child in n_prop :
       resource_set.properties[child.tag] = child.text
       if child.tag == "name":
           resource_set.name = child.text
           
    for child in n_resources :
        if child.tag == "Resource":
            resource_set.append(res_from_xml(child))
        elif child.tag =="ResourceSet":
            resource_set.append(RS_from_xml(child))

    return resource_set

def parser_xml(path):
    """function to creat a ResrouceSet from an xml file 

    :param path: the path of the xml file
    :type path: string
    
    :return: the ResourceSet created
    :rtype: ResourceSet


    :Example:

    >>> parser_xml('xml/rs1.xml')
     <resourceSet.Resource object at .... >

    """
    tree = ET.parse(path) #'xml/rs1.xml'
    root = tree.getroot()
    return (RS_from_xml(root))


#***********************************************
#### function to create xml from a resource_set :


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
        function taken from the site : https://pymotw.com/2/xml/etree/ElementTree/create.html
    """
    
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def R_toxml(r):
    """function for parsing node into a xml 
            
        :param r: Resource
        :type r:  Resource

        :return:  a node from Element tree
        :rtype: Element tree 
    """
    top = ET.Element('Resource')
    prop = ET.SubElement(top,"properties")
    
    for key,value in r.properties.items():
        c = ET.SubElement(prop, key)
        c.text = value
    
    n_t = ET.SubElement(top,"type")
    n_t.text = r.type
    
    return top 

def Rs_toxml(rs):
    """function for parsing node into a xml 
            
        :param r: ResourceSet
        :type r:  ResourceSet

        :return:  a node from Element tree
        :rtype: Element tree 
    """
    top = ET.Element('ResourceSet')
    prop = ET.SubElement(top,"properties")
    resource = ET.SubElement(top, "resources")
    for key,value in rs.properties.items():
        c = ET.SubElement(prop, key)
        c.text = value
    
    resources = []
    for res in rs.resources :
        if isinstance(res,ResourceSet):
            resources.append(Rs_toxml(res))
            
        elif isinstance(res,Resource):
            resources.append(R_toxml(res))
    
    resource.extend(resources)    
    
    n_t = ET.SubElement(top,"type")
    n_t.text = rs.type
    
    return top

def xml_writer(r):
    """function to create xml data from a node 

    :param r: ResrouceSet
    :type r: ResrousceSEt
    
    :return: the xml created

    """
    return prettify(Rs_toxml(r))



