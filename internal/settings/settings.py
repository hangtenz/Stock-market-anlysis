import string
import datetime

bar_chart = set([
        'รายได้รวม',
        'กำไรต่อหุ้น',
        'หนี้สินระยะยาว',
        'อัตราการจ่ายเงินปันผล'
])

line_chart = set([
        'อัตรากำไรขั้นต้น',
        'อัตราค่าใช้จ่ายในการขายและบริหาร',
        'หนี้สินต่อส่วนของผู้ถือหุ้น',
        'อัตราผลตอบแทนผู้ถือหุ้น'
])

no_plot_chart = set([
    'ราคา',
     'อัตราส่วนราคาต่อกำไร',
     'เงินปันผลต่อหุ้น'
])

column_mapping = list(string.ascii_uppercase) + list(map(lambda x: 'A'+x, string.ascii_uppercase))
current_year = str(datetime.date.today().year)
last_year = str(int(current_year) - 1)