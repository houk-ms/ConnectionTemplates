## Get started

#### Code execution

To run the generator with codes

```cmd
cd ./src/azure_iac/
python ./command_azd.py <path-to-your-payload> <output-folder>
```

#### Binary execution

Run cmd below to build the generator, and it generates an executable in `dist/`.

```cmd
# cd root folder
pyinstaller installer.spec
```

To execute the generator

```cmd
./dist/generator.exe <path-to-your-payload> <output-folder>
```

#### Pakage execution

Run cmd below to package the generator, and it generates a package in `dist/`

```cmd
# cd root folder
python setup.py sdist bdist_wheel
```

Run cmd below to install the generator

```cmd
pip install .\dist\azure_iac-0.1-py3-none-any.whl
```

To execute generator through the package provide command

```cmd
azure_iac <path-to-your-payload> <output-folder>
```

To execute generator through package imports

```python
from azure_iac.command import Command

Command().execute('<path-to-your-payload>', '<path-to-your-payload>')
```
