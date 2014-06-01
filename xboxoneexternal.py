__author__ = '@DamonLPollard'

import sys


SECTOR_SIZE = 0x200
XBOX_ONE_NT_DISK_SIGNATURE = '12345678'.decode('hex')
XBOX_ONE_BOOT_SIGNATURE = '99cc'.decode('hex')
PC_BOOT_SIGNATURE = '55aa'.decode('hex')


def usage():
    print 'Usage:   {0} [disk]'.format(sys.argv[0])
    print 'Example: {0} {1}'.format(sys.argv[0], r"\\.\PhysicalDriveX")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(usage())
        sys.exit(-1)

    path = sys.argv[1]
    try:
        with open(path, 'r+b') as disk:
            disk.seek(0)
            sector_zero = disk.read(SECTOR_SIZE)

            nt_disk_signature = sector_zero[0x1b8:0x1bc]
            boot_signature = sector_zero[0x1fe:0x200]

            print
            print 'NT Disk Signature: \t0x{0}'.format(nt_disk_signature.encode('hex'))
            print 'Boot Signature: \t0x{0}'.format(boot_signature.encode('hex'))

            if nt_disk_signature == XBOX_ONE_NT_DISK_SIGNATURE:
                if boot_signature == XBOX_ONE_BOOT_SIGNATURE:
                    print 'Operation: \t\tXbox One->PC'
                    print 'NEW Boot Signature: \t0x{0}'.format(PC_BOOT_SIGNATURE.encode('hex'))
                    sector_zero = sector_zero[:-2] + PC_BOOT_SIGNATURE
                    disk.seek(0)
                    disk.write(sector_zero)
                elif boot_signature == PC_BOOT_SIGNATURE:
                    print 'Operation: \t\tPC->Xbox One'
                    print 'NEW Boot Signature: \t0x{0}'.format(XBOX_ONE_BOOT_SIGNATURE.encode('hex'))
                    sector_zero = sector_zero[:-2] + XBOX_ONE_BOOT_SIGNATURE
                    disk.seek(0)
                    disk.write(sector_zero)
                else:
                    raise Exception("Unexpected Boot Signature.")
            else:
                raise Exception("Unexpected NT Disk Signature.")

        print
        print 'Done!'
        print


    except Exception as ex:
        print(ex)
        exit(-1)