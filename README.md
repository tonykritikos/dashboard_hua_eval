# HUA evaluation dashboard

### Summary 
This dissertation concerns the construction of an online dashboard that presents basic elements of a data set using graphs. The object of those graphs is data stored in a secure database of Harokopio University and are anonymous student evaluations of the courses and teachers who taught them each semester. The purpose of these graphs is to give an overall picture of the quality of the courses and the effectiveness of the teachers in them, for each course and each year. The significance of this dashboard is as important as the evaluations: Just as student evaluations must be there to highlight the pros and cons of teachers and, consequently, of the lessons, it is just as important to have a system that processes the data and produces an overview of these evaluations. This page, with the appropriate configuration, can be used by Harokopio University to present the image that students have of the administrative staff and the courses. The present work was the opportunity for the acquaintance with the design of dashboards but also their implementation with relevant libraries of the python language.

### User Interface

When entering the application the user sees two dropdown lists and below them there are five tabs. The top dropdown list contains the courses and the bottom one contains the years. The first three tabs have plots which are grouped by specific perspectives of either the student, the lesson or the teacher. The two last tabs have more general content and have plots that show the course's grade through the years (based on a question that is chosen from the dropdown list from within the tab) or the overall rank of a lesson at a specific year. 

### Main files

#### config.py

Contains labels and verbal translates of variables, as well as some configuration elements which are called in the basic program. The reason they exist in a separate file is so that the verbals are not hardcoded in each graph and can be changed (or added) without having to write many lines of code, as well as so that the configurations are declared in a variable and change en masse within the program. More specifically, there are the following statements:

- <b>columns</b>: all columns in the ratings table
- <b>mean_columns</b>: all columns corresponding to type 1 to 5 rating questions used for graphs on average
- <b>dict_mean_columns</b>: all columns of mean_columns with their corresponding words, used for the internal folding list of the fourth tab
- <b>dict_columns</b>: All columns in the table mapped to words (along with additional columns and words that can be added to extensions of this dissertation)
- <b>mean_columns_plus_year</b>: all columns used for averages along with the column showing the year, used for grouping on the fourth tab
- <b>bar_labels</b>: labels shown on the axes of each bar chart of the first three tabs
- <b>year</b>: the "present year" which is calculated by the following part of the code:
 ``` python
year = int ((datetime.datetime.now (). strftime ('% Y')))
```
&nbsp;&nbsp;&nbsp;&nbsp;which takes the current date, keeps the year and assigns it to variable year.
- <b>height</b> and <b>width</b>: variables of graph size
- <b>bar_x_range</b>: the range that the x-axis of the bar graphs can take
- <b>bar_y_range</b>: the range that the y-axis of the bar graphs can take
- <b>def titles</b>: a method that takes the column id as a variable and returns the corresponding evaluation word. In the return of the method we see the following statement:
``` python
  '<br>' .join (textwrap.wrap (y))
```
&nbsp;&nbsp;&nbsp;&nbsp;which is used to wrap words in graphs so that they do not appear on top of other graphs or off-page.



#### dashboard.py

This is the basic program that implements the dashboard.
The main parts of the implementation are the following:

- <b>Imports</b>: All classes, files, and anything else the dashboard needs to run.

- <b>Error handling and suppressing block</b>: The piece of code that checks and manages any errors.

- <b>Styling and configuration block</b>: The piece of code that initializes the app and its basic appearance

- <b>def sql_query</b>: the method used to connect to the database. There, the respective command is given, which will run in the database to return the data needed.

- <b>courses</b>: the variable to which the course words are assigned their id

- <b>df</b>: the basic dataframe to which all data entering from the database is assigned. Based on this, dataframes are created in each tab which are properly configured based on the requirements of each graph.

- <b>app</b>: The app is the whole layout that we see on the browser page

- <b>def first_tab</b>, <b>def second_tab</b>, <b>def third_tab</b>: The part that contains the graphs of the first, second and third tab respectively. An important feature is the dataframe statement:
``` python
first_tab_df = df [(df ['courseid'] == courseid) & (df ['qyear'] == syear)]
second_tab_df = df [(df ['courseid'] == courseid) & (df ['qyear'] == syear)]
third_tab_df = df [(df ['courseid'] == courseid) & (df ['qyear'] == syear)]
```
&nbsp;&nbsp;&nbsp;&nbsp;which are created from the basic dataframe, but the course code is selected from the drop-down list of courses and also the year is selected from the drop-down list of years

- <b>def fourth_tab</b>: The part that contains the graph of the fourth tab. The dataframe is created only by selecting the course:
``` python
fourth_tab_df = df [(df ['courseid'] == courseid)]
```
&nbsp;&nbsp;&nbsp;&nbsp;and there is the following configuration:
``` python
px.line (fourth_tab_df [config.mean_columns_plus_year] .groupby (['qyear']). mean (), y = mean_column, title = "Mean", height = config.height, width = config.width)
```
&nbsp;&nbsp;&nbsp;&nbsp;where:
  1. <b>config.mean_columns_plus_year</b>: uses the mean_columns_per_year declared in config.py for this very graph
  2. <b>groupby (['qyear'])</b>: gets grouped by year
  3. <b>mean ()</b>: the average per column is displayed
  4. <b>y = mean_column</b>: y axis is the selected mean mean_column of the internal drop-down list

- <b>def fifth_tab</b>: The part that contains the table of the fifth tab. The dataframe is created only by selecting the year:
``` python
fifth_tab_df = df [(df ['qyear'] == syear)]
```
&nbsp;&nbsp;&nbsp;&nbsp;An additional column named 'Mean' is created in this dataframe as follows:
``` python
fifth_tab_df ['Mean'] = fifth_tab_df.loc [:, config.mean_columns] .mean (axis = 1, skipna = True)
```
&nbsp;&nbsp;&nbsp;&nbsp;which is calculated from the columns in mean_columns and returns the average of the row (so the axis value is 1) \
&nbsp;&nbsp;&nbsp;&nbsp;Then the course variables are replaced by their verbal words by the following:
``` python
for name, number in courses:
fifth_tab_df ['courseid'] = fifth_tab_df ['courseid']. replace (number, name)
```
&nbsp;&nbsp;&nbsp;&nbsp;And finally comes the general average per lesson as follows:
``` python
fifth_tab_df.groupby (['courseid'], as_index = False) .mean (). round (2) .sort_values ('Mean', ascending = False) .to_dict ('records')
```
- where:
  1. <b>groupby (['courseid'])</b>: data is grouped by lesson
  2. <b>mean ()</b>: the (now general) average per lesson comes out
  3. <b>round (2)</b>: the average is rounded to two decimal places
  4. <b>sort_values ('Mean', ascending = False)</b>: scores are sorted from highest to lowest 

### Possible future extensions

This page can be enriched with more graphs and information about the ratings. The latest evaluations also contain some questions about elective courses, as well as some questions about distance learning or asynchronous education. The dict_columns of the config.py file will be useful there. In this file , in addition to all the ids of the columns used in the program and their corresponding verbal words, there are other questions from the ratings that do not exist as columns in the database. However they have deliberately stayed in config.py and have been given some dummy ids (from extra1 to extra11 and from tele1 to tele6). Therefore, in an extension of the page functionality, another table can be created in the database, with additional questions and some additional tabs and graphs can be created with the already config.py configurations.
An additional extension of the dashboard will be done either by extending the already existing evaluation with additional questions, or by creating a separate evaluation that includes questions about the administrative staff, the facilities, the University environment, etc. Given the roles in which this dashboard is designed, there are users (eg external evaluators or committees) to whom such evaluations, for University characteristics, would be interesting and useful for their research and their own evaluations to the Universities. 