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

        raw_memory = self.wasm_instance.exports["memory"]
        self.memory_len = raw_memory.data_len
        self.memory_ctype = ctypes.c_ubyte * self.memory_len

        mem_as_array = ctypes.cast(raw_memory.data_ptr, ctypes.POINTER(self.memory_ctype))[0]
        self.memory_view = memoryview(mem_as_array).cast("B")

    def f64_load(self, addr):
        assert 0 <= addr <= self.memory_len and addr % 8 == 0
        return struct.unpack_from("d", self.memory_view, addr)[0]

    def f64_store(self, addr, value):
        assert 0 <= addr <= self.memory_len and addr % 8 == 0
        struct.pack_into("d", self.memory_view, addr, float(value))


class ScriptInstance(object):
    def __init__(self, env):
        self.env = env
        self.data_len = self.env.memory_len

        
        self.memory_view = self.env.memory_view
        self.memory_copy = memoryview(self.env.memory_ctype()).cast("B")
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
        self.memory_view[:] = self.memory_copy[:]

    def store_memory(self):
        self.memory_copy[:] = self.memory_view[:]

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
