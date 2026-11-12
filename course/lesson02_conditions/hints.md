# คำใบ้บทที่ 2

คำใบ้แต่ละข้อมี 3 ระดับ เปิดทีละระดับ แล้วกลับไปลองเองก่อนเปิดระดับถัดไป

เปิดไฟล์นี้แบบ preview เพื่อให้คำใบ้ถูกพับไว้: กด `Cmd+Shift+V` (macOS) หรือ `Ctrl+Shift+V` (Windows)

## ข้อ 1

<details><summary>ระดับ 1</summary>

ข้อนี้ไม่ต้องใช้ `if` ผลของการเปรียบเทียบเป็น `True` หรือ `False` อยู่แล้ว และเก็บลงตัวแปรได้เลย ดูตัวอย่าง `is_big` ในบทเรียน

</details>

<details><summary>ระดับ 2</summary>

เครื่องหมายที่ถามว่าเท่ากันไหมคือ `==` สองตัว ถ้าใช้ `=` ตัวเดียว ตัวแปรจะได้ข้อความ `"โฉนด"` มาเก็บไว้แทนที่จะได้ `True`

</details>

<details><summary>ระดับ 3</summary>

`is_chanote = parcel_type ___ "โฉนด"`

</details>

## ข้อ 2

<details><summary>ระดับ 1</summary>

รูปแบบเดียวกับข้อ 1 เปลี่ยนเครื่องหมายเปรียบเทียบ

</details>

<details><summary>ระดับ 2</summary>

คำว่า "ตั้งแต่ 400 ขึ้นไป" รวมเลข 400 ด้วย ดูตารางเครื่องหมายในบทเรียนว่าตัวไหนรวมค่าที่เท่ากัน

</details>

<details><summary>ระดับ 3</summary>

`is_one_rai_or_more = total_sq_wa ___ 400`

</details>

## ข้อ 3

<details><summary>ระดับ 1</summary>

ดูตัวอย่างตัวแปร `note` ในหัวข้อ else ของบทเรียน ข้อนี้มีโครงเดียวกัน

</details>

<details><summary>ระดับ 2</summary>

ต้องมี 4 บรรทัด คือบรรทัด `if` บรรทัดสร้าง `size_note` ที่ย่อหน้า บรรทัด `else:` และบรรทัดสร้าง `size_note` อีกค่าที่ย่อหน้า

ถ้าตัวตรวจบอกว่าโค้ดไม่ได้สร้างตัวแปร แปลว่ามีทางหนึ่งที่ไม่ได้กำหนดค่าให้ `size_note`

</details>

<details><summary>ระดับ 3</summary>

```python
if total_sq_wa >= 400:
    size_note = "___"
else:
    size_note = "___"
```

</details>

## ข้อ 4

<details><summary>ระดับ 1</summary>

ดูตัวอย่าง `grade` ในหัวข้อ elif ของบทเรียน ข้อนี้มี 3 ทางเหมือนกัน

</details>

<details><summary>ระดับ 2</summary>

เริ่มจากกลุ่มเล็กสุดก่อน ถ้าไม่ใช่กลุ่มเล็ก บรรทัด `elif` ไม่ต้องตรวจซ้ำว่ามีตั้งแต่ 400 เพราะ Python มาถึงบรรทัดนั้นได้ก็ต่อเมื่อเงื่อนไขแรกไม่จริงแล้ว

ถ้าไม่ผ่านที่ค่า 400 หรือ 2000 พอดี ให้ดูว่าใช้ `<` หรือ `<=` ถูกตัวหรือยัง โจทย์บอกว่า "น้อยกว่า" ซึ่งไม่รวมค่าที่เท่ากัน

</details>

<details><summary>ระดับ 3</summary>

```python
if total_sq_wa < 400:
    size = "เล็ก"
elif total_sq_wa < ___:
    size = "___"
else:
    size = "___"
```

</details>

## ข้อ 5

<details><summary>ระดับ 1</summary>

มีสองเงื่อนไขที่ต้องจริงพร้อมกัน บทเรียนมีคำที่ใช้เชื่อมเงื่อนไขแบบนี้

</details>

<details><summary>ระดับ 2</summary>

เขียนการเปรียบเทียบสองอันให้สมบูรณ์ทีละอัน อันแรกเกี่ยวกับ `parcel_type` อันที่สองเกี่ยวกับ `total_sq_wa` แล้วเชื่อมด้วย `and` ไม่ต้องใช้ `if`

</details>

<details><summary>ระดับ 3</summary>

`is_large_chanote = parcel_type == "โฉนด" and total_sq_wa ___ ___`

</details>

## ข้อ 6

<details><summary>ระดับ 1</summary>

มีสองเงื่อนไข และจริงอันใดอันหนึ่งก็พอ

</details>

<details><summary>ระดับ 2</summary>

อ่านข้อควรระวังท้ายหัวข้อ and, or ในบทเรียน แต่ละฝั่งของ `or` ต้องเป็นการเปรียบเทียบที่สมบูรณ์ คือต้องมี `parcel_type ==` ทั้งสองฝั่ง

ข้อความที่เปรียบเทียบต้องตรงกับโจทย์ทุกตัวอักษร รวมถึงจุดและช่องว่าง แนะนำให้คัดลอกจากโจทย์

</details>

<details><summary>ระดับ 3</summary>

`is_ns3 = parcel_type == "นส.3" or parcel_type == "___"`

</details>

## ข้อท้าทาย 1

<details><summary>ระดับ 1</summary>

แตกโจทย์เป็นเงื่อนไขย่อยก่อน แล้วเขียนทีละอัน มีทั้งหมดกี่อันที่ต้องจริงพร้อมกัน

</details>

<details><summary>ระดับ 2</summary>

มี 5 การเปรียบเทียบ คือ `rai` ไม่ติดลบ `ngan` มีตั้งแต่ 0 `ngan` ไม่เกิน 3 `wa` มีตั้งแต่ 0 และ `wa` น้อยกว่า 100 ทั้งหมดเชื่อมกันด้วย `and`

</details>

<details><summary>ระดับ 3</summary>

`is_valid_area = rai >= 0 and ngan >= 0 and ngan <= 3 and wa >= ___ and wa ___ 100`

</details>

## ข้อท้าทาย 2

<details><summary>ระดับ 1</summary>

ข้อนี้ใช้ f-string จากบทที่ 1 กับตัวแปร `size` ที่สร้างไว้ในข้อ 4

</details>

<details><summary>ระดับ 2</summary>

ดูข้อความเป้าหมาย `แปลงขนาดกลาง (โฉนด)` คำว่า กลาง และ โฉนด คือส่วนที่มาจากตัวแปร ระหว่าง `แปลงขนาด` กับค่าของ `size` ไม่มีช่องว่าง

</details>

<details><summary>ระดับ 3</summary>

`description = f"แปลงขนาด{___} ({___})"`

</details>
