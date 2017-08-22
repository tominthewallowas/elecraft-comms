#!/usr/bin/python
# -*- coding: utf-8 -*-

# elecraft.py
'''
	This module is specific to the Elecraft K3S transceiver. The intent
	is to monitor the state of certain functions by interrogating the
	bytes returned from the IC command passed in from another module.
'''

common_response_fields = [
    [  # Byte A
        [],
        [],
        ['TX TEST', 'On', 'Off'],
        [],
        [],
        [],
        [],
        [],
    ],
    [  # Byte E
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    ]
]


by_mode_response_fields = {
	'CW_MODE':
		[
			[  # Byte B
				[],
				[],
				[],
				[],
				[],
				[],
				[],
				[],
			],
			[  # Byte C
				[],
				[],
				[],
				[],
				[],
				[],
				[],
				[],
			],
			[  # Byte D
				[],
				[],
				[],
				[],
				[],
				[],
				[],
				[],
			]
		],
	'VOICE_MODE':
		[
			[  # Byte B
				[],
				[],
				[],
				[],
				[],
				[],
				[],
				[],
			],
			[  # Byte C
				[],
				[],
				[],
				[],
				[],
				[],
				[],
				[],
			],
			[  # Byte D
				[],
				[],
				[],
				[],
				[],
				[],
				[],
				[],
			]
		],
	'SUBRX_MODE':
		[
			[  # Byte B
				[],
				[],
				[],
				[],
				[],
				[],
				[],
				[],
			],
			[  # Byte C
				[],
				[],
				[],
				[],
				[],
				[],
				[],
				[],
			],
			[  # Byte D
				[],
				[],
				[],
				[],
				[],
				[],
				[],
				[],
			]
		]
}


def listifyHexstring(hexstring):
    ''' Take a hex string returned from the IC command and
        turn it into a list of binary strings.
        Although the elecraft programmer's reference states
        that the first bit of each sequence of eight bits is
        the "bit0" it actually comes out in reverse.
    '''
    #print('listifyHexstring', hexstring)
    bin_str = '{0:020b}'.format(int(hexstring[2:39].encode('hex'), 16))
    #print(bin_str)
    status = []
    for x in range(0, 39, 8):
        # print(bin_str[x:x+8])
        status.append(bin_str[x:x + 8])
    return status


def interrogateStatus(all_status):
    ''' Using the list of binary strings from interrogateStatus,
                    compare each bit of each string and compare its value to
                    a lookup into a list of lists of lists containing a function
                    name and the value to return depending on 0 or 1.
    '''
    # print(all_status)
    rigstatus = {}
    for byte_number, status in enumerate(all_status):
        #print(byte_number, status)
        for pos, bit in enumerate(status):
            #print(pos, bit)
            if len(response_fields[byte_number][pos]) > 0:
                #print('got one')
                # print(response_fields[byte_number][pos][0])
                if bit == '1':
                    value = response_fields[byte_number][pos][1]
                else:
                    value = response_fields[byte_number][pos][2]

                rigstatus[response_fields[byte_number][pos][0]] = value
    print(rigstatus)


if __name__ == '__main__':
    responses = ['IC\xA1\x8C\xC4\xC4\x80;', 'IC\xA1\x8C\xD4\xC4\x80;']
    for response in responses:
		status = listifyHexstring(response)
		print status
		interrogateStatus(status)
