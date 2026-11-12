# คำใบ้บทที่ 0

คำใบ้แต่ละข้อมี 3 ระดับ เปิดทีละระดับ แล้วกลับไปลองเองก่อนเปิดระดับถัดไป

เปิดไฟล์นี้แบบ preview เพื่อให้คำใบ้ถูกพับไว้: กด `Cmd+Shift+V` (macOS) หรือ `Ctrl+Shift+V` (Windows)

## ข้อ 1

<details><summary>ระดับ 1</summary>

ดูตัวอย่างคำสั่ง `print` ในบทเรียน ข้อนี้ใช้รูปแบบเดียวกันทุกอย่าง เปลี่ยนแค่ข้อความ

</details>

<details><summary>ระดับ 2</summary>

ข้อความต้องอยู่ในเครื่องหมายคำพูด และเครื่องหมายคำพูดต้องอยู่ในวงเล็บของ `print`

</details>

<details><summary>ระดับ 3</summary>

รูปแบบคือ `print("___")` เติมข้อความที่โจทย์ต้องการลงในช่องว่าง ตัวตรวจเทียบทุกตัวอักษร รวมถึงช่องว่างระหว่างคำ

</details>

## ข้อ 2

<details><summary>ระดับ 1</summary>

เหมือนข้อ 1 แต่ข้อความเป็นของเราเอง

</details>

<details><summary>ระดับ 2</summary>

ข้อความต้องขึ้นต้นด้วยคำว่า `ฉันชื่อ` ตามด้วยช่องว่าง แล้วตามด้วยชื่อ ทั้งหมดอยู่ในเครื่องหมายคำพูดคู่เดียว

</details>

<details><summary>ระดับ 3</summary>

`print("ฉันชื่อ ___")`

</details>

## ข้อ 3

<details><summary>ระดับ 1</summary>

ตัวเลขใส่ในวงเล็บของ `print` ได้โดยตรง

</details>

<details><summary>ระดับ 2</summary>

ข้อนี้ไม่มีเครื่องหมายคำพูดเลย

</details>

<details><summary>ระดับ 3</summary>

`print(___)` เติมตัวเลขลงในช่องว่าง

</details>

## ข้อ 4

<details><summary>ระดับ 1</summary>

อ่านหัวข้อ "คำสั่ง print" ตรงที่พูดถึงการแสดงหลายอย่างในครั้งเดียว

</details>

<details><summary>ระดับ 2</summary>

ในวงเล็บมีสองอย่างคั่นด้วย `,` อย่างแรกเป็นข้อความ อย่างที่สองเป็นตัวเลข Python เติมช่องว่างระหว่างสองอย่างให้เอง จึงไม่ต้องพิมพ์ช่องว่างท้ายข้อความ

</details>

<details><summary>ระดับ 3</summary>

`print("จำนวนแปลง:", ___)`

</details>

## ข้อ 5

<details><summary>ระดับ 1</summary>

หลังลบ `#` แล้วรัน ให้อ่าน error จากล่างขึ้นบนตามที่บทเรียนสอน มันบอกชนิดของปัญหาเป็นภาษาอังกฤษ ลองแปลคำว่า unterminated

</details>

<details><summary>ระดับ 2</summary>

ถ้า error เป็น `IndentationError: unexpected indent` แปลว่ายังมีช่องว่างเหลืออยู่หน้า `print` ให้ลบจน `print` ชิดซ้ายสุด

ถ้า error เป็น `SyntaxError: unterminated string literal` ให้นับเครื่องหมายคำพูดในบรรทัดนั้น

</details>

<details><summary>ระดับ 3</summary>

เครื่องหมายคำพูดต้องมาเป็นคู่ คือเปิดหนึ่งตัวและปิดหนึ่งตัว บรรทัดนี้มีตัวเปิดแต่ไม่มีตัวปิด ให้เติมตัวปิดก่อนวงเล็บปิด

</details>

## ข้อ 6

<details><summary>ระดับ 1</summary>

มีเครื่องหมายหนึ่งตัวที่ทำให้ Python ข้ามทั้งบรรทัด บทเรียนมีหัวข้อของมันโดยเฉพาะ

</details>

<details><summary>ระดับ 2</summary>

ข้อ 5 เราเพิ่งลบเครื่องหมายนี้ออกเพื่อให้บรรทัดทำงาน ข้อนี้ทำกลับกัน

</details>

<details><summary>ระดับ 3</summary>

พิมพ์ `#` ไว้หน้าสุดของบรรทัดนั้น

</details>

## ข้อท้าทาย

<details><summary>ระดับ 1</summary>

รัน `print("ab" * 3)` ตามที่โจทย์แนะนำ แล้วดูว่าเครื่องหมาย `*` ทำอะไรกับข้อความ

</details>

<details><summary>ระดับ 2</summary>

ข้อความคูณด้วยตัวเลขได้ ผลคือข้อความเดิมซ้ำกันตามจำนวนนั้น

</details>

<details><summary>ระดับ 3</summary>

`print("=" * ___)`

</details>
