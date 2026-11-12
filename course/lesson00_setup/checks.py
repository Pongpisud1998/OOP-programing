from checklib import CheckFailed, Lesson

lesson = Lesson(0, "เตรียมเครื่องและโปรแกรมแรก")


@lesson.check("แสดงข้อความ สวัสดี Python")
def _(t):
    t.output_has_line("สวัสดี Python")


@lesson.check("แสดงชื่อของตัวเอง")
def _(t):
    t.output_has_line_starting("ฉันชื่อ", "ชื่อเล่นของเรา")


@lesson.check("แสดงตัวเลข 40")
def _(t):
    t.output_has_line("40")


@lesson.check("แสดงข้อความและตัวเลขใน print เดียว")
def _(t):
    t.output_has_line("จำนวนแปลง: 40")


@lesson.check("แก้บรรทัดที่ผิดให้รันได้")
def _(t):
    t.output_has_line("แก้ฉันให้รันได้")


@lesson.check("ปิดการทำงานของบรรทัดด้วย comment")
def _(t):
    t.output_lacks("บรรทัดนี้ต้องไม่แสดง")
    if "บรรทัดนี้ต้องไม่แสดง" not in t.path.read_text(encoding="utf-8"):
        raise CheckFailed("บรรทัดนั้นถูกลบไปแล้ว โจทย์ให้เก็บบรรทัดไว้แต่ทำให้ไม่ทำงาน ให้พิมพ์กลับมาแล้วลองใหม่")


@lesson.check("แสดงเส้นคั่น = 30 ตัว", challenge=True)
def _(t):
    t.output_has_line("=" * 30)
