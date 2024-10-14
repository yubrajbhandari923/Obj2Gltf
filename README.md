# Obj2gltf
Small wrapper library over pygtlflib that helps you convert your obj files into gtlf format, for something like 3.js which prefer gltf format.

## Installation
```
pip install obj2gltf
```


## Usuage Guide
This script converts OBJ files to GLTF format. It can process a single file or an entire folder of OBJ files.
You can use it as command line tool, or import it to your own code.


### Basic Usage

```
python -m obj2gltf <obj_path> [options]
```

### Arguments

1. `obj_path` (required): Path to the OBJ file or folder containing OBJ files.

### Options

2. `--output`: Path to the output GLTF file or folder. If not specified, the output will be saved in the same location as the input with a .gltf extension.

3. `--exclude_list`: List of files to be excluded from processing. Useful when converting a folder of OBJ files.

4. `--colors`: List of RGB color values to be applied to the converted models.

### Examples

1. Convert a single OBJ file:
   ```
   python -m obj2gltf path/to/model.obj
   ```

2. Convert a single OBJ file with a specific output path:
   ```
   python -m obj2gltf path/to/model.obj --output path/to/output.gltf
   ```

3. Convert all OBJ files in a folder:
   ```
   python -m obj2gltf path/to/obj_folder
   ```

4. Convert all OBJ files in a folder, excluding specific files:
   ```
   python -m obj2gltf path/to/obj_folder --exclude_list "[file1.obj,file2.obj]"
   ```

5. Convert an OBJ file and apply a specific color:
   ```
   python -m obj2gltf path/to/model.obj --colors "[255,0,0]"
   ```

### Notes

- When using `--exclude_list` or `--colors`, enclose the list in square brackets and separate items with commas, without spaces.
- Color values should be integers between 0 and 255 for each RGB component.
- If processing a folder, the script will maintain the folder structure in the output.


### Alternative Usuage
Import the Obj2Gltf class to your own code.
```
from obj2gltf import Obj2Gltf
```


For any issues or further questions, please refer to the documentation or contact the developer.
