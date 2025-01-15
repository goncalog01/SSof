#! /usr/bin/env python3
import argparse
import json
import os

import analyser
import php_ast
from visitors import TypeChecker

parser = argparse.ArgumentParser()
parser.add_argument("slice_path", type=str, help="The path to the slice")
parser.add_argument("pattern_path", type=str, help="The path to the pattern")
parser.add_argument("--loop-depth",
                    type=int,
                    default=2,
                    help="The depth for loops")
parser.add_argument("--stdout",
                    action="store_true",
                    help="Output to stdout instead of a file")


class DummyArgs:

    def __init__(self, slice_path, pattern_path, loop_depth, stdout=False):
        self.slice_path = slice_path
        self.pattern_path = pattern_path
        self.loop_depth = loop_depth
        self.stdout = stdout


if __name__ == "__main__":
    if os.environ.get("DEBUG"):
        args = DummyArgs("./T06-01/program.json",
                         "./T06-01/patterns.json", 5, False)
    else:
        args = parser.parse_args()

    ast_json = None
    with open(args.slice_path) as f:
        ast_json = json.load(f)
    assert ast_json is not None

    pattern_json = None
    with open(args.pattern_path) as f:
        pattern_json = json.load(f)
    assert pattern_json is not None

    ast = php_ast.AstNode.make_program_node(ast_json)

    vulnerabilities = []

    for pattern in pattern_json:
        type_checker = TypeChecker(args.loop_depth)
        ast.accept(type_checker)
        vulnerabilities.extend(
        analyser.find_vulnerabilities(pattern, type_checker.states,
                                          args.loop_depth))

    vulnerabilities = list(
        {
            "vulnerability": el.vulnerability,
            "source": el.source,
            "sink": el.sink,
            "unsanitized flows": el.unsanitized_flows,
            "sanitized flows": list(list(ul) for ul in el.sanitized_flows)
        } for el in vulnerabilities)

    if not args.stdout:
        output_path = args.slice_path.split('/')[-1].split('.')[0]
        try:
            os.mkdir("./output")
        except FileExistsError:
            pass
        with open(f"./output/{output_path}.output.json", "w+") as f:
            f.write(json.dumps(vulnerabilities, indent=4))
    else:
            print(json.dumps(vulnerabilities, indent=4))
