from checklib import Lesson

lesson = Lesson(1, "ค่าและตัวแปร")

# Starting values for other real parcels. Expected results are written as plain
# numbers so this file does not give away the formulas.
SMALL = {"rai": 0, "ngan": 0, "wa": 50}
MIXED = {"rai": 1, "ngan": 2, "wa": 3}
BIG = {"rai": 12, "ngan": 0, "wa": 85}


@lesson.check("สร้างตัวแปร parcel_count")
def _(t):
    t.var_equals("parcel_count", 40)


@lesson.check("แปลงไร่เป็นตารางวา")
def _(t):
    t.var_equals("rai_in_sq_wa", 1200)
    t.var_equals("rai_in_sq_wa", 400, given=MIXED)
    t.var_equals("rai_in_sq_wa", 4800, given=BIG)


@lesson.check("แปลงงานเป็นตารางวา")
def _(t):
    t.var_equals("ngan_in_sq_wa", 300)
    t.var_equals("ngan_in_sq_wa", 200, given=MIXED)
    t.var_equals("ngan_in_sq_wa", 0, given=BIG)


@lesson.check("เนื้อที่รวมเป็นตารางวา")
def _(t):
    t.var_equals("total_sq_wa", 1554)
    t.var_equals("total_sq_wa", 603, given=MIXED)
    t.var_equals("total_sq_wa", 50, given=SMALL)
    t.var_equals("total_sq_wa", 4885, given=BIG)


@lesson.check("เนื้อที่รวมเป็นตารางเมตร")
def _(t):
    t.var_equals("total_sq_m", 6216)
    t.var_equals("total_sq_m", 2412, given=MIXED)
    t.var_equals("total_sq_m", 200, given=SMALL)


@lesson.check("ประกอบข้อความ label")
def _(t):
    t.var_equals("label", "โฉนด เลขที่ 11304")
    t.var_equals("label", "นส.3 เลขที่ 77", given={"parcel_type": "นส.3", "parcel_no": 77})


@lesson.check("ประกอบข้อความ area_text")
def _(t):
    t.var_equals("area_text", "3 ไร่ 3 งาน 54 ตารางวา")
    t.var_equals("area_text", "12 ไร่ 0 งาน 85 ตารางวา", given=BIG)


@lesson.check("แยกตารางวาเป็น ไร่ งาน ตารางวา", challenge=True)
def _(t):
    cases = [(2126, 5, 1, 26), (399, 0, 3, 99), (400, 1, 0, 0), (50, 0, 0, 50)]
    for area, rai, ngan, wa in cases:
        given = None if area == 2126 else {"area_sq_wa": area}
        t.var_equals("rai_part", rai, given=given)
        t.var_equals("ngan_part", ngan, given=given)
        t.var_equals("wa_part", wa, given=given)
