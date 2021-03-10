import wasmtime
import ctypes
import struct


class ScriptAsset(object):
    def __init__(self, path):
        self.path = path


class ScriptEnvironment(object):
    def __init__(self, asset):
        self.store = wasmtime.Store()
        self.module = wasmtime.Module.from_file(self.store.engine, asset.path)
        self.wasm_instance = wasmtime.Instance(self.store, self.module, [])

        self.wasm_setup = self.wasm_instance.exports["setup"]
        self.wasm_update = self.wasm_instance.exports["update"]
        self.wasm_memory = self.wasm_instance.exports["memory"]

    def f64_load(self, addr):
        assert 0 <= addr <= self.wasm_memory.data_len and addr % 8 == 0
        raw_value = bytearray(self.wasm_memory.data_ptr[addr:addr+8])
        value = struct.unpack("d", raw_value)[0]
        return value

    def f64_store(self, addr, value):
        assert 0 <= addr <= self.wasm_memory.data_len and addr % 8 == 0
        raw_value = struct.pack("d", float(value))
        for i in range(8):
            self.wasm_memory.data_ptr[addr+i] = raw_value[i]


class ScriptInstance(object):
    def __init__(self, env):
        self.env = env
        self.data_len = self.env.wasm_memory.data_len

        mem_type = ctypes.c_char * self.data_len
        self.data_arr = ctypes.cast(self.env.wasm_memory.data_ptr, ctypes.POINTER(mem_type))[0]
        self.memory = mem_type()
        self.component_values = {}

    def setup(self):
        self.env.wasm_setup()
        self.store_memory()
        self.store_component_values()

    def update(self, dt):
        # Load memory and writable component values
        self.load_memory()
        self.load_component_values()

        # Run the script instance
        self.env.wasm_update(dt)

        # Save memory and writable component values
        self.store_memory()
        self.store_component_values()

    def load_memory(self):
        self.data_arr.contents = self.memory 

    def store_memory(self):
        self.memory.contents = self.data_arr

    def load_component_values(self):
        # Loading from instance, storing to Wasm
        self.env.f64_store(0, self.component_values["pos_x"])

    def store_component_values(self):
        # Loading from Wasm, storing to instance
        self.component_values["pos_x"] = self.env.f64_load(0)

    def get_component_values(self):
        # Engine-facing call
        return self.component_values.copy()
    
    def set_component_values(self, comp_vals):
        # Engine-facing call
        self.component_values.update(comp_vals)
