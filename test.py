#!/usr/bin/env python3

import asset
import vdk

# CT to CSV
ct = asset.CT("test/ASSET/ASSET/ItemInfo.ct")
ct.verbose = True
csv = asset.CSV("test/ASSET/ASSET/copy/ItemInfo.csv")
csv.verbose = True

data = ct.read()
print(ct.header)
print(ct.types)
print(ct.rows[0])
csv.write(data)

# CSV to CT
csv = asset.CSV("test/ASSET/ASSET/copy/Attendance.csv")
csv.verbose = True
ct = asset.CT("./test/ASSET/ASSET/Attendance.ct")
ct.verbose = True

data = csv.read()
print(csv.header)
print(csv.types)
print(csv.rows[0])
ct.write(data)

# VDK extract
vdisk = vdk.VDK("test/1/STRING.VDK")
vdisk.verbose = True
vdisk.unpack()

# VDK insert
vdisk = vdk.VDK("test/1/STRING_TEST.VDK")
vdisk.verbose = True
vdisk.pack("test/1/STRING")
