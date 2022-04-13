# 
# Bianca Atienza 674064582
# CS 341 Project 1 (SQL + Python)
# Descrition: Following the pdf, asked to perform series of queries for 9 commands and using matplotlib to plot the graphs
# Spring 2022
#

import sqlite3
import matplotlib.pyplot as figure


########################################################### 
# first command - single query to match userInput to station names using LIKE and then loop for printing out results
def firstCommand(userInput, dbConn):
  dbCursor = dbConn.cursor()
  print()
  userInput = input("Enter partial station name (wildcards _ and %): ");
  sql = """Select Station_ID, Station_Name from Stations where Station_Name like ? Order by Station_Name"""
  dbCursor.execute(sql, [userInput])
  row = dbCursor.fetchall();
  if(len(row) > 0 ):
    for i in row:
      print(i[0], ":", i[1])
    print()
  else:
    print("**No stations found...")
    print()


###########################################################
# second command - two queries total, main one is to list all station names and its corresponding number of riders, use join and loop the row to print out results and %
def secondCommand(dbConn):
  dbCursor = dbConn.cursor()
  print("** ridership all stations **")
  print()
  dbCursor.execute("Select Station_Name, sum(Num_Riders) From Ridership inner join Stations on Stations.Station_ID = Ridership.Station_ID Group by Station_Name Order by Station_Name")
  row = dbCursor.fetchall();
  dbCursor.execute("Select sum(Num_Riders) From Ridership;")
  row2 = dbCursor.fetchone();
  # percent = ((row[1]/row2[0]) * 100);
  for i in row:
    percent = ((i[1]/row2[0]) * 100);
    print(i[0], ":", f"{i[1]:,}", f"({percent:0.2f}%)")
  print()
  


###########################################################
# third command - similar to the second command, 2 queries and the main one uses where and join to find station names but to p10 using limit, loop to print results
def thirdCommand(dbConn):
  dbCursor = dbConn.cursor()
  print("** top-10 stations **")
  print()
  dbCursor.execute("Select Station_Name, sum(Num_Riders) From Ridership join Stations on Ridership.Station_ID = Stations.Station_ID Group by Station_Name Order by sum(Num_Riders) desc Limit 10;")
  row = dbCursor.fetchall();
  dbCursor.execute("Select sum(Num_Riders) From Ridership;")
  row2 = dbCursor.fetchone();
  for i in row:
    percent = ((i[1]/row2[0]) * 100);
    print(i[0], ":", f"{i[1]:,}", f"({percent:0.2f}%)")
  print()
    

###########################################################
# fourth command - like 2 and 3, total of 2 queries use join and like and order by to find station names and num riders, loop through row to print
def fourthCommand(dbConn):
  dbCursor = dbConn.cursor()
  print("** least-10 stations **")
  print()
  dbCursor.execute("Select Station_Name, sum(Num_Riders) From Ridership join Stations on Ridership.Station_ID = Stations.Station_ID Group by Station_Name Order by sum(Num_Riders) asc Limit 10;")
  row = dbCursor.fetchall();
  dbCursor.execute("Select sum(Num_Riders) From Ridership;")
  row2 = dbCursor.fetchone();
  for i in row:
    percent = ((i[1]/row2[0]) * 100);
    print(i[0], ":", f"{i[1]:,}", f"({percent:0.2f}%)")
  print()


###########################################################
# fifth command - single query that includes order by and join to find Stop Name, Dir, ADA and check if there exists a line, loop to print results
def fifthCommand(userInput, dbConn):
  dbCursor = dbConn.cursor()
  print()
  userInput = input("Enter a line color (e.g. Red or Yellow): ");
  sql = """Select Stop_Name, Direction, ADA From Stops
  join StopDetails on Stops.Stop_ID = StopDetails.Stop_ID
  join Lines on StopDetails.Line_ID = Lines.Line_ID
  where Color like ?
  Order by Stop_Name asc;"""
  dbCursor.execute(sql, [userInput])
  row = dbCursor.fetchall();
  if(len(row) > 0):
    for i in row:
      if(i[2] == 1):
        print(i[0], ": direction =", f"{i[1]}", "(accessible? yes)")
      else:
        print(i[0], ": direction =", f"{i[1]}", "(accessible? no)")
    print()
  else:
    print("**No such line...")
    print()


########################################################### 
# sixth command - single query consists of where, group by and order by to find all ridership total every month, loop to print results and follow pdf to plot
def sixthCommand(userInput, dbConn):
  dbCursor = dbConn.cursor()
  print("** ridership by month **")
  dbCursor.execute("select strftime('%m', date(Ride_Date)), sum(Num_Riders) From Ridership where strftime('%m', date(Ride_Date)) between '01' and '12' Group by strftime('%m', date(Ride_Date)) Order by strftime('%m', date(Ride_Date)) asc")
  row = dbCursor.fetchall();
  for i in row:
    print(i[0], ":", f"{i[1]:,}")
  print()
  userInput = input("Plot? (y/n) ")
  if(userInput == 'y'):
    x = []
    y = []
    for j in row:
      yNum = round(j[1]/(10**8), 1)
      x.append(j[0])
      y.append(yNum)
    figure.xlabel("month")
    figure.ylabel("number of riders (x * 10^8)")
    figure.title("monthly ridership")
    figure.plot(x,y)
    figure.show()
  print()


########################################################### 
# seventh command - very similar to 6, following the same format fo code, only major difference is instead of months change to strftime('%Y') for year, plot
def seventhCommand(userInput, dbConn):
  dbCursor = dbConn.cursor()
  print("** ridership by year **")
  dbCursor.execute("select strftime('%Y', date(Ride_Date)), sum(Num_Riders) From Ridership where strftime('%Y', date(Ride_Date)) between '2001' and '2021' Group by strftime('%Y', date(Ride_Date)) Order by strftime('%Y', date(Ride_Date)) asc")
  row = dbCursor.fetchall();
  for i in row:
    print(i[0], ":", f"{i[1]:,}")
  print()
  userInput = input("Plot? (y/n) ")
  if(userInput == 'y'):
    x = []
    y = []
    for j in row:
      xNum = (j[0][-2:])
      yNum = round(j[1]/(10**8), 2)
      x.append(xNum)
      y.append(yNum)
    figure.xlabel("year")
    figure.ylabel("number of riders (x * 10^8)")
    figure.title("yearly ridership")
    figure.plot(x,y)
    figure.show()
  print()


###########################################################  
#
# necessary helper function for eighthCommand to help loop through 2 separate rows and print out results first 5 and last 5
def helperFunc(row, row2, row3, row4):
    for r in row:
      print("Station 1:", r[0], r[1])
    for i in row3[:5]:
      print(i[0], i[1])
    for j in row3[-5:]:
      print(j[0], j[1])
    for r in row2:
      print("Station 2:", r[0], r[1])
    for i in row4[:5]:
      print(i[0], i[1])
    for j in row4[-5:]:
      print(j[0], j[1])
    print()


###########################################################  
#
# helpeer function for eighthCommand to plot the graph, using the given code on pdf modify to work with the given parameters
def plotFunc8(userInput, userInput4, row3, row4, label1, label2):
  if(userInput4 == 'y'):
    counter, counter2 = 1, 1;
    x1, y1, x2, y2= [], [], [], []
    for i in row3:
      x1.append(counter)
      y1.append(i[1])
      counter += 1;
    for j in row4:
      x2.append(counter2)
      y2.append(j[1])
      counter2 += 1;
    figure.xlabel("day")
    figure.ylabel("number of riders")
    figure.title("riders each day of " + userInput)
    figure.plot(x1,y1)
    figure.plot(x2,y2)
    figure.legend([label1, label2])
    figure.show()
  print()


########################################################### 
# eighth command - long function, needed helper functions, 2 total queries (1 to deal with station name, station ID; 1 to deal with date, num ride), multiple if-elif-else statements to check user input, loop for results and plot graph
def eighthCommand(userInput, dbConn):
  dbCursor = dbConn.cursor()
  print()
  userInput = input("Year to compare against? ");
  print()
  userInput2 = input("Enter station 1 (wildcards _ and %): ");
  sql = """Select Station_ID, Station_Name from Stations where Station_Name like ? Order by Station_Name"""
  dbCursor.execute(sql, [userInput2])
  row = dbCursor.fetchall();
  sql2 = """Select date(Ride_Date), (Num_Riders)
  From Ridership where Station_ID = ? and strftime('%Y', (Ride_Date)) = ? 
  Order by strftime('%Y', (Ride_Date))"""
  if(len(row) > 1):
    print("**Multiple stations found...")
    print()
  elif(len(row) < 1):
    print("**No station found...")
    print()
  elif(len(row) == 1):
    stationID = row[0][0];
    print()
    userInput3 = input("Enter station 2 (wildcards _ and %): ");
    dbCursor.execute(sql, [userInput3])
    row2 = dbCursor.fetchall();
    # stationID2 = row2[0][0];
    if(len(row2) > 1):
      print("**Multiple stations found...")
      print()
    elif(len(row2) < 1):
      print("**No station found...")
      print()
    elif(len(row2) == 1):
      stationID2 = row2[0][0];
      dbCursor.execute(sql2, [stationID, userInput])
      row3 = dbCursor.fetchall();
      stationID = row2[0][0];
      dbCursor.execute(sql2, [stationID2, userInput])
      row4 = dbCursor.fetchall();
      helperFunc(row, row2, row3, row4)
      userInput4 = input("Plot? (y/n) ")
      label1 = row[0][1];
      label2 = row2[0][1];
      plotFunc8(userInput, userInput4, row3, row4, label1, label2);
    

########################################################### 
# ninth command - similar to the 5th/8th command, follow the formats of both to create 1 query to find Station name, Lat, Long, loop to print output and plot follow pdf using chicago pic as background
def ninthCommand(userInput, dbConn):
  dbCursor = dbConn.cursor()
  print()
  userInput = input("Enter a line color (e.g. Red or Yellow): ");
  sql = """Select Distinct Station_Name, Latitude, Longitude From Stops
  join Stations on Stops.Station_ID = Stations.Station_ID
  join StopDetails on Stops.Stop_ID = StopDetails.Stop_ID
  join Lines on StopDetails.Line_ID = Lines.Line_ID
  where Color like ?
  Order by Station_Name asc;"""
  dbCursor.execute(sql, [userInput])
  row = dbCursor.fetchall();
  if(len(row) == 0):
    print("**No such line...")
    print()
  else:
    for i in row:
      print(i[0], ":", f"{i[1], i[2]}")
    print()
    userInput2 = input("Plot? (y/n) ")
    if(userInput2 == 'y'):
      x = []
      y = []
      for j in row:
        x.append(j[2])
        y.append(j[1])
      image = figure.imread("chicago.png")
      xydims = [-87.9277, -87.5569, 41.7012, 42.0868]
      figure.imshow(image, extent = xydims)
      figure.title(userInput + "line")
      if(userInput.lower() == "purple-express"):
        userInput = "Purple"
      figure.plot(x, y, "o", c=userInput)
      for r in row:
        figure.annotate(r[0], (r[2], r[1]))
      figure.xlim([-87.9277, -87.5569])
      figure.ylim([41.7012, 42.0868])
      figure.show()
    print()
  

###########################################################  
#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
    dbCursor = dbConn.cursor()
    
    print("General stats:")
    
    dbCursor.execute("Select count(*) From Stations;")
    row = dbCursor.fetchone();
    print("  # of stations:", f"{row[0]:,}")
    dbCursor.execute("Select count(*) From Stops;")
    row = dbCursor.fetchone();
    print("  # of stops:", f"{row[0]:,}")
    dbCursor.execute("Select count(*) From Ridership;")
    row = dbCursor.fetchone();
    print("  # of ride entries:", f"{row[0]:,}")
    dbCursor.execute("Select min(date(Ride_Date)) From Ridership;")
    row = dbCursor.fetchone();
    dbCursor.execute("Select max(date(Ride_Date)) From Ridership;")
    row1 = dbCursor.fetchone();
    print("  date range:", f"{row[0]} - {row1[0]}")
    dbCursor.execute("Select sum(Num_Riders) From Ridership;")
    row2 = dbCursor.fetchone();
    print("  Total ridership:", f"{row2[0]:,}")
    dbCursor.execute("Select sum(Num_Riders) From Ridership where Type_of_Day = 'W';")
    row3 = dbCursor.fetchone();
    percent1 = float(((row3[0]/row2[0]) * 100));
    print("  Weekday ridership:", f"{row3[0]:,}", f"({percent1:0.2f}%)")
    dbCursor.execute("Select sum(Num_Riders) From Ridership where Type_of_Day = 'A';")
    row4 = dbCursor.fetchone();
    percent2 = float(((row4[0]/row2[0]) * 100));
    print("  Saturday ridership:", f"{row4[0]:,}", f"({percent2:0.2f}%)")
    dbCursor.execute("Select sum(Num_Riders) From Ridership where Type_of_Day = 'U';")
    row5 = dbCursor.fetchone();
    percent3 = float(((row5[0]/row2[0]) * 100));
    print("  Sunday/holiday ridership:", f"{row5[0]:,}", f"({percent3:0.2f}%)")
    print();
    

###########################################################  
#
# main
# main function to run defined functions above
#
print('** Welcome to CTA L analysis app **')
print()

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')

print_stats(dbConn)

# while loop to keep asking for userInput unless user exited
while(True):
  userInput = input("Please enter a command (1-9, x to exit): ")
  if(userInput == 'x'):
    exit()
  elif(userInput == '1'):
    firstCommand(userInput, dbConn)
  elif(userInput == '2'):
    secondCommand(dbConn)
  elif(userInput == '3'):
    thirdCommand(dbConn)
  elif(userInput == '4'):
    fourthCommand(dbConn)
  elif(userInput == '5'):
    fifthCommand(userInput, dbConn)
  elif(userInput == '6'):
    sixthCommand(userInput, dbConn)
  elif(userInput == '7'):
    seventhCommand(userInput, dbConn)
  elif(userInput == '8'):
    eighthCommand(userInput, dbConn)
  elif(userInput == '9'):
    ninthCommand(userInput, dbConn)
  else:
    print("**Error, unknown command, try again... ")
    print()

#
# done
#
