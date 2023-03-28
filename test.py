__is_Stateimport subprocess

# convert hex (0x00000001) to decimal (1)
def hex_to_dec(hex_num):
    return int(hex_num, 16)

def _ON():
    output = subprocess.check_output('powercfg /q').decode('utf-8')
    output = output.split('\n')

    index = 0

    for line in output:
        if 'Subgroup GUID: 4f971e89-eebd-4455-a8de-9e59040e7347' in line and 'Power Setting GUID: 5ca83367-6e45-459f-a27b-476b1d01c936' in output[index + 2]:
            AC = output[index + 12]
            DC = output[index + 13]

            if 'Current AC Power Setting Index:' in AC and 'Current DC Power Setting Index:' in DC:
                hex_AC = AC.strip().split(':')[1].strip()
                dec_AC = hex_to_dec(hex_AC)
                print (dec_AC)

                hex_DC = DC.strip().split(':')[1].strip()
                dec_DC = hex_to_dec(hex_DC)
                print (dec_DC)

                if dec_AC == 0 and dec_DC == 0:
                    return True
                else:
                    return False
                
        index += 1
        
    return None



if __name__ == "__main__":
    # get_remaining_battery()
    # get_lid_state()
    print (get_lid_state())