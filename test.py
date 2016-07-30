#!/usr/bin/env python3

import asset
import vdk

# CT to TSV
ct = asset.CT("test/ASSET/ASSET/ItemInfo.ct")
ct.verbose = True
tsv = asset.TSV("test/ASSET/ASSET/copy/ItemInfo.tsv")
tsv.verbose = True

data = ct.read()
print(ct.header)
print(ct.types)
print(ct.rows[0])
tsv.write(data)

# TSV to CT
tsv = asset.TSV("test/ASSET/ASSET/copy/ItemInfo.tsv")
tsv.verbose = True
ct = asset.CT("./test/ASSET/ASSET/ItemInfo.ct")
ct.verbose = True

data = tsv.read()
print(tsv.header)
print(tsv.types)
print(tsv.rows[0])
ct.write(data)

# VDK extract
vdisk = vdk.VDK("test/1/STRING.VDK")
vdisk.verbose = True
vdisk.unpack()

# VDK insert
vdisk = vdk.VDK("test/1/STRING_TEST.VDK")
vdisk.verbose = True
vdisk.pack("test/1/STRING")
