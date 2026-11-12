"""ตรวจแบบฝึกหัด

วิธีใช้ (รันจากโฟลเดอร์ course):
    python check.py 0        ตรวจบทที่ 0
    python check.py 1        ตรวจบทที่ 1
"""

import sys

from checklib import main

if __name__ == "__main__":
    sys.exit(main(sys.argv))
