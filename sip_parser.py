import pyshark


def parse_sip_headers(headers_str):
    headers = {}
    header_lines = headers_str.split('\r\n')
    for line in header_lines:
        if ': ' in line:
            key, value = line.split(': ', 1)
            headers[key] = value
        elif len(line.strip()) > 0:  # Handling folded headers
            if headers:
                headers[list(headers.keys())[-1]] += ' ' + line.strip()
    return headers


def parse_sip_messages(pcap_file):
    global src_ip, dst_ip
    cap = pyshark.FileCapture(pcap_file, display_filter='sip')

    sip_messages = []

    for packet in cap:
        try:
            if 'SIP' in packet:
                if hasattr(packet, 'ipv6'):
                    src_ip = packet.ipv6.src
                    dst_ip = packet.ipv6.dst
                elif hasattr(packet, 'ip'):
                    src_ip = packet.ip.src
                    dst_ip = packet.ip.dst
                else:
                    print('hasattr else')
                    src_ip = None
                    dst_ip = None

                raw_headers = packet.sip._all_fields['sip.msg_hdr']
                parsed_headers = parse_sip_headers(raw_headers)

                sip_info = {
                    'time': packet.sniff_time,
                    'source_ip': src_ip,
                    'destination_ip': dst_ip,
                    'source_port': packet.udp.srcport,
                    'destination_port': packet.udp.dstport,
                    'request_line': getattr(packet.sip, 'Request_Line', None),
                    'status_line': getattr(packet.sip, 'Status_Line', None),
                    'headers': parsed_headers
                }
                sip_messages.append(sip_info)
        except AttributeError as e:
            print(f"Error processing packet: {e}")

    return sip_messages


# 사용 예시
pcap_file = "pcap/tcpdump_any_20240627143116.pcap"
sip_messages = parse_sip_messages(pcap_file)

for msg in sip_messages:
    print(f"Time: {msg['time']}")
    if msg['source_ip']:
        print(f"Source IP: {msg['source_ip']}:{msg['source_port']}")
    if msg['destination_ip']:
        print(f"Destination IP: {msg['destination_ip']}:{msg['destination_port']}")
    if msg['request_line']:
        print(f"Request Line: {msg['request_line']}")
    if msg['status_line']:
        print(f"Status Line: {msg['status_line']}")
    print(f"Headers: {msg['headers']}")
    print('----------------------------------')
