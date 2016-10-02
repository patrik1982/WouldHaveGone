§Source : https://github.com/WFoundation/WF.Compiler

File format of GWC files:

    @0000:                          ; Signature
        BYTE     0x02               ; Version
        BYTE     0x0a               ; 2.10 or 2.11
        BYTE     "CART"
        BYTE     0x00

    @0007:
        USHORT   NumberOfObjects    ; Number of objects ("media files") in cartridge:

    @0009:
        ; References to individual objects in cartridge.
        ; Object 0 is always Lua bytecode for cartridge.
        ; There is exactly [number_of_objects] blocks like this:
        repeat <NumberOfObjects> times
        {
            USHORT   ObjectID       ; Distinct ID for each object, duplicates are forbidden
            INT      Address          ; Address of object in GWC file
        }

    @xxxx:                          ; 0009 + <NumberOfObjects> * 0006 bytes from begining
        ; Header with all important informations for this cartridge
        INT      HeaderLength       ; Length of information header (following block):

        DOUBLE   Latitude           ; N+/S-
        DOUBLE   Longitude          ; E+/W-
        DOUBLE   Altitude           ; Meters

        LONG     Date of creation   ; Seconds since 2004-02-10 01:00:00

        ; MediaID of icon and splashscreen
        SHORT    ObjectID of splashscreen    ; -1 = without splashscreen/poster
        SHORT    ObjectID of icon            ; -1 = without icon

        ASCIIZ   TypeOfCartridge             ; "Tour guide", "Wherigo cache", etc.
        ASCIIZ   Player                      ; Name of player downloaded cartridge
        LONG     PlayerID                    ; ID of player in the Groundspeak database

        ASCIIZ   CartridgeName               ; "Name of this cartridge"
        ASCIIZ   CartridgeGUID
        ASCIIZ   CartridgeDescription        ; "This is a sample cartridge"
        ASCIIZ   StartingLocationDescription ; "Nice parking"
        ASCIIZ   Version                     ; "1.2"
        ASCIIZ   Author                      ; Author of cartridge
        ASCIIZ   Company                     ; Company of cartridge author
        ASCIIZ   RecommendedDevice           ; "Garmin Colorado", "Windows PPC", etc.

        INT      Length                      ; Length of CompletionCode
        ASCIIZ   CompletionCode              ; Normally 15/16 characters

    @address_of_FIRST_object (with ObjectID = 0):
        ; always Lua bytecode
        INT      Length                      ; Length of Lua bytecode
        BYTE[Length]    ContentOfObject      ; Lua bytecode

    @address_of_ALL_OTHER_objects (with ID > 0):
        BYTE     ValidObject
        if (ValidObject == 0)
        {
            ; when ValidObject == 0, it means that object is DELETED and does
            ; not exist in cartridge. Nothing else follows.
        }
        else
        {
            ; Object type: 1=bmp, 2=png, 3=jpg, 4=gif, 17=wav, 18=mp3, 19=fdl, 
            ; 20=snd, 21=ogg, 33=swf, 49=txt, other values have unknown meaning
            INT           ObjectType               
            INT           Length
            BYTE[Length]  content_of_object
        }

    @end

    Varibles

        BYTE   = unsigned char (1 byte)
        SHORT  = signed short (2 bytes, little endian)
        USHORT = unsigned short (2 bytes, little endian)
        INT    = signed long (4 bytes, little endian)
        UINT   = unsigned long (4 bytes, little endian)
        LONG   = signed long (8 bytes, little endian)
        DOUBLE = double-precision floating point number (8 bytes)
        ASCIIZ = zero-terminated string ("hello world!", 0x00)
