from OpenGL import GL


class VAOError(Exception):
    pass


class ArrayBuffer:
    """Container for a vbo with additional information"""
    def __init__(self, format, vbo):
        self.format = format
        self.vbo = vbo
        self.stride = 0

    @property
    def target(self):
        """GL_ARRAY_BUFFER, GL_ELEMENT_ARRAY_BUFFER etc"""
        return self.vbo.target

    @property
    def usage(self):
        """GL_DYNAMIC_DRAW / GL_STATIC_DRAW"""
        return self.usage

    @property
    def size(self):
        return self.vbo.size

    @property
    def vertices(self):
        if self.size % self.stride != 0:
            raise VAOError("size % stride != 0")
        return self.size // self.stride


class ArrayMapping:
    """Keeps track of vbo to attribute mapping"""
    def __init__(self, array_buffer, attrib_name, components, offset):
        self.array_buffer = array_buffer
        self.attrib_name = attrib_name
        self.components = components
        self.offset = offset


class VAOCombo:
    """VAO of a specific attribute configuration"""
    def __init__(self, key):
        self.vao = GL.glGenVertexArrays(1)
        self.key = key
        self.array_mapping_list = []
        self.array_mapping_map = {}

    def bind(self):
        # FIXME: Bind counter
        # FIXME: Track currently bound VAO to avoid re-binding
        GL.glBindVertexArray(self.vao)

    def add_array_mapping(self, mapping):
        """Add ArrayMappings relevant to this VAO version"""
        self.array_mapping_list.append(mapping)
        self.array_mapping_map[mapping.attrib_name] = mapping


class VAO:
    """Vertex Array Object"""
    def __init__(self, name):
        self.name = name
        self.array_buffer_map = {}

        self.array_mapping = []
        self.array_mapping_map = {}

        self.element_buffer = None
        self.vertex_count = 0
        self.combos = {}

    def bind(self, shader):
        shader.bind()
        combo = self.generate_vao_combo(shader)
        combo.bind()

    def draw(self, mode=GL.GL_TRIANGLES):
        if self.element_buffer:
            raise NotImplemented
        GL.glDrawArrays(mode, 0, self.vertex_count)

    def add_array_buffer(self, format, vbo):
        self.array_buffer_map[id(vbo)] = ArrayBuffer(format, vbo)

    def set_element_buffer(self, format, vbo):
        # GL_ELEMENT_ARRAY_BUFFER, GL_UNSIGNED_INT
        self.element_buffer = ArrayBuffer(format, vbo)

    def map_buffer(self, vbo, attrib_name, components):
        """
        Map parts of the vbo to an attribute name
        :param vbo: The vbo
        :param attrib_name: Name of the attribute in the shader
        :param components: Number of components (for example 3 for a x, y, x position)
        """
        ab = self.array_buffer_map[id(vbo)]

        # FIXME: Determine byte size based on data type in VBO
        offset = ab.stride
        ab.stride += components * 4
        am = ArrayMapping(ab, attrib_name, components, offset)

        self.array_mapping.append(am)
        self.array_mapping_map[attrib_name] = am

    def build(self):
        """Finalize the VAO"""
        if len(self.array_buffer_map) == 0:
            raise VAOError("VAO has no buffers")

        for key, buff in self.array_buffer_map.items():
            if buff.stride == 0:
                raise VAOError("Buffer {} was never mapped in VAO {}".format(key, self.name))

        # Check that all buffers have the same number of elements
        last_vertices = -1
        for name, buf in self.array_buffer_map.items():
            vertices = buf.vertices
            if last_vertices > -1:
                if last_vertices != vertices:
                    raise VAOError("{} num_vertices {} != {}".format(name, last_vertices, vertices))

        self.vertex_count = vertices
        print("VAO {} has {} vertices".format(self.name, self.vertex_count))

    def generate_vao_combo(self, shader):
        """Create a VAO based on the shader's attribute specification."""
        # Return the combo if already generated
        combo = self.combos.get(shader.attribute_key)
        if combo:
            return combo

        print("Generating VAO Combo for {} using key {}".format(self.name, shader.attribute_key))
        combo = VAOCombo(shader.attribute_key)
        combo.bind()

        # Build the vao according to the shader's attribute specifications
        for attribute in shader.attribute_list:
            # Do we actually have an array mapping with this attribute name?
            mapping = self.array_mapping_map.get(attribute.name)
            if not mapping:
                raise VAOError("VAO {} don't know about the attribute '{}'".format(self.name, attribute.name))
            combo.add_array_mapping(mapping)

        # Do the data binding for this VAO: Order is the same as the attribList
        for i, mapping in enumerate(combo.array_mapping_list):
            print(" - > [{name}] loc {loc} components={comp} format={frmt} stride={stride} offset={offset}".format(
                name=shader.attribute_list[i].name,
                loc=shader.attribute_list[i].location,
                # vbo=mapping.array_buffer.vbo.buffers,
                comp=mapping.components,
                frmt=mapping.array_buffer.format,
                stride=mapping.array_buffer.stride,
                offset=mapping.offset,
            ))

            mapping.array_buffer.vbo.bind()
            GL.glEnableVertexAttribArray(shader.attribute_list[i].location)

            if mapping.array_buffer.format == GL.GL_FLOAT:
                GL.glVertexAttribPointer(shader.attribute_list[i].location,
                                         mapping.components,
                                         mapping.array_buffer.format,
                                         GL.GL_FALSE,
                                         mapping.array_buffer.stride,
                                         mapping.array_buffer.vbo + mapping.offset)
            else:
                raise VAOError("VAO class have not implemented array binding for {}".format(
                    mapping.array_buffer.format))

        self.combos[shader.attribute_key] = combo
        GL.glBindVertexArray(0)
        return combo
