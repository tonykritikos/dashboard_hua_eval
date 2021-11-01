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
dict_median_columns = [("q3", "q3_cleargoalslectures"),
                       ("q4", "q4_cleargoalslabs"),
                       ("q5", "q5_studymaterial"),
                       ("q6", "q6_tutorinteresting"),
                       ("q7", "q7_tutorquestions"),
                       ("q8", "q8_tutorreachable"),
                       ("q9", "q9_tutorexplains"),
                       ("q10", "q10_tutorontime"),
                       ("q11", "q11b_assistanthelps"),
                       ("q12", "q12_materialcovered"),
                       ("q13", "q13_tutororganised"),
                       ("q14", "q14_evaluationcriteria")]
median_columns_plus_year = ['q3_cleargoalslectures', 'q4_cleargoalslabs', 'q5_studymaterial',
                            'q6_tutorinteresting',
                            'q7_tutorquestions', 'q8_tutorreachable', 'q9_tutorexplains',
                            'q10_tutorontime', 'q11b_assistanthelps',
                            'q12_materialcovered',
                            'q13_tutororganised', 'q14_evaluationcriteria', 'qyear']
year = int((datetime.datetime.now().strftime('%Y')))
