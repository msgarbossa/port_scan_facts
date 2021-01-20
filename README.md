# Ansible Role: port_scan_facts

Scan destination TCP ports.  The resulting facts contain the round-trip-time for the TCP connection.  A duration of -1 indicates a failed connection.  A custom module is used to time a TCP connect (send SYN packet, get SYN-ACK).

## Role Variables

| Variable                | Choices/Defaults | Purpose/Description                                                                     |
| ----------------------- | ---------------- | --------------------------------------------------------------------------------------- |
| destinations            | []               | list of dictionaries with keys for name, d_host and/or d_ip, and d_port                  |

## Role Dependencies

- none

## Example Playbook

- The source for the TCP connection will be ansible_host.  Use delegate_to: localhost to source connection attempts from the local Ansible controller.
- Either d_host or d_ip must be supplied for each entry
- If both d_host and d_ip are supplied, d_ip will override d_host

```yaml
    - name: Include role to scan ports
      include_role:
        name: port_scan_facts
      vars:
        destinations:
          - name: Google
            d_host: www.google.com
            d_port: 443
          - name: Microsoft
            d_host: www.microsoft.com
            d_port: 443

    - name: Print port scan facts
      debug:
        var: port_scan_facts
```

## Example Facts

Ansible task:

```json

    "port_scan_facts": {
        "www.google.com:443": 63,
        "www.microsoft.com:443": 65
    }
```

## Testing

```
molecule test
```

## Future Improvements

- Allow failures when port checks fail
- Ability to define failure groups
  - failure_group ID defined for each item in list?
  - look for lists of lists and ensure minimum of 1 item passes?
- Result format
  - simple (current)
  - verbose (dictionary result per item) to more easily allow parsing of results

## License

MIT / BSD

## Source

https://github.com/msgarbossa/port_scan_facts

