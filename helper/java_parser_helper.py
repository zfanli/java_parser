"""
Java parser entry.
"""

import re
import json
import yaml
import hashlib
import datetime
import time
import logging

from functools import wraps
from pathlib import Path
from lark.exceptions import UnexpectedInput
from java_parser import create_parser, JavaTransformer
from helper.io_helper import save_to_file, search_files

__version__ = "0.2.4"
__author__ = "Richard Zeng"

IGNORE_LIST = [".git", "package-info.java"]

md5 = hashlib.md5()
logger = logging.getLogger("parser")
logger.setLevel(logging.DEBUG)
logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger.addHandler(logging.StreamHandler())


def log(message):
    """Logger"""

    def decorator_log(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Logging
            m = " ".join(
                [str(x) for x in [message, *args[1:], kwargs if kwargs else ""]]
            )
            logger.info(m)
            # Perform func
            return func(*args, **kwargs)

        return wrapper

    return decorator_log


remove_flag = False
pattern_inline = re.compile(r"/\*.*\*/")


def removecomment(content):
    global remove_flag
    # Remove inline comment
    content = re.sub(pattern_inline, "", content)
    result = ""
    # Remove multiple line comment and keep lineno
    for line in content.splitlines():
        # nonlocal flag
        if line.strip().startswith("/*"):
            line = ""
            remove_flag = True
        if line.strip().endswith("*/"):
            line = ""
            remove_flag = False
        if remove_flag:
            line = ""
        result += line + "\n"
    return result


class JavaParser:
    version = __version__

    @log("Java Parser initialized!")
    def __init__(self):

        # Initialize parser
        self._parser = create_parser()
        # Count files
        self._count = 0
        self._skip = 0
        self._success = 0
        # Initial variables
        self._output = None
        self._parsed = None
        self._destination = None
        self._target_dir = None
        self._error = None
        self._encoding = "utf-8"
        self._force_parse = False
        self._skip_condition = "md5"
        self._fileformat = "json"
        self._start_timestamp = time.time()
        self._comment_ignored = None

    @property
    def fileformat(self):
        """File format"""

        return self._fileformat

    @fileformat.setter
    def fileformat(self, format):
        """Set file format, `json` by default"""

        self._fileformat = format

    @property
    def force_parse(self):
        """Force parsing mode"""

        return self._force_parse

    @force_parse.setter
    def force_parse(self, force_parse):
        """Set file encoding"""

        self._force_parse = force_parse

    @property
    def skip_condition(self):
        """Skip condition"""

        return self._skip_condition

    @skip_condition.setter
    def skip_condition(self, skip_condition):
        """Set skip condition: 'md5' or 'exist' """

        self._skip_condition = skip_condition

    @property
    def encoding(self):
        """File encoding"""

        return self._encoding

    @encoding.setter
    def encoding(self, encoding):
        """Set file encoding"""

        self._encoding = encoding

    @property
    def target_dir(self):
        """Get target directory directory"""

        return self._target_dir

    @target_dir.setter
    @log("Set target directory: ")
    def target_dir(self, target_dir):
        """Set target directory directory"""

        path = Path(target_dir)
        if not path.exists():
            raise IOError("Target directory does not exist!")
        self._target_dir = target_dir

    @property
    def destination(self):
        """Get destination directory"""

        return self._destination

    @destination.setter
    @log("Set destination directory: ")
    def destination(self, destination):
        """Set destination directory"""

        try:
            path = Path(destination)
            if not path.exists():
                path.mkdir(parents=True)

            self._destination = destination
        except:
            self._destination = None

    @log("Save to file...\n")
    def to_file(self, filename):
        """Save output to file"""

        output = []

        if self._fileformat in ("yaml", "yml"):
            output.append(yaml.dump(self._output, default_flow_style=False))
        if self._fileformat in ("json"):
            output.append(
                json.dumps(self._output, indent=2, ensure_ascii=False, sort_keys=True)
            )

        for o in output:
            save_to_file(filename, o)

    @log("\nError occurred")
    def error(self, error, message, filename):
        """Print error and return false"""

        if self._error is None:
            self._error = []

        line = error.line if hasattr(error, "line") else None
        column = error.column if hasattr(error, "column") else None

        error = {
            "filename": ",".join([str(x) for x in [filename, line, column]]),
            "output": f"{message}:{str(filename)}\n{str(error)}",
        }

        self._error.append(error)

        return error

    @log("Parseing finished!")
    def finish(self):

        count = self._count
        failed = len(self._error) if self._error is not None else 0
        skip = self._skip
        success = self._success
        parsed_count = skip + success
        complete_ratio = "%.2f" % (((parsed_count - failed) / parsed_count) * 100)
        start_time = datetime.datetime.fromtimestamp(self._start_timestamp)
        timestamp = time.time()
        report = "\n"
        report += f"Total parsed: {count}\n"
        report += f"Complete: {success}\n"
        report += f"Complete Ratio: {complete_ratio}%\n"
        report += f"Skipped: {skip}\n"
        report += f"Failed: {failed}\n"
        report += f"Start time: {start_time}\n"
        report += f"Finished time: {datetime.datetime.now()}\n"
        report += f"Past: {int(timestamp - self._start_timestamp)}s\n"

        report_to_file = report
        if self._error is not None:
            not_parsed_list = ""
            for item in self._error:
                report_to_file += f'{item["output"]}\n'
                not_parsed_list += str(item["filename"]) + "\n"
            if self.destination:
                path = Path(self.destination)
                save_to_file(
                    path.joinpath(f"not_parsed_list_{timestamp}.txt"), not_parsed_list
                )

        # Save comment ignored list to file
        if self._comment_ignored is not None:
            comment_ignored_list = ""
            if self.destination:
                for item in self._comment_ignored:
                    comment_ignored_list += f"{str(item)}\n"
                    path = Path(self.destination)
                    save_to_file(
                        path.joinpath(f"comment_ignored_{timestamp}.txt"),
                        comment_ignored_list,
                    )

        # Save to file if destination is specified
        if self.destination:
            path = Path(self.destination)
            save_to_file(path.joinpath(f"result_{timestamp}.log"), report_to_file)
            # Save parsed file list
            if self._parsed:
                parsed = ""
                for f in self._parsed:
                    parsed += f + "\n"
                save_to_file(path.joinpath(f"parsed_{timestamp}.txt"), parsed)

        # Some clean up
        self._error = None
        self._parsed = None
        self._output = None

        return self.report(report)

    @log("\nReport:\n")
    def report(self, *message):
        pass

    @log("Skipped:")
    def skip(self, *message):
        self._skip += 1

    def is_parsed(self, target, name, md5):
        """Check if target is already parsed"""

        if self._destination is None:
            return False

        parsed_package = ""

        for line in target.splitlines():
            if "package" in line:
                parsed_package = line
                parsed_package = parsed_package.replace("package", "")
                parsed_package = parsed_package.replace(";", "")
                parsed_package = parsed_package.strip()
                break

        parsed_filename = f"{parsed_package}.{name.stem}.json"

        # Parsed file maybe in this path
        path = Path(self._destination).joinpath(parsed_filename)

        if path.exists():

            if self._skip_condition == "exist":
                return True
            else:
                with open(path, "r") as f:
                    content = json.load(f)

                    # Always reparse if comment was skipped
                    if "_comment_skipped" in content:
                        return False

                    # Force parse if version upped
                    if not "version" in content or content["version"] != __version__:
                        return False

                    # Prevent parse if no version up and md5 doesn't change
                    if "md5" in content and content["md5"] == md5:
                        return True

        return False

    def parse(self, filename):

        try:

            self._parse(filename, encoding=self._encoding)

        except UnicodeDecodeError:

            # Fallback: UTF-8
            if self._encoding != "utf-8":
                # Shift encoding
                encoding = self._encoding
                self._encoding = "utf-8"
                # Try again
                self.parse(filename)
                # Recover encoding
                self._encoding = encoding

        except Exception as identifier:

            self.finish()
            raise identifier

    @log("Parsing...\n")
    def _parse(self, filename, encoding="utf-8"):
        """Parse target"""

        # Update count
        self._count += 1

        digest = ""

        with open(filename, "r", encoding=encoding) as f:
            target = f.read()

            # Calculate md5 first
            md5.update(bytearray(target.encode()))
            digest = md5.hexdigest()

            # Check if parsed only in not force mode
            if not self._force_parse:
                # Check if parsed
                if self.is_parsed(target, filename, digest):
                    self.skip(str(filename))
                    return "Skipped"

            try:
                # Parsing
                tree = self._parser.parse(target)
                # Make output object, in dict
                output = JavaTransformer().transform(tree)
            except UnexpectedInput as identifier:
                try:
                    # Remove comment and try again
                    target = removecomment(target)
                    tree = self._parser.parse(target)
                    # Make output object, in dict
                    output = JavaTransformer().transform(tree)
                    output["_comment_skipped"] = True
                    if self._comment_ignored is None:
                        self._comment_ignored = []
                    self._comment_ignored.append(filename)
                except UnexpectedInput as identifier:
                    # Nothing can do, write error log
                    return self.error(identifier, "ParseError", filename)
            except Exception as identifier:
                return self.error(identifier, "Exception", filename)

        # Add some additional info
        self._success += 1
        output["version"] = __version__
        output["md5"] = digest
        output["fileName"] = str(filename.absolute())

        # Fallback for cases that package is not specified
        if "package" in output:
            package = output["package"]["value"]
        else:
            package = "default_package"

        output["fullName"] = ".".join([package, output["name"]])

        # Set output for save to file
        self._output = output

        # Save to file if destination exists
        if self._destination:
            path = Path(self._destination)
            # Save to file
            if self._fileformat == "both":
                fn = path.joinpath(output["fullName"] + ".json")
                self.to_file(fn)
                fn = path.joinpath(output["fullName"] + ".yml")
                self.to_file(fn)
            else:
                fn = path.joinpath(output["fullName"] + "." + self._fileformat)
                self.to_file(fn)
            if not self._parsed:
                self._parsed = []
            self._parsed.append(output["fileName"])

        # Cleanup
        self._output = None

        return output

    @log("Searching files...")
    def search_and_parse(self, ignore_list=[]):
        """Search for parse"""

        if not self._target_dir:
            raise IOError("Target directory is not specified!")
        if not self._destination:
            raise IOError("Destination directory is not specified!")

        parse_targets = Path(self._destination).joinpath("parse_target_list.txt")
        ignore_list = IGNORE_LIST + ignore_list

        with open(parse_targets, "w") as f:

            def writer(message):
                f.write(message)
                f.write("\n")

            search_files(
                target_dir=self._target_dir,
                suffix=".java",
                writer=writer,
                ingore_list=ignore_list,
            )

        with open(parse_targets, "r") as f:
            for line in f:
                if line.strip():
                    self.parse(Path(line.strip()))

        self.finish()


if __name__ == "__main__":
    pass
