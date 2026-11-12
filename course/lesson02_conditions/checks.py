from checklib import Lesson

lesson = Lesson(2, "เงื่อนไข")


def area(value):
    return {"total_sq_wa": value}


@lesson.check("เปรียบเทียบว่าเท่ากันไหม")
def _(t):
    t.var_equals("is_chanote", True)
    t.var_equals("is_chanote", False, given={"parcel_type": "นส.3"})


@lesson.check("เปรียบเทียบมากกว่าหรือเท่ากับ")
def _(t):
    t.var_equals("is_one_rai_or_more", True)
    t.var_equals("is_one_rai_or_more", False, given=area(399))
    t.var_equals("is_one_rai_or_more", True, given=area(400))
    t.var_equals("is_one_rai_or_more", False, given=area(50))


@lesson.check("if และ else")
def _(t):
    t.var_equals("size_note", "ตั้งแต่ 1 ไร่ขึ้นไป")
    t.var_equals("size_note", "ไม่ถึง 1 ไร่", given=area(399))
    t.var_equals("size_note", "ตั้งแต่ 1 ไร่ขึ้นไป", given=area(400))


@lesson.check("if, elif และ else")
def _(t):
    t.var_equals("size", "กลาง")
    t.var_equals("size", "เล็ก", given=area(50))
    t.var_equals("size", "เล็ก", given=area(399))
    t.var_equals("size", "กลาง", given=area(400))
    t.var_equals("size", "กลาง", given=area(1999))
    t.var_equals("size", "ใหญ่", given=area(2000))
    t.var_equals("size", "ใหญ่", given=area(8942))


@lesson.check("เงื่อนไขที่ต้องจริงทั้งคู่")
def _(t):
    t.var_equals("is_large_chanote", False)
    t.var_equals("is_large_chanote", True, given={"parcel_type": "โฉนด", "total_sq_wa": 2075.5})
    t.var_equals("is_large_chanote", True, given={"parcel_type": "โฉนด", "total_sq_wa": 2000})
    t.var_equals("is_large_chanote", False, given={"parcel_type": "นส.3", "total_sq_wa": 2216})
    t.var_equals("is_large_chanote", False, given={"parcel_type": "นส.3", "total_sq_wa": 419})


@lesson.check("เงื่อนไขที่จริงอย่างใดอย่างหนึ่งก็พอ")
def _(t):
    t.var_equals("is_ns3", False)
    t.var_equals("is_ns3", True, given={"parcel_type": "นส.3"})
    t.var_equals("is_ns3", True, given={"parcel_type": "น.ส.3 ก."})
    t.var_equals("is_ns3", False, given={"parcel_type": "ท.ค."})


@lesson.check("ตรวจรูปแบบเนื้อที่", challenge=True)
def _(t):
    t.var_equals("is_valid_area", True)
    t.var_equals("is_valid_area", True, given={"rai": 0, "ngan": 0, "wa": 0})
    t.var_equals("is_valid_area", True, given={"rai": 1, "ngan": 3, "wa": 99.9})
    t.var_equals("is_valid_area", False, given={"rai": 3, "ngan": 4, "wa": 54})
    t.var_equals("is_valid_area", False, given={"rai": 3, "ngan": 3, "wa": 100})
    t.var_equals("is_valid_area", False, given={"rai": -1, "ngan": 0, "wa": 0})
    t.var_equals("is_valid_area", False, given={"rai": 1, "ngan": -1, "wa": 0})
    t.var_equals("is_valid_area", False, given={"rai": 1, "ngan": 0, "wa": -5})


@lesson.check("ประกอบข้อความจากผลของเงื่อนไข", challenge=True)
def _(t):
    t.var_equals("description", "แปลงขนาดกลาง (โฉนด)")
    t.var_equals("description", "แปลงขนาดเล็ก (นส.3)", given={"parcel_type": "นส.3", "total_sq_wa": 50})
    t.var_equals("description", "แปลงขนาดใหญ่ (น.ส.3 ก.)", given={"parcel_type": "น.ส.3 ก.", "total_sq_wa": 8942})
