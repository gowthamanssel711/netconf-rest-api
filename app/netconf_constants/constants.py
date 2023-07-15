filter_tag = """
        <filter>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
            <{interface_name}>
            <name>2</name>
            </{interface_name}>
        </interface>
        </native>
        </filter>
"""

add_configuration = """
 <config>
     <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
             <interface>
                     <name>{interface_name}</name>
                     <description>{interface_description}</description>
                     <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
                     <enabled>true</enabled>
                     <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                             <address>
                                     <ip>{ip_address}</ip>
                                     <netmask>{subnet_mask}</netmask>
                             </address>
                     </ipv4>
             </interface>
     </interfaces>
</config>
"""

delete_configuration = """
<config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface operation="{operation}">
                        <name>{interface_name}</name>
                </interface>
        </interfaces>
</config>
"""