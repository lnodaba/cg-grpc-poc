
# gRPC Server Setup

## Prerequisites

- Ensure you have `Poetry` installed for managing dependencies. If not, you can install it by following the instructions [here](https://python-poetry.org/docs/#installation).
- Make sure you have Python 3.8+ installed.

## Installation

1. Navigate to the `server/` directory:

   ```bash
   cd server/
   ```

2. Lock dependencies without updating:

   ```bash
   poetry lock --no-update
   ```

3. Install the dependencies:

   ```bash
   poetry install
   ```

## Running the Server

To start the gRPC server, use the following command:

```bash
poetry run python app/main.py
```

This will start the gRPC server located in `app/main.py`.


# gRPC Setup and Code Generation

This project uses `grpcio-tools` to generate Python gRPC code from `.proto` files.

### Prerequisites

Make sure you have `grpcio-tools` installed. You can install it via pip:

```bash
pip install grpcio-tools
```

### Generating Python Code from `.proto` Files

To generate the Python classes and gRPC stubs from the `.proto` files, run the following command:

```bash
python -m grpc_tools.protoc --proto_path=./app/services/proto --python_out=./app/services/proto --grpc_python_out=./app/services/proto ./app/services/proto/acronyms.proto


python -m grpc_tools.protoc --proto_path=./app/services/proto --python_out=./app/services/proto --grpc_python_out=./app/services/proto ./app/services/proto/acronyms.proto

python -m grpc_tools.protoc --proto_path=./app/services/proto --python_out=./app/services/proto --grpc_python_out=./app/services/proto --proto_path=./app/services/proto ./app/services/proto/*.proto

```

### Explanation

- `--proto_path=./app/services/proto`: Specifies the directory where your `.proto` files are located.
- `--python_out=./app/services/proto`: Defines the output directory for the generated Python files (for messages and services).
- `--grpc_python_out=./app/services/proto`: Specifies the directory where the gRPC-specific Python code will be placed.
- `./app/services/proto/acronyms.proto`: The actual `.proto` file you want to compile.

### Notes

- Ensure the `.proto` file exists in the specified path (`./app/services/proto/acronyms.proto`).
- After running the command, the generated files will be available in the specified output directories.
- You can modify the paths to suit your project structure as needed.


### Error: `ModuleNotFoundError: No module named 'acronyms_pb2'`

If the following error occurs:
```bash
ModuleNotFoundError: No module named 'acronyms_pb2'
```

Change the import in the `acronyms_pb2_grpc.py` file:

#### Before:
```python
import acronyms_pb2 as acronyms__pb2
```

#### After:
```python
from . import acronyms_pb2 as acronyms__pb2
```
