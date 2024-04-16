import xmlschema
import dicttoxml
from flask import Flask, render_template, request, Response
import json

from convert_tools.xml_parse_tools import convert_xml_to_dict
from convert_tools.xsd_parse_tools import parse_json_xsd

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/convert/json_to_xml', defaults={'validate': False}, methods=['POST'])
@app.route('/convert/json_to_xml/<validate>', methods=['POST'])
def convert_json_to_xml(validate: bool) -> Response:
    schema = xmlschema.XMLSchema('data/Add_Entrant_List.xsd')

    json_data = request.form.get('json')
    data_dict = json.loads(json_data)

    data = parse_json_xsd(schema, data_dict)

    xml = dicttoxml.dicttoxml(data, attr_type=False, root=False, item_func=lambda tag_name: 'Address')

    if validate:
        if schema.is_valid(xml):
            return Response(xml, mimetype='text/xml', status=200)
        else:
            schema.validate(xml)
            return Response("XML does not match XSD schema", status=400)

    return Response(xml, mimetype='text/xml', status=200)


@app.route('/convert/xml_to_json', defaults={'validate': False}, methods=['POST'])
@app.route('/convert/xml_to_json/<validate>', methods=['POST'])
def convert_xml_to_json(validate: bool) -> Response:
    xml = request.form.get('xml')
    schema = xmlschema.XMLSchema('data/Get_Entrant_List.xsd')

    if validate:
        if not schema.is_valid(xml):
            schema.validate(xml)
            return Response("XML does not match XSD schema", status=400)

    json_result = convert_xml_to_dict(xml)
    return Response(json_result, mimetype='application/json', status=200)


if __name__ == '__main__':
    app.run(debug=True)
