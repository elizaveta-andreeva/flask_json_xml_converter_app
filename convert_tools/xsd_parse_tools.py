import json
from typing import Any

import xmlschema
from xml.etree import ElementTree

from convert_tools.map import document_type_id_name, map_json_keys, address_fields_map, doc_fields

schema = xmlschema.XMLSchema('data/Add_Entrant_List.xsd')


def get_fields(document_id: int) -> list:
    # return document fields from dict_document_type_cls.json
    with open('data/dict_document_type_cls.json', encoding="utf8") as f:
        dict_document_type_cls = json.load(f)
    for cls in dict_document_type_cls:
        if cls["Id"] == document_id:
            return cls["FieldsDescription"]["fields"]


def has_children(element: ElementTree.Element) -> bool:
    # check children tags with name attribute
    return any(child.tag.endswith('element') and 'name' in child.attrib for child in list(element.iter())[1:])


def traverse_xsd(element: ElementTree.Element, json_data: dict, result: dict, parent: str) -> dict:
    """
    Traverse the schema and fill result dict
    :param element: current tag
    :param json_data: json data from user
    :param result: result dict that contains necessary fields according to schema
    :param parent: parent tag that has name attribute
    :return: result dict that we will convert to valid xml
    """
    # if tag has name we should add it to json
    if 'name' in element.attrib:
        # if tag name is Fields we should take document fields
        if element.attrib['name'] == 'Fields':
            fields = get_fields(json_data['IdDocumentType'])
            result[parent][element.attrib['name']] = {}
            for field in fields:
                if field["xml_name"] in json_data:
                    result[parent][element.attrib['name']][field["xml_name"]] = json_data[field["xml_name"]]
                elif not field["not_null"]:
                    continue
                else:
                    raise KeyError(f"No such field in json data: {field['xml_name']}")
        if element.attrib['name'] == 'AddressList':
            result[parent][element.attrib['name']] = handle_address(json_data)
            return result
        # if tag has no children we should take its value
        elif not has_children(element):
            if element.attrib['name'] in json_data:
                if json_data[element.attrib['name']] is None and 'minOccurs' in element.attrib and int(
                        element.attrib['minOccurs']) == 0:
                    pass
                else:
                    result[parent][element.attrib['name']] = json_data[element.attrib['name']]
            elif 'minOccurs' in element.attrib and int(element.attrib['minOccurs']) == 0:
                print(element.attrib['name'])
                pass
            else:
                if element.attrib['name'] in ['DocName', 'DocSeries', 'DocNumber', 'IssueDate', 'DocOrganization']:
                    if element.attrib['name'] == 'DocName':
                        result[parent][element.attrib['name']] = \
                            document_type_id_name[int(json_data["IdDocumentType"])][1]
                    else:
                        document_name = document_type_id_name[int(json_data["IdDocumentType"])][0]
                        field_name = f"{document_name}_{doc_fields[element.attrib['name']]}"
                        if field_name in json_data:
                            result[parent][element.attrib['name']] = json_data[field_name]
                        else:
                            KeyError(f"No such field in json data: {field_name}")
                else:
                    KeyError(f"No such field in json data: {element.attrib['name']}")
        else:
            result[parent][element.attrib['name']] = {}
        result = result[parent]
        parent = element.attrib['name']
    for child in element:
        traverse_xsd(child, json_data, result, parent)
    return result


def handle_choice(result_dict: dict) -> dict:
    # if entrant already has service guid then keep Guid tag and pop AddEntrant tag
    for key, value in result_dict.items():
        if value['Guid'] is None:
            value.pop('Guid')
            break
        else:
            value.pop('AddEntrant')
            break
    return result_dict


def handle_address(json_data: dict) -> Any:
    # process entrant addresses
    full_address_fields = ["address_txt1", "address_txt2", "address_txt3", "address_txt4"]
    if not json_data['has_another_living_address']:
        result = {'Address': {'FullAddr': ''}}
        for field in full_address_fields:
            if field in json_data and json_data[field] is not None:
                result['Address']['FullAddr'] += json_data[field]

        for address_field_name, map_field_name in address_fields_map.items():
            result['Address'][map_field_name] = json_data[address_field_name]
        return result
    else:
        result = []
        for address_field_name, map_field_name in address_fields_map.items():
            json_data_field_names = [name for name in json_data if address_field_name in name]
            if not result:
                result = [{'FullAddr': ''} for _ in range(len(json_data_field_names))]
            for i, name in enumerate(json_data_field_names):
                result[i][map_field_name] = json_data[name]

        for full_address_field in full_address_fields:
            full_address_fields_values = [name for name in json_data if full_address_field in name]
            for i, name in enumerate(full_address_fields_values):
                if name in json_data and json_data[name] is not None:
                    result[i]['FullAddr'] += json_data[name]
        return result


def parse_json_xsd(schema: xmlschema.validators.schemas.XMLSchema10, json_data: Any) -> dict:
    # if json_data contains data about several entrants
    if isinstance(json_data, list):
        map_json_data = []
        result = {"EntrantChoice": {"AddEntrant": []}}
        for entrant_data in json_data:
            map_json_data.append(map_json_keys(entrant_data))
        for entrant_data in map_json_data:
            entrant_result = handle_choice(traverse_xsd(schema.root[0], entrant_data, {'root': {}}, 'root'))
            result['EntrantChoice']['AddEntrant'].append(entrant_result['EntrantChoice']['AddEntrant'])
    else:
        json_data = map_json_keys(json_data)
        result = handle_choice(traverse_xsd(schema.root[0], json_data, {'root': {}}, 'root'))
    return result
