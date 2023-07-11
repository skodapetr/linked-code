#!/usr/bin/env python3
# Extract annotations from source files.
#
import argparse
from pprint import pprint

from comment_parser import comment_parser

from annotation_model import *

# List of types https://pypi.org/project/comment-parser/
EXTENSION_MAPPING = {
    ".ts": "application/javascript",
    ".js": "application/javascript",
    ".py": "text/x-python",
    ".html": "text/html",
    ".java": "text/x-java-source",
    ".c": "text/x-c",
    ".h": "text/x-c",
    ".cpp": "text/x-c++",
    ".hpp": "text/x-c++",
    ".xml": "text/xml",
}

COMMENT_PREFIX = "@lc-"


def _parse_arguments():
    parser = argparse.ArgumentParser(description="Extract annotations from given file.")
    parser.add_argument(
        action="store", dest="input", help="File to extract annotations from."
    )
    return vars(parser.parse_args())


def main(args):
    file = extract_source_file(args["input"])
    pprint(file.annotations)


def extract_source_file(file_path: str, mime=None) -> SourceFile:
    # List of mime-types: https://pypi.org/project/comment-parser/
    annotations: list[Annotation] = [
        annotation
        for comment in _read_comments_from_file(file_path, mime)
        for annotation in _comment_to_annotations(comment)
    ]
    return SourceFile(file_path, annotations)


def _read_comments_from_file(file_path: str, mime=None):
    if mime is None:
        extension = file_path[file_path.rfind(".") :].lower()
        mime = EXTENSION_MAPPING.get(extension, None)
    if mime is None:
        # We ignore the file as we are unable to read it.
        return []
    return comment_parser.extract_comments(file_path, mime)


def _comment_to_annotations(comment) -> list[Annotation]:
    result = []
    lines = _split_comment(comment)
    comment_line_start = comment.line_number()
    for offset, line in enumerate(lines):
        if not line.startswith(COMMENT_PREFIX):
            continue
        annotation = _create_annotation(comment_line_start, offset, line)
        if annotation is not None:
            result.append(annotation)
    return result


def _split_comment(comment) -> list[str]:
    # TODO Consider multiline comments.
    if comment.is_multiline():
        lines = [line.strip()[1:].strip() for line in comment.text().splitlines()]
    else:
        lines = [comment.text().strip()]
    return lines


def _create_annotation(
    comment_start: int, annotation_offset: int, content: str
) -> Annotation:
    annotation_start = comment_start + annotation_offset
    tokens = content.split()
    annotation_name = tokens[0][len(COMMENT_PREFIX) :]
    args = tokens[1:]
    if annotation_name == "prefix":
        prefix = args[0]
        base = args[1]
        return PrefixAnnotation(comment_start, annotation_start, prefix, base)
    elif annotation_name == "entity":
        return EntityAnnotation(comment_start, annotation_start)
    elif annotation_name == "property":
        return PropertyAnnotation(comment_start, annotation_start)
    elif annotation_name == "identifier":
        identifier = args[0]
        return IdentifierAnnotation(comment_start, annotation_start, identifier)
    elif annotation_name == "name":
        name = " ".join(args)
        return NameAnnotation(comment_start, annotation_start, name)
    elif annotation_name == "label":
        label = " ".join(args)
        return LabelAnnotation(comment_start, annotation_start, label)
    elif annotation_name == "description":
        description = " ".join(args)
        return DescriptionAnnotation(comment_start, annotation_start, description)
    elif annotation_name == "extends":
        return EntityExtendsAnnotation(comment_start, annotation_start, args)
    elif annotation_name == "type":
        type = args[0]
        return TypeAnnotation(comment_start, annotation_start, type)
    else:
        return None


if __name__ == "__main__":
    main(_parse_arguments())
