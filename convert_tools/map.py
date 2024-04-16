fields_mapping_xml = {
    "first_name": "Name",
    "second_name": "Surname",
    "middle_name": "Patronymic",
    "dict_sex_id": "IdGender",
    "birthday": "Birthday",
    "motherland": "Birthplace",
    "tel_mobile": "Phone",
    "email": "Email",
    "citizenship_id": "IdOksm",
    "residence_country_id": "SubdivisionCode",
    "passport_endda": "ExpirationDate",
    "paid_passport_endda": "ExpirationDate",
    "old_passport_endda": "ExpirationDate",
    "paid_contract_endda": "ExpirationDate",
    "snils": "Snils",
    "service_entrant_guid": "Guid",
    "document_type_id": "IdDocumentType",
    "document_name": "DocName"
}

doc_fields = {
    "IssueDate": "begda",
    "ExpirationDate": "endda",
    "DocNumber": "number",
    "DocOrganization": "issued_by",
    "DocSeries": "series"
}

address_fields_map = {
    "kladr_1": "IdRegion",
    "is_registration": "IsRegistration",
    "address_txt3": "City"
}

document_type_id_name = {
    100001: ["passport", "Паспорт гражданина Российской Федерации"],
    100002: ["military_card", "Военный билет"],
    100037: ["temporary_identity_card", "Временное удостоверение личности"],
    100038: ["resident_card", "Вид на жительство"],
    100039: ["paid_passport", "Заграничный паспорт гражданина Российской Федерации"],
    100040: ["foreign_passport", "Паспорт гражданина иностранного государства"],
    100042: ["diplomatic_passport", "Дипломатический паспорт"],
    100043: ["service_passport", "Служебный паспорт"],
    100045: ["temporary_residence_permit", "Разрешение на временное проживание"],
    100046: ["refugee_card", "Удостоверение беженца"],
    100048: ["temporary_asylum_card", "Свидетельство о предоставлении временного убежища"],
    100052: ["military_certificate", "Удостоверение военнослужащего Российской Федерации"],
    100053: ["seaman_identity_card", "Удостоверение личности моряка"],
    100054: ["stateless_person_temporary_identity_card", "Временное удостоверение личности лица без гражданства в РФ"],
    100055: ["temporary_identity_document", "Документ, удостоверяющий личность на период рассмотрения заявления о "
                                            "признании гражданином РФ или о приеме в гражданство РФ"],
    100056: ["application_certificate",
             "Свидетельство о рассмотрении ходатайства о признании беженцем на территории РФ по существу"],
    100057: ["foreign_document",
             "Документ, выданный иностранным государством и признаваемый в соответствии с международным договором"
             " РФ в качестве документа, удостоверяющего личность лица без гражданства"]
}


def map_json_keys(json_dict: dict) -> dict:
    """
    Map json key names to valid names
    :param json_dict: json data from user
    :return: json with valid key names
    """
    for key in list(json_dict.keys()):
        if key == 'has_another_living_address':
            json_dict["IsRegistration"] = not json_dict["has_another_living_address"]
        if key in fields_mapping_xml:
            new_key = fields_mapping_xml[key]
            json_dict[new_key] = json_dict.pop(key)
    return json_dict


def map_address_key_names():
    pass


def create_fields_mapping_json() -> dict:
    # create dict to map key names to convert xml to json
    fields_mapping_json = {}
    fields_values = list(fields_mapping_xml.values())
    for key, value in fields_mapping_xml.items():
        if fields_values.count(value) > 1:
            continue
        else:
            fields_mapping_json[value] = key
    return fields_mapping_json
