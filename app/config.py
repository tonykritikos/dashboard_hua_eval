import datetime

columns = ['qid', 'qlastpage', 'q1_attendslectures', 'q2_coursehaslabs', 'q2b_attendslabs',
           'q3_cleargoalslectures', 'q4_cleargoalslabs', 'q5_studymaterial',
           'q6_tutorinteresting',
           'q7_tutorquestions', 'q8_tutorreachable', 'q9_tutorexplains',
           'q10_tutorontime', 'q11_hasassistant', 'q11b_assistanthelps',
           'q12_materialcovered',
           'q13_tutororganised', 'q14_evaluationcriteria', 'opencomments', 'courseid',
           'qyear', 'qseason']
median_columns = ['q3_cleargoalslectures', 'q4_cleargoalslabs', 'q5_studymaterial',
                  'q6_tutorinteresting',
                  'q7_tutorquestions', 'q8_tutorreachable', 'q9_tutorexplains',
                  'q10_tutorontime', 'q11b_assistanthelps',
                  'q12_materialcovered',
                  'q13_tutororganised', 'q14_evaluationcriteria']
median_columns_plus_year = ['q3_cleargoalslectures', 'q4_cleargoalslabs', 'q5_studymaterial',
                     'q6_tutorinteresting',
                     'q7_tutorquestions', 'q8_tutorreachable', 'q9_tutorexplains',
                     'q10_tutorontime', 'q11b_assistanthelps',
                     'q12_materialcovered',
                     'q13_tutororganised', 'q14_evaluationcriteria', 'qyear']
median_columns_plus_courseid = ['q3_cleargoalslectures', 'q4_cleargoalslabs', 'q5_studymaterial',
                       'q6_tutorinteresting',
                       'q7_tutorquestions', 'q8_tutorreachable', 'q9_tutorexplains',
                       'q10_tutorontime', 'q11b_assistanthelps',
                       'q12_materialcovered',
                       'q13_tutororganised', 'q14_evaluationcriteria', 'courseid']


year = int((datetime.datetime.now().strftime('%Y')))
