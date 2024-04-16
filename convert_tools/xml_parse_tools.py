import json
import re
from typing import Any

import xmltodict
from convert_tools.map import create_fields_mapping_json, document_type_id_name

fields_mapping_json = create_fields_mapping_json()


def create_correct_field_name(field_name: str, prefix: Any = None) -> str:
    # create understandable json key names
    field_name_words = [word.lower() for word in re.findall('[A-Z][^A-Z]*', field_name) if word != 'Doc']
    if prefix is not None:
        field_name_words.insert(0, prefix)
    correct_field_name = '_'.join(field_name_words)
    return correct_field_name


def traverse_json(json_dict: dict, result_dict: dict) -> dict:
    """
    Recursively traverse json dictionary
    :param json_dict: json dict with data from xml
    :param result_dict: result dict with data from xml
    :return: result dict with valid format
    """
    for tag, value in json_dict.items():
        if tag == "Entrant":
            result_dict[tag] = []
            if isinstance(value, list):
                for entrant in value:
                    result_dict[tag].append(traverse_json(entrant, {}))
            else:
                result_dict[tag].append(traverse_json(value, {}))
        elif tag == "Document":
            for document in value:
                document_type_id = int(document["IdDocumentType"])
                if document_type_id not in document_type_id_name:
                    raise KeyError(f"No such document type id: {document_type_id}")
                document_name = document_type_id_name[document_type_id][0]
                for field_name, field_value in document.items():
                    if field_name == "DocName":
                        continue
                    elif field_name in fields_mapping_json:
                        result_dict[fields_mapping_json[field_name]] = field_value
                    else:
                        result_dict[create_correct_field_name(field_name, prefix=document_name)] = field_value
        elif tag == "Address":
            if isinstance(value, list):
                for i, address in enumerate(value):
                    for field_name, field_value in address.items():
                        if field_name in fields_mapping_json:
                            correct_name = f"address{i + 1}_{fields_mapping_json[field_name]}"
                        else:
                            correct_name = create_correct_field_name(field_name, prefix=f"address{i + 1}")
                        result_dict[correct_name] = field_value
            else:
                for field_name, field_value in value.items():
                    if field_name in fields_mapping_json:
                        correct_name = f"address_{fields_mapping_json[field_name]}"
                    else:
                        correct_name = create_correct_field_name(field_name, prefix=f"address")
                    result_dict[correct_name] = field_value

        elif isinstance(value, dict):
            traverse_json(value, result_dict)
        else:
            if tag in fields_mapping_json:
                result_dict[fields_mapping_json[tag]] = value
            else:
                result_dict[create_correct_field_name(tag)] = value
    return result_dict


def convert_xml_to_dict(xml):
    # convert xml to dict
    json_dict = xmltodict.parse(xml)
    json_dict = traverse_json(json_dict, {})
    return json.dumps(json_dict["Entrant"], ensure_ascii=False)
