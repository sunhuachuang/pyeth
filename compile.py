import json
from solc import compile_files

from os import listdir
from os.path import isfile, join

source_path = "./src"
abi_path = "./abi"

onlyfiles = [f for f in listdir(source_path) if isfile(join(source_path, f))]

for name in onlyfiles:
    file_path = source_path + "/" + name
    file_abi_path = abi_path + "/" + name.replace(".sol", ".json")

    compiled_sol = compile_files([file_path])
    contract_interface = compiled_sol["{}:Token".format(file_path)]

    with open(file_abi_path, "w+") as f:
        f.write(json.dumps(contract_interface['abi']))
        print("compile {} abi ok ".format(name))
