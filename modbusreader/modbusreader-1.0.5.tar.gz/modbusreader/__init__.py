import os
import modbusreader.structutils
import logging
import json
from jsonschema import validate
from pymodbus3.client.sync import ModbusTcpClient
from math import acos, asin, atan, atan2, ceil, cos, cosh, degrees, e, exp, fabs, floor, fmod, frexp, hypot, ldexp, \
    log, log10, modf, pi, pow, radians, sin, sinh, sqrt, tan, tanh


__version__ = '1.0.5'

__author__ = "Stephan Müller"
__copyright__ = "2017, Stephan Müller"
__license__ = "MIT"

__dirname__ = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger(__name__)

_safe_math_functions = dict([(k, locals().get(k, None)) for k in
                             ['math', 'acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'degrees', 'e', 'exp',
                              'fabs', 'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow',
                              'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh']
                             ])
_safe_math_functions['abs'] = abs


class ModbusReader:
    """ModbusReader is an automated modbus client which reads all discretes and registers of a modbus server over TCP
    """

    def __init__(self, host, port, unit, modbus_device_definition, float_low_byte_first=False):
        """
        Initializes a new instance
        
        :param host: host of modbus server
        :type host: str
        :param port: port of modbus server
        :type port: int
        :param unit: unit id
        :type unit: int
        :param modbus_device_definition: modbus device definition python dictionary or file name based on
                config `https://github.com/smueller18/modbus-readermodbusreader/modbus_definition.config.json`
        :type modbus_device_definition: dict or str
        :param float_low_byte_first: Because modbus float datatype consists of two integer bytes, there are 2
                possibilities for the determination of the float value. Set to True if float interpretation order is
                Low Byte and then High Byte. Otherwise interpretation order is High Byte and then Low Byte.
        :type float_low_byte_first: bool
        
        :raise ~jsonschema.exceptions.ValidationError: if the modbus device definition dictionary or file is invalid
        :raise ~jsonschema.exceptions.SchemaError: if the modbus device definition config itself is invalid
        """
        self._modbus_device_definition_schema_file = __dirname__ + "/modbus_definition.schema.json"
        self.host = host
        self.port = port
        self.unit = unit
        self.float_low_byte_first = float_low_byte_first

        if type(modbus_device_definition) is not dict:
            modbus_device_definition = json.loads(open(modbus_device_definition, 'rb').read().decode("UTF-8"))

        validate(modbus_device_definition,
                 json.loads(open(self._modbus_device_definition_schema_file, 'rb').read().decode("UTF-8")))

        self.grouped_modbus_device_definition = self.group_modbus_device_definition(modbus_device_definition)
        self.client = ModbusTcpClient(host=self.host, port=self.port)

    @staticmethod
    def group_modbus_device_definition(modbus_device_definition):
        """
        Groups modbus addresses. This method is needed, if there are gaps of non existent modbus addresses.
        
        :param modbus_device_definition: modbus device definition dictionary
        :type modbus_device_definition: dict
        
        :return: grouped modbus device definition dictionary
        :type: dict
        """

        grouped_sensors = dict()

        for function_type in ["discrete_inputs", "discrete_outputs", "input_registers", "output_registers"]:

            grouped_sensors.update({function_type: list()})

            config_sensors = modbus_device_definition[function_type]
            sorted_sensors = sorted(config_sensors.items(), key=lambda k: config_sensors[k[0]]['address'])

            if function_type.startswith("discrete"):
                start_address = None
                last_address = None
                sensors = dict()

                for i in range(0, len(sorted_sensors)):
                    sensor_id = sorted_sensors[i][0]
                    sensor_config = sorted_sensors[i][1]

                    current_address = sorted_sensors[i][1]["address"]
                    if i < len(sorted_sensors) - 1:
                        next_address = sorted_sensors[i + 1][1]["address"]
                    else:
                        next_address = None

                    if start_address is None:
                        start_address = current_address

                    if last_address is None or last_address + 1 == current_address:
                        sensors.update({sensor_id: sensor_config})
                        last_address = current_address

                    if next_address is None or current_address + 1 != next_address:
                        grouped_sensors[function_type].append(
                            {
                                "start_address": start_address,
                                "count": current_address - start_address + 1,
                                "sensors": sensors
                            })
                        sensors = dict()
                        start_address = None
                        last_address = None

            if function_type.endswith("registers"):
                start_address = None
                last_address = None
                last_count = None
                sensors = dict()

                for i in range(0, len(sorted_sensors)):
                    sensor_id = sorted_sensors[i][0]
                    sensor_config = sorted_sensors[i][1]
                    sensor_config.update({"count": int(structutils.calcsize(sorted_sensors[i][1]["type"]) / 2)})

                    current_address = sorted_sensors[i][1]["address"]
                    if i < len(sorted_sensors) - 1:
                        next_address = sorted_sensors[i + 1][1]["address"]
                    else:
                        next_address = None

                    if start_address is None:
                        start_address = current_address

                    if last_address is None or last_address + last_count == current_address:
                        sensor_config.update({"count": sensor_config["count"]})
                        sensors.update({sensor_id: sensor_config})
                        last_address = current_address
                        last_count = sensor_config["count"]

                    if next_address is None or current_address + sensor_config["count"] != next_address:
                        grouped_sensors[function_type].append(
                            {
                                "start_address": start_address,
                                "count": current_address + sensor_config["count"] - start_address,
                                "sensors": sensors
                            })
                        sensors = dict()
                        start_address = None
                        last_address = None
                        last_count = None

        return grouped_sensors

    def read_discretes(self, discrete_type):
        """
        read either discrete inputs or outputs
        
        :param discrete_type: type of discrete. either 'input' or 'output'
        :type discrete_type: str
        
        :return: discrete values: { sensor_id: sensor_value,  ... }
        :type: dict
        
        :raise AttributeError: is raised if discrete_type doesn't match required types
        :raise IOError: is raised if reading discretes over TCP connection fails
        """

        if discrete_type != "input" and discrete_type != "output":
            raise AttributeError("discrete type has to be either 'input' or 'output'")

        sensor_readings = dict()

        discretes = self.grouped_modbus_device_definition["discrete_" + discrete_type + "s"]
        if len(discretes) == 0:
            return sensor_readings

        for i in range(0, len(discretes)):
            results = None
            if discrete_type == "input":
                results = self.client.read_discrete_inputs(unit=self.unit, address=discretes[i]["start_address"],
                                                           count=discretes[i]["count"])
            if discrete_type == "output":
                results = self.client.read_coils(unit=self.unit, address=discretes[i]["start_address"],
                                                 count=discretes[i]["count"])
            try:
                for sensor_id in discretes[i]["sensors"]:
                    position = discretes[i]["sensors"][sensor_id]["address"] - discretes[i]["start_address"]
                    sensor_readings.update({sensor_id: results.bits[position]})

            except AttributeError:
                raise IOError("reading discrete " + discrete_type + "s failed")

        return sensor_readings

    def read_registers(self, register_type):
        """
        read either input or output registers
        
        :param register_type: type of register. either 'input' or 'output'
        :type register_type: str
        :return: discrete output values as follows: { sensor_id: sensor_value, ... }
        :type: dict
        
        :raise AttributeError: If register_type doesn't match required types
        :raise IOError: If reading registers over TCP connection fails
        """

        if register_type != "input" and register_type != "output":
            raise AttributeError("register type has to be either 'input' or 'output'")

        sensor_readings = dict()

        registers = self.grouped_modbus_device_definition[register_type + "_registers"]
        if len(registers) == 0:
            return sensor_readings

        for i in range(0, len(registers)):
            results = None
            if register_type == "input":
                results = self.client.read_input_registers(unit=self.unit, address=registers[i]["start_address"],
                                                           count=registers[i]["count"])
            if register_type == "output":
                results = self.client.read_holding_registers(unit=self.unit, address=registers[i]["start_address"],
                                                             count=registers[i]["count"])
            for sensor_id in registers[i]["sensors"]:
                try:
                    register = registers[i]["sensors"][sensor_id]

                    position_start = register["address"] - registers[i]["start_address"]
                    position_end = position_start + register["count"]

                    if register["type"] == "float" and self.float_low_byte_first:
                        byte_list = structutils.int16list_to_bytes(results.registers[position_start:position_end][::-1])
                    else:
                        byte_list = structutils.int16list_to_bytes(results.registers[position_start:position_end])
                    sensor_raw_value = structutils.bytes_to_datatype(byte_list, register["type"])

                    sensor_value = sensor_raw_value * register["factor"]

                    if "error_correction" in register:
                        try:
                            _safe_math_functions['x'] = sensor_value
                            sensor_value = float(eval(register["error_correction"]["equation"],
                                                      {"__builtins__": None},
                                                      _safe_math_functions))
                        except Exception as ex:
                            logger.warning("Error correction failed for sensor id " + sensor_id +
                                           ". Using original value instead. Error details: " + str(ex))

                    if register["type"] in ["int16", "int32", "uint32"]:
                        sensor_value = round(sensor_value, int(1 / register["factor"]))

                    sensor_readings.update({
                        sensor_id: sensor_value
                    })

                except AttributeError:
                    raise IOError("reading " + register_type + " registers failed")

        return sensor_readings

    def read_discrete_outputs(self):
        """
        read discrete outputs
        
        :return: discrete output values as follows: { sensor_id: sensor_value, ... }
        :type: dict
        
        :raise IOError: is raised if reading discretes over TCP connection fails
        """
        return self.read_discretes("output")

    def read_discrete_inputs(self):
        """
        read discrete inputs
        
        :return: discrete output values as follows: { sensor_id: sensor_value, ... }
        :type: dict
        
        :raise IOError: is raised if reading discretes over TCP connection fails
        """
        return self.read_discretes("input")

    def read_output_registers(self):
        """
        read output registers
        
        :return: discrete output values as follows: { sensor_id: sensor_value, ... }
        :type: dict
        
        :raise IOError: is raised if reading registers over TCP connection fails
        """
        return self.read_registers("output")

    def read_input_registers(self):
        """
        read input registers
        
        :return: discrete output values as follows: { sensor_id: sensor_value, ... }
        :type: dict
        
        :raise IOError: is raised if reading registers over TCP connection fails
        """
        return self.read_registers("input")

    def read_all_values(self):
        """
        read discretes and registers
        
        :return: discrete output values as follows: { sensor_id: sensor_value, ... }
        :type: dict
        
        :raise IOError: is raised if reading discretes or registers over TCP connection fails
        """
        sensor_readings = dict()
        try:
            sensor_readings.update(self.read_discrete_inputs())
            sensor_readings.update(self.read_discrete_outputs())
            sensor_readings.update(self.read_input_registers())
            sensor_readings.update(self.read_output_registers())
        except IOError as io_error:
            raise io_error

        return sensor_readings
