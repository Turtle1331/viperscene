from typing import Dict, Union, Any

import wasmtime
import ctypes
import struct


class ScriptAsset:
    def __init__(self, path: str) -> None:
        self.path = path


class ScriptEnvironment:
    def __init__(self, asset: ScriptAsset) -> None:
        self.store = wasmtime.Store()
        self.module = wasmtime.Module.from_file(self.store.engine, asset.path)
        self.wasm_instance = wasmtime.Instance(self.store, self.module, [])

        self.wasm_setup = self.wasm_instance.exports["setup"]
        self.wasm_update = self.wasm_instance.exports["update"]

        raw_memory = self.wasm_instance.exports["memory"]
        self.memory_len = raw_memory.data_len
        self.memory_ctype = ctypes.c_ubyte * self.memory_len

        mem_as_array = ctypes.cast(
            raw_memory.data_ptr, ctypes.POINTER(self.memory_ctype)
        )[0]
        self.memory_view = memoryview(mem_as_array).cast("B")

    def f64_load(self, addr: int) -> float:
        assert 0 <= addr <= self.memory_len and addr % 8 == 0
        return struct.unpack_from("d", self.memory_view, addr)[0]

    def f64_store(self, addr: int, value: float) -> None:
        assert 0 <= addr <= self.memory_len and addr % 8 == 0
        struct.pack_into("d", self.memory_view, addr, float(value))


ComponentValues = Dict[str, Union[int, float]]


class ScriptInstance:
    def __init__(self, env: ScriptEnvironment) -> None:
        self.env = env
        self.data_len = self.env.memory_len

        self.memory_view = self.env.memory_view
        self.memory_copy = memoryview(self.env.memory_ctype()).cast("B")
        self.component_values: ComponentValues = {}

    def setup(self) -> None:
        self.env.wasm_setup()
        self.store_memory()
        self.store_component_values()

    def update(self, dt: float) -> None:
        # Load memory and writable component values
        self.load_memory()
        self.load_component_values()

        # Run the script instance
        self.env.wasm_update(dt)

        # Save memory and writable component values
        self.store_memory()
        self.store_component_values()

    def load_memory(self) -> None:
        self.memory_view[:] = self.memory_copy[:]

    def store_memory(self) -> None:
        self.memory_copy[:] = self.memory_view[:]

    def load_component_values(self) -> None:
        # Loading from instance, storing to Wasm
        self.env.f64_store(0, self.component_values["pos_x"])

    def store_component_values(self) -> None:
        # Loading from Wasm, storing to instance
        self.component_values["pos_x"] = self.env.f64_load(0)

    def get_component_values(self) -> ComponentValues:
        # Engine-facing call
        return self.component_values.copy()

    def set_component_values(self, comp_vals: ComponentValues) -> None:
        # Engine-facing call
        self.component_values.update(comp_vals)
