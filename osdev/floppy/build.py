#!/usr/bin/python
import os
import subprocess

def fix_stage1_size():
  stage2_size = os.stat("stage2.bin").st_size
  stage2_size = (stage2_size + 511) / 512
  if 255 <= stage2_size:
    raise Exception("stage2 zbyt dlugi")
  with open("stage1.bin", "rb+") as f:
    d = f.read()
    idx = d.index("\xb0\xcc\x90\x90")
    d = bytearray(d)
    d[idx + 1] = stage2_size
    f.seek(0)
    f.write(d)

cmds_to_run = [
  "/./home/uzytkownik/praca/github/nauka/fasm/fasm stage2.asm",
  "/./home/uzytkownik/praca/github/nauka/fasm/fasm stage1.asm",
  fix_stage1_size
]

files_to_img = [
  "stage1.bin",
  "stage2.bin"
]

for cmd in cmds_to_run:
  if type(cmd) is str:
    print "Wykonuje: ", cmd
    print subprocess.check_output(cmd, shell=True)
  else:
    print "Wykonuje: ", cmd.func_name
    cmd()
  
buf = []
for fn in files_to_img:
  with open(fn, "rb") as f:
    d = f.read()
    buf.append(d)
    if 0 == len(d) % 512:
      continue
    padding_size = 512 - len(d) % 512
    buf.append("\0" * padding_size)
    
with open("floppy.bin", "wb") as f:
  f.write(''.join(buf))

