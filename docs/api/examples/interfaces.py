# TODO: Let user filter by ctnr and attributes. Auto-resolve hyperlinked fields.
# TODO: Make columns fqdn, type, mac, ip, last seen.

from conrad import Conrad

API_TOKEN = "4df242bda29ab46e9343ed1042a557fa9540935c"
INTERFACE_ENDPOINT_URL = "http://127.0.0.1:8000/api/v1/core/interface/"


def render_csv(cols, data, separator=',', newline='\n'):
    print separator.join(cols)
    print newline.join(
        [separator.join([(row[col] if col in row else "") for col in cols]) for row in data])


def list_to_csv(list, separator=',', newline='\n'):
    return newline.join([separator.join(row) for row in list])


# TODO: add some filtering options (at least by ctnr)
def get_systems(limit=None, ctnr=None):
    """
    Params:
        limit - Lets you limit the number of results, but because of how it's
                checked, you may get more. I guarantee
                    abs(num_results - limit) <= 100
                will be True (unless both the maximum record per page limit
                and Conrad are altered).
    """
    c = Conrad(API_TOKEN, INTERFACE_ENDPOINT_URL)
    query = {'ctnr': ctnr} if ctnr else None
    c.get(query=query)

    interfaces = []
    num_results = 0

    while True:
        interfaces += c.result
        num_results += len(c.result)

        if limit and num_results >= limit:
            break

        if not c.get_next():
            break

    return interfaces


def filter_dict(dict, keys):
    return {key: dict[key] for key in keys}


def process_interfaces(systems,
                      system_fields=(),
                      staticinterface_fields=('fqdn', 'ip_str', 'mac',
                                              'last_seen'),
                      dynamicinterface_fields=('domain', 'range', 'mac',
                                               'last_seen')):
    """
    Take the nested dict containing an interface and convert it to a 2D list for
    CSV conversion.
    """

    # extract
    # processed = {}
    # processed.update(filter_dict(interface, system_fields))
    # processed.update(filter_dict(interface['staticinterface_set'],
    #                              staticinterface_fields))
    # processed.update(filter_dict(interface['dynamicinterface_set'],
    #                              dynamicinterface_fields))

    # processed = []
    # processed.append([interface[field] for field in system_fields])
    # processed.append([interface['staticinterface_set'][field]
    #                   for field in staticinterface_fields])
    # processed.append([interface['dynamicinterface_set'][field]
    #                   for field in dynamicinterface_fields])

    headers = list(
        set(system_fields)
        | set(staticinterface_fields)
        | set(dynamicinterface_fields)
    )
    rows = []

    for system in systems:
        system_info = {f: system[f] for f in system_fields}

        for si in system['staticinterface_set']:
            row = {}
            row.update(system_info)
            row.update(filter_dict(si, staticinterface_fields))
            rows.append(row)

        for di in system['dynamicinterface_set']:
            row = {}
            row.update(system_info)
            row.update(filter_dict(di, dynamicinterface_fields))
            rows.append(row)

    return headers, rows


def main():
    systems = get_systems(ctnr="zone.ads-fn")
    headers, rows = process_interfaces(systems)
    render_csv(headers, rows, separator='~')


if __name__ == "__main__":
    main()