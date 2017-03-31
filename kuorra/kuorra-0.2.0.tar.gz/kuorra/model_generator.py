import web
import os

class Model_generator:
    
    db_host = 'localhost'
    db_name = 'acme_store'
    db_user = 'root'
    db_pw = 'toor'

    table_name = ''

    db = web.database(
            dbn='mysql',
            host=db_host,
            db=db_name,
            user=db_user,
            pw=db_pw
            )

    def conectar(self):
        try:
            new_db = web.database(
            dbn='mysql',
            host=self.db_host,
            db=self.db_name,
            user=self.db_user,
            pw=self.db_pw
            )
            self.db = new_db
            print 'Conectado'
        except Exception as e:
            print e.args
            print "Error en conexion {}".format(e.message)

    def get_tables(self):
        try:
            return self.db.query('show tables')
        except Exception as e:
            print e.args
            print "Error en get_tables {}".format(e.message)
            return None


    def describre_tables(self,table):
        try:
            sql = 'describe {}'.format(table)
            return self.db.query(sql, vars=locals())
        except Exception as e:
            print e.args
            print "Error en describre_tables {}".format(e.message)
            return None


    def get_fields(self,table):
        try:
            result = self.describre_tables(table)
            fields = []
            for i in result:
                r = [i.Field, i.Key]
                fields.append(r)
            return fields
        except Exception as e:
            print e.args
            print "Error en get_fields {}".format(e.message)
            return None


    def get_primary_key(self,fields):
        primary_key = ''
        for field in fields:
            try:
                if field[1] == 'PRI':
                    primary_key = field[0]
                    exit
            except:
                primary_key = None
        return primary_key


    def super_cool(self,table_name):
        try:
            primary_key = self.get_primary_key(self.get_fields(table_name))

            fields = ""
            for field in self.get_fields(table_name)[1:]:
                fields += field[0] + ','
            fields = fields[:-1]

            values = ""
            for field in self.get_fields(table_name)[1:]:
                values += field[0] + '=' + field[0] + ',\n'
            values = values[:-2]

            fields_all = ""
            for field in self.get_fields(table_name):
                fields_all += field[0] + ','
            fields_all = fields_all[:-1]

            values_all = ""
            for field in self.get_fields(table_name):
                values_all += field[0] + '=' + field[0] + ',\n'
            values_all = values_all[:-2]

                    
                    
            script_path = os.path.abspath(__file__)
            script_dir = os.path.split(script_path)[0]
            rel_path = "plugin"
            abs_file_path = os.path.join(script_dir, rel_path)
            
            file = open(abs_file_path+'/model_master.py','r')
            plantilla = ''
            for line in file:
                plantilla += line


            plantilla = plantilla.replace('table_name', table_name)
            plantilla = plantilla.replace('primary_key', primary_key)
            plantilla = plantilla.replace('fields', fields)
            plantilla = plantilla.replace('values', values)
            plantilla = plantilla.replace('fields_all', fields_all)
            plantilla = plantilla.replace('values_all', values_all)


            model = plantilla

            file = open('model_' + table_name + '.py', 'w')
            file.write(model)
            file.close()
        except Exception as e:
            print e.args
            print "Error en supercool {}".format(e.message)


    def generate(self):
        try:
            for i in self.get_tables():
                m = str(i.values())
                print m[3:-2]
                self.super_cool(m[3:-2])
        except Exception as e:
            print "Error en generate {}".format(e.message)
