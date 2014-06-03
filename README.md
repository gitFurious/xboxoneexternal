# Xbox One External HDD Tool

## What

* Convert an Xbox One configured external hard drive to work with Windows.
* Convert a GPT+NTFS configured external hard drive to work with the Xbox One.

## Requirements

1. Xbox One.
2. External Hard drive greater than 256GB.
3. Python 2.7.
4. Administrator rights.

## Instructions

#### Xbox One to Windows PC

1. Use an Xbox One to correctly configure an external hard drive.
2. Physically connect the now Xbox One configured external hard drive to a Windows PC.
2. Run the script with the appropriate paramaters (see xboxoneexternal.py --help, or below). 
4. Power cycle the external hard drive.

#### Windows PC to Xbox One

1. Use a Windows PC to correctly configure a GPT disk with an NTFS partition.
2. Run the script with the appropriate paramaters (see xboxoneexternal.py --help, or below). 
3. Physically connect the now Xbox One configured external hard drive to a Windows PC.

#### Screenshot

![cmd](http://i.imgur.com/B6EdboT.png)

## Parameters

```
usage: xboxoneexternal.py [-h] -d DRIVE [-i] [-bs] [-ds]

Xbox One External HDD Tool

optional arguments:

-h, --help                 show this help message and exit
-d DRIVE, --drive DRIVE    The target physical drive
-i, --ignore               Ignore the 'Xbox One NT Disk Signature' sanity check
-bs, --bootsignature       Update 'Boot Signature'
-ds, --disksignature       Update 'NT Disk Signature'
```

## Examples

#### Display current 'Boot Signature' and 'NT Disk Signature'

```
xboxoneexternal.py -d \\.\PhysicalDrive5

NT Disk Signature:      0x12345678
Boot Signature:         0x99cc
```


#### Xbox One to Windows PC

```
xboxoneexternal.py -bs -d \\.\PhysicalDrive5 

NT Disk Signature:      0x12345678
Boot Signature:         0x99cc
Operation:              Xbox One->PC
NEW Boot Signature:     0x55aa

Writing new MBR ... done.
```

#### Windows PC to Xbox One

```
xboxoneexternal.py -i -bs -d \\.\PhysicalDrive5 

NT Disk Signature:      0x12345678
Boot Signature:         0x55aa
Operation:              PC->Xbox One
NEW Boot Signature:     0x99cc

Writing new MBR ... done.
```

#### Update 'NT Disk Signature' with the default value used by the Xbox One (sanity!)

```
xboxoneexternal.py -i -bs -ds -d \\.\PhysicalDrive5

NT Disk Signature:      0x46555249
Boot Signature:         0x55aa
NEW NT Disk Signature:  0x12345678

Writing new MBR ... done.
```

## What to Expect

```
F:\>dir /p
 Volume in drive F is Pluto
 Volume Serial Number is xxxx-xxxx

 Directory of F:\

01/06/2014  09:39 AM     2,191,065,088 520FCE1F-7BF6-48AE-AF3A-A469574766D9        (Peggle 2)
01/06/2014  09:39 AM             4,096 520FCE1F-7BF6-48AE-AF3A-A469574766D9.xvi    (Peggle 2)
01/06/2014  09:41 AM     5,367,975,936 F57F7834-5D73-4CAA-8479-3107957CC0AB        (Trials Evolution)
01/06/2014  09:41 AM             4,096 F57F7834-5D73-4CAA-8479-3107957CC0AB.xvi    (Trials Evolution)
01/06/2014  09:40 AM                16 LastConsole                                 (Console GUID(?))
               5 File(s)  7,559,049,232 bytes
               0 Dir(s)  504,384,786,432 bytes free

F:\>tree /f /a
Folder PATH listing for volume Pluto
Volume serial number is xxxxxxxx xxxx:xxxx
F:.
    520FCE1F-7BF6-48AE-AF3A-A469574766D9        (Peggle 2 - MD5:8F06F76D0BEE9681FF5F9A3E4187AB1D)
    520FCE1F-7BF6-48AE-AF3A-A469574766D9.xvi    (Peggle 2 - MD5:A0B247B79954C469B6CF635FAA7BBF6D)
    F57F7834-5D73-4CAA-8479-3107957CC0AB        (Trials Evolution - MD5:ED511CDD51A8BB2FE09CC0A4538AC71F)
    F57F7834-5D73-4CAA-8479-3107957CC0AB.xvi    (Trials Evolution - MD5:A66BD3E8125650C6D1FE84D73EC591FA)
    LastConsole

No subfolders exist
```

## How?

The Xbox One initializes the external drive with a GPT (GUID Partition Table).

The original Boot Signature of the device 0x99CC (0x1FE-0x1FF) doesn't appear to allow the drive to be seen as initialized in Windows.

Swapping the two Boot Signature bytes with the traditional 0x55AA allows the NTFS partition to be seen be Windows.

Original 'Protective MBR':
```
Offset(h)   00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F

0000000000  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000010  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000020  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000030  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000040  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000050  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000060  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000070  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000080  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000090  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000000A0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000000B0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000000C0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000000D0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000000E0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000000F0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000100  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000110  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000120  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000130  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000140  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000150  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000160  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000170  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000180  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000190  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000001A0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000001B0  00 00 00 00 00 00 00 00 12 34 56 78 00 00 00 00  .........4Vx....
00000001C0  00 00 EE 00 00 00 01 00 00 00 AE 12 9E 3B 00 00  ..î.......®.ž;..
00000001D0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000001E0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000001F0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 99 CC  ..............™Ì
```

Modified 'Protective MBR':
```
Offset(h)   00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F

0000000000  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000010  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000020  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000030  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000040  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000050  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000060  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000070  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000080  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000090  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000000A0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000000B0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000000C0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000000D0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000000E0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000000F0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000100  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000110  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000120  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000130  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000140  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000150  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000160  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000170  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000180  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
0000000190  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000001A0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000001B0  00 00 00 00 00 00 00 00 12 34 56 78 00 00 00 00  .........4Vx....
00000001C0  00 00 EE 00 00 00 01 00 00 00 AE 12 9E 3B 00 00  ..î.......®.ž;..
00000001D0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000001E0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000001F0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 55 AA  ..............™Ì
```

## Notes

1. Windows will offer to initialize an Xbox One formatted disk. Don't do this unless you want to start everything again.
2. If the Boot Signature matches 0x99CC, the Xbox One will be able to read the partitions. Windows PC will not.
3. If the Boot Signature matches 0x55AA, a Windows PC will be able to read the partitions. Xbox One will not.
4. Windows might complain that there is something wrong with the disk and will want to run a chkdsk. I don't reccomend doing this.
5. Make sure you specify the right disk - don't come to me when it hits the fan.

