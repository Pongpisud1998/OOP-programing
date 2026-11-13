#การเปรียบเทียบให้ผลเป็น True หรือ False
area = 1554
print(area > 1000)
print(area > 2000)

is_big = area > 1000
print(is_big)


#if: ทำเมื่อเงื่อนไขเป็นจริง
area = 1554
if area > 1000:
    print("แปลงนี้เกิน 1000 ตารางวา")

print("จบโปรแกรม")


#else: ทำเมื่อเงื่อนไขไม่จริง
if area > 1000:
    note = "เกิน 1000 ตารางวา"
else:
    note = "ไม่เกิน 1000 ตารางวา"
print(note)


#elif: มีมากกว่าสองทาง
score = 72

if score >= 80:
    grade = "ดีมาก"
elif score >= 50:
    grade = "ผ่าน"
else:
    grade = "ไม่ผ่าน"

print(grade)


#and, or: รวมหลายเงื่อนไข
age = 20
has_ticket = True

can_enter = age >= 18 and has_ticket
print(can_enter)


#ข้อควรระวัง: แต่ละฝั่งของ and และ or ต้องเป็นการเปรียบเทียบที่สมบูรณ์ในตัวเอง
color = "แดง"

print(color == "แดง" or color == "ส้ม")
print(color == "แดง" or "ส้ม")