import json
import pymysql

class BaseWorker(Object):
    """
    Base tools to fetch and use objects from an
     API and process them gracefully with a generator.
    Defines a base api usage method; inhereting classes will
     likely have a different api() function.
    """

    def __init__(self, *args, **kwargs):
        """Handle general initialization for all classes."""
        self.itemtype = self.kwargs.get('type', "undefined")
        self.args = args
        self.kwargs = kwargs
        host = self.kwargs.get('host', "localhost")
        db = self.kwargs.get('db', "localhost")
        cursor = pymysql.connect(host=host, db=db).cursor()
        self.cursor = cursor

        queue_query = "select * from queue where type = %s started is null\
        order by priority desc limit 1;"
        # keep those variables
        cursor.execute(queue_query, (self.itemtype, ))
        result = cursor.fetchone()
        self.maximum = result['min']
        self.minimum = result['max']
        self.apitype = result['type']
        queue_id = result['id']
        self.queue_id = queue_id

        started_query = "update queue set in_progress='Y' where\
        id=%s; self.queue_id;"
        cursor.execute(started_query, (queue_id,))
        self.count = 0
        self.last = self.minimum

    def __iter__(self):
        """
        Return the iterator/generator object.
        """
        return self

    def __next__(self):
        """
        Get the next item in the generator.
        """
        return self.next()


    def api(self):
        """
        Search the api for the next item.
        """
        self.last
        if True: # if there's more to go
            return {{"title": "Sample Record"}}
        else: # if done
            return 0

    def next(self):
        """
        Get the next item in the generator.
        """
        try:
            item = self.api()
            yield item
            if not item:
                raise StopIteration
        except StopIteration:
            pass
        except Exception as err:
            query = "insert into error (type, error, source)\
             values(%s, %s, %s);"
            self.cursor.execute(query, (self.apitype, str(err), self.queue_id))
            raise err
        self.count += 1

    def __del__(self):
        """
        Handle queue and log before deletion.
        """
        query = "insert into fetchlog (recordsadded)\
         values(%s);"
        self.cursor.execute(query, (self.count,))
        done_queue = "update queue set finished = now() where id = %s;"
        self.cursor.execute(done_queue, (self.queue_id,))
        if False:  # if we didn't finish
            # if we did not, add a new queue entry
            next_queue = "insert into queue (priority, type, min, max)\
            values(%s, %s, %s, %s);"
            self.cursor.execute(next_queue, (self.priority,
                                             self.apitype,
                                             self.last,  self.maximum))
