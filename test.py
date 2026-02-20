

def handle_afp_payload(payload):
    print(payload)

def handle_document_payload(payload):
    print(payload)

with open('./sample/POC_AFP_PARSE_structure.json', 'r', encoding='utf-8') as f:
    for l in f:
        if l.strip() in ['}', '{', '],'] or l.strip().startswith('"documents"'):
            continue

        l_stripped = l.rstrip(',\n')

        if l_stripped.startswith('"afp"'):
            handle_afp_payload(l_stripped.lstrip('"afp": '))
        else:
            handle_document_payload(l_stripped)