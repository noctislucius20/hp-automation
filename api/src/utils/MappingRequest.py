import ast

def mapping_data(data):
    request_mapping = {
        'firstName': 'first_name',
        'lastName': 'last_name',
        'ipAddress': 'ip_address',
    }
    try:
        for old_prop, new_prop in request_mapping.items():
            if old_prop in data:
                data[new_prop] = data[old_prop]
                data.pop(old_prop)

        if 'honeypot' in data:
            data['honeypot'] = [ast.literal_eval(honeypot) for honeypot in data['honeypot']]
                
        return data
    
    except Exception as e:
        print(e)
