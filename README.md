# viperscene
This is a simple ECS (entity-component-system) demonstration using WebAssembly component scripts, using the Wasmtime library for Python. It is intended as a prototype for managing WebAssembly instances in [Mondradiko](https://github.com/mondradiko/mondradiko).

### TODO
[ ] replace asserts with type hints and error handling
[ ] clean up the almost-too-tangled dependencies between the subdirectories
[ ] upgrade to a scene hierarchy using TransformComponent
[ ] add multiple entities to demonstrate component storage/loading
[ ] use a single Wasm instance per script asset 
[ ] revamp the bindings API to actually support dynamic component bindings
[ ] update memory storage and loading to only store changed regions
[ ] expand to a multiprocessing model for parallelism
[ ] experiment with instrumenting Wasm code to add callbacks on memory writes
[ ] experiment with Wasm static analysis to pinpoint memory writes at load time
[ ] experiment with sharing a page using instrumentation and bounds checking
