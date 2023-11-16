from flask import request, make_response, send_file, jsonify
def return_response(status_code = 200, message: str = None, data: dict or list = None, response_type = "json", filepath = None, attachment=True, preflight=False):
    if not preflight:
        if response_type == "json":
            obj = {
                "status_code": status_code
            }
            if data is not None:
                obj['data'] = data
            
            if message is not None:
                obj['message'] = message
                
            response = make_response(jsonify(obj))
            response.status_code = status_code
        elif response_type == 'file' and filepath is not None: 
            response = send_file(filepath, as_attachment=attachment)
    else:
        response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    return response