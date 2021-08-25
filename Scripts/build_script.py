#!/usr/bin/env python3.6

import json
import os
import sys
import shutil
import subprocess
from distutils.dir_util import copy_tree
from typing import Any, Dict

def copytree(src, dst, symlinks=False):
    if os.path.isdir(src):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.exists(d):
                try:
                    shutil.rmtree(d)
                except OSError:
                    os.unlink(d)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks)
            else:
                shutil.copy2(s, d)
    else:
        shutil.copy2(src, dst)

def runBuild() -> None:  # noqa C901
    # Xcode Environment
    arch = os.environ.get("ARCHS", default="")
    platform_name = os.environ.get("PLATFORM_NAME", default="")
    source_root = os.environ.get("SOURCE_ROOT", default="")
    wrapper_name = os.environ.get("WRAPPER_NAME")
    executable_name = os.environ.get("EXECUTABLE_NAME")
    executable_extension = os.environ.get("EXECUTABLE_EXTENSION")
    wrapper_extension = os.environ.get("WRAPPER_EXTENSION")
    if wrapper_extension is None:
        if executable_name is None:
            exit(0)
        wrapper_name = executable_name
    else:
        wrapper_extension = "app"

    # Buck Environment
    buck_cell_relative_path = os.environ.get("BUCK_CELL_RELATIVE_PATH")
    build_target = os.environ.get("BUILD_TARGET").replace("\/\/", "//")
    built_products_dir = os.environ.get("TARGET_BUILD_DIR", default="")
    target_name = os.environ.get("TARGET_NAME", default="")

    buck_cell_root = os.path.normpath(
        os.path.join(source_root, buck_cell_relative_path)
    )

    product_name = (
        wrapper_name
        if wrapper_name is not None and wrapper_name != ""
        else target_name + "." + wrapper_extension
    )
    path = os.path.join(built_products_dir, product_name)

    archs = arch.split(" ")
    if len(archs) > 1:
      archs.remove("arm64")
      archs = ",".join(archs)
      arch = archs

    build_target += "#" + platform_name + "-" + arch
    if executable_extension is not None and executable_extension == "a":
        build_target += ",static"
        
    build_command = ["./buck", "build", build_target] + [
        "--report-absolute-paths",
        "--show-output"
    ]
    print(build_command, file=sys.stderr)
    build_output = subprocess.check_output(build_command, encoding="utf-8")
    print(build_output, file=sys.stderr)
    print("Output:")
    print(build_output)
    cell_relative_path = os.path.join(
        "buck-out", build_output.split(" buck-out/")[-1].strip()
    )
    print(cell_relative_path)
    app = os.path.join(buck_cell_root, cell_relative_path)
    app = app.replace("Libraries/buck-out", "/buck-out")
    if not os.path.exists(app):
        print(
            f"error: {product_name} not found at expected path ({app}).",
            file=sys.stderr,
        )
        exit(1)
    
    copytree(app, path, symlinks=True)

    machine_log_path = os.path.join(
        buck_cell_root, "buck-out", "log", "last_buildcommand", "buck-machine-log"
    )
    machine_log_first_line = ""
    try:
        with open(machine_log_path, "r", encoding="utf-8") as fp:
            machine_log_first_line = fp.readline()
    except OSError:
        print("warning Buck machine log unable to be read for run.", file=sys.stderr)
    if machine_log_first_line != "":
        machine_log_json: Dict[str, Any] = {}
        try:
            machine_log_json = machine_log_first_line.split()[1]
        except IndexError:
            print("warning Buck machine log unable to be parsed", file=sys.stderr)
    print(path)
    print(app)

def touchDummyFiles():
  temp_dir = os.environ.get("TEMP_DIR", default="")
  native_arch = os.environ.get("NATIVE_ARCH")
  product_name = os.environ.get("PRODUCT_NAME")
  derived_data_native_arch_path = f'{temp_dir}/Objects-normal/{native_arch}/'

  print("Writing files...")
  os.makedirs(derived_data_native_arch_path, exist_ok=True)
  os.popen(f'mkdir -p {derived_data_native_arch_path}/ && touch {derived_data_native_arch_path}/{product_name}.swiftmodule')
  os.popen(f'touch -f {derived_data_native_arch_path}/{product_name}.swiftdoc')
  os.popen(f'touch -f {derived_data_native_arch_path}/{product_name}-Swift.h')
  os.popen(f'touch -f {derived_data_native_arch_path}/{product_name}-master.d')


runBuild()
touchDummyFiles()