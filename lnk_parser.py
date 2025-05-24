import sys


def LinkFlags(num):
    flags = [
        (0, 'HasLinkTargetIDList'),
        (1, 'HasLinkInfo'),
        (2, 'HasName'),
        (3, 'HasRelativePath'),
        (4, 'HasWorkingDir'),
        (5, 'HasArguments'),
        (6, 'HasIconLocation'),
        (7, 'IsUnicode'),
        (8, 'ForceNoLinkInfo'),
        (9, 'HasExpString'),
        (10, 'RunInSeparateProcess'),
        (11, 'Unused1'),
        (12, 'HasDarwinID'),
        (13, 'RunAsUser'),
        (14, 'HasExpIcon'),
        (15, 'NoPidlAlias'),
        (16 , 'Unused2'),
        (17, 'RunWithShimLayer'),
        (18, 'ForceNoLinkTrack'),
        (19, 'EnableTargetMetadata'),
        (20, 'DisableLinkPathTracking'),
        (21, 'DisableKnownFolderTracking'),
        (22, 'DisableKnownFolderAlias'),
        (23, 'AllowLinkToLink'),
        (24, 'UnaliasOnSave'),
        (25, 'PreferEnvironmentPath'),
        (26, 'KeepLocalIDListForUNCTarget'),
    ]
    enabled = []
    for bit, name in flags:
        if (num >> bit) & 1:
            enabled.append(name)

    return enabled

def FileAttributesFlags(num):
    flags = [
    (0, 'FILE_ATTRIBUTE_READONLY'),
    (1, 'FILE_ATTRIBUTE_HIDDEN'),
    (2, 'FILE_ATTRIBUTE_SYSTEM'),
    (3, 'Reserved1'),
    (4, 'FILE_ATTRIBUTE_DIRECTORY'),
    (5, 'FILE_ATTRIBUTE_ARCHIVE'),
    (6, 'Reserved2'),
    (7, 'FILE_ATTRIBUTE_NORMAL'),
    (8, 'FILE_ATTRIBUTE_TEMPORARY'),
    (9, 'FILE_ATTRIBUTE_SPARSE_FILE'),
    (10, 'FILE_ATTRIBUTE_REPARSE_POINT'),
    (11, 'FILE_ATTRIBUTE_COMPRESSED'),
    (12, 'FILE_ATTRIBUTE_OFFLINE'),
    (13, 'FILE_ATTRIBUTE_NOT_CONTENT_INDEXED'),
    (14, 'FILE_ATTRIBUTE_ENCRYPTED')
]
    enabled = []
    for bit, name in flags:
        if (num >> bit) & 1:
            enabled.append(name)

    return enabled

def rev(bt):
    # little endian 換 big endian
    bytes_data = bytes.fromhex(bt)
    reordered = bytes_data[::-1]  # 反轉
    linkflags_int = int.from_bytes(reordered, byteorder='big')
    return linkflags_int


def read_lnk_structure(data):

    
    structure = {}

    # 檢查開頭的 20 bytes (HeaderSize)
    header_size = data[:20]

    if header_size == b'\x4C\x00\x00\x00\x01\x14\x02\x00\x00\x00\x00\x00\xc0\x00\x00\x00\x00\x00\x00\x46':
        structure['HeaderSize_Valid'] = True
    else:
        print('Wrong file! NOT LNK file')
        return '-1'


    # LinkFlags (4 bytes)
    link_flags = data[20:24]
    structure['LinkFlags'] = LinkFlags(rev(link_flags.hex()))

    # FileAttributesFlags (4 bytes)
    File_Attributes_Flags = data[24:28]
    structure['FileAttributesFlags'] = FileAttributesFlags(rev(File_Attributes_Flags.hex()))

    # HotKey (2 bytes)
    Hot_Key = data[0x40:0x42]
    if (Hot_Key == b'\x00\x00'):
        structure['HotKey'] = 'NO'
    else:
        key =''
        if data[0x41] & 0x01:
            key+=('SHIFT ')
        if data[0x41] & 0x02:
            key+=('CTRL ')
        if data[0x41] & 0x04:
            key+=('ALT ')
        structure['HotKey'] = chr(data[0x40]) , key

    return structure


def check_item(data,num,ed):
    item = []
    ed-=2
    while ed != 0:
        size = rev(data[num:num+2].hex()) 
        ed -= size
        item.append(data[num:num+size])
        num = num+size
    return item


def LinkTargetIDList(data):
    size = rev(data [76:78].hex())
    item =check_item(data,78,size)
    for idx, content in enumerate(item, start=1):
        hex_string = ''.join(f'\\x{b:02x}' for b in content)
        print(f"item {idx}: {hex_string}")
    return 78+size


def HasLinkInfo(data,now):
    size = rev(data [now:now+4].hex())
    print ("LinkInfoSize size:",size)
    now+=4

    size = rev(data [now:now+4].hex())
    print ("LinkInfoHeaderSize size:",size)
    now +=4

    # check LinkInfoFlags 直接手刻((
    Vo = 0
    Co = 0
    info = rev(data [now:now+4].hex())
    if (info == 1):
        print("LinkInfoFlags: VolumeIDAndLocalBasePath")
        Vo = 1
    elif (info == 2):
        print("LinkInfoFlags: CommonNetworkRelativeLinkAndPathSuffix")
        Co = 1
    elif (info ==3):
        print("LinkInfoFlags: VolumeIDAndLocalBasePath, CommonNetworkRelativeLinkAndPathSuffix")
        Vo = 1
        Co = 1  
    now +=4


    size = rev(data [now:now+4].hex())
    print ("VolumeIDOffset:",size)
    now +=4

    size = rev(data [now:now+4].hex())
    print ("LocalBasePathOffset:",size)
    lb = size
    now +=4

    size = rev(data [now:now+4].hex())
    print ("CommonNetworkRelativeLinkOffset	:",size)
    comm = size
    now +=4

    size = rev(data [now:now+4].hex())
    print ("CommonPathSuffixOffset:",size)
    comm = size
    now +=4
    
    if (Vo == 1):
        # has VolumeID ＆ LocalBasePath
        size = rev(data [now:now+4].hex())
        # DriveType


        now += size

        # LocalBase
        path = data[now:now+comm-lb]
        print(path)
        now += comm-lb



    if (Co == 1):
        # has 
        print("Test")
    now+=1
    return now



def HasStringData(data,now):
    IsUnicode = 1
    print(data[now:now+1].hex())

    if 'IsUnicode' in (result['LinkFlags']):
        print('~ IsUnicode ~')
        IsUnicode = 2
    
    if 'HasName' in (result['LinkFlags']):
            size = rev(data [now:now+2].hex()) * IsUnicode
            now += 2
            print('NAME_STRING :',  data[now:now+size].decode('utf-16le'))
            now += size

    if 'HasRelativePath' in (result['LinkFlags']):
            size = rev(data [now:now+2].hex()) * IsUnicode
            now += 2
            print('RELATIVE_PATH :',  data[now:now+size].decode('utf-16le'))
            now += size

    if 'HasWorkingDir' in (result['LinkFlags']):
            size = rev(data [now:now+2].hex()) * IsUnicode
            now += 2
            print('WORKING_DIR :',  data[now:now+size].decode('utf-16le'))
            now += size

    if 'HasArguments' in (result['LinkFlags']):
            size = rev(data [now:now+2].hex()) * IsUnicode
            now += 2
            print('COMMAND_LINE_ARGUMENTS :',  data[now:now+size].decode('utf-16le'))
            now += size

    if 'HasIconLocation' in (result['LinkFlags']):
            size = rev(data [now:now+2].hex()) * IsUnicode
            now += 2
            print('ICON_LOCATION :',  data[now:now+size].decode('utf-16le'))
            now += size

    return now





def HasExtraData(data,now):
    print(len(data),now)

    # ExtraDataBlock
    while (now != len(data)-4):
        size = rev(data [now:now+4].hex())
        # detect BlockSignature
        if size == 0:
            break

        BlockSignature =  rev(data [now+4:now+8].hex())
        # print(hex(size),now)

        if (BlockSignature == 0xA0000002):
            print('ConsoleDataBlock :',data[now:now+size])

        elif (BlockSignature == 0xA0000004):
            print('ConsoleFEDataBlock :',data[now:now+size])

        elif (BlockSignature == 0xA0000006):
            print('DarwinDataBlock :',data[now:now+size])

        elif (BlockSignature == 0xA0000001):
            print('EnvironmentVariableDataBlock :',data[now:now+size])

        elif (BlockSignature == 0xA0000007):
            print('IconEnvironmentDataBlock :',data[now:now+size])

        elif (BlockSignature == 0xA000000B):
            print('KnownFolderDataBlock :',data[now:now+size])
        elif (BlockSignature == 0xA0000009):
            print('PropertyStoreDataBlock :',data[now:now+size])

        elif (BlockSignature == 0xA0000008):
            print('ShimDataBlock :',data[now:now+size])
        elif (BlockSignature == 0xA0000005):
            print('SpecialFolderDataBlock :',data[now:now+size])
            
        elif (BlockSignature == 0xA0000003):
            print('TrackerDataBlock :',data[now:now+size])

        elif (BlockSignature == 0xA000000C):
            print('VistaAndAboveIDListDataBlock :',data[now:now+size])
        
        else :
            print("!!! something worng in",hex(now),"!!!")
            exit()

        now += size


        # TerminalBlock
    print('TerminalBlock :',data [now:now+4].hex())
    return now



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("請輸入 .lnk 檔案路徑作為參數")
        sys.exit(1)

    lnk_path = sys.argv[1]

    with open(lnk_path, 'rb') as f:
        data = f.read()

    result = read_lnk_structure(data)
    for k, v in result.items():
        print(f"{k}: {v}")

    now = 76
    if 'HasLinkTargetIDList' in (result['LinkFlags']):
        print('--- has TargetIDList ---')
        now = LinkTargetIDList(data)
        print(now)

    if 'HasLinkInfo' in (result['LinkFlags']):
        print('--- has HasLinkInfo ---')
        now = HasLinkInfo(data,now)
        print(now)

    if ('HasLinkInfo'  or 'HasName' or 'HasRelativePath' or 'HasWorkingDir' or 'HasArguments' or 'HasIconLocation' in (result['LinkFlags'])):
        print('--- has StringData ---')
        now = HasStringData(data,now)
    print(now)

    if (now != hex(len(data))):
        print('--- has ExtraData ---')
        now = HasExtraData(data,now)
    
    print('--- End Structure ---')
