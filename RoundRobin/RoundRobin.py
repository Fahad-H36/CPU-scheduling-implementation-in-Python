import pandas as pd
import sys
import statistics



# Reading data from inputs file
df = pd.read_csv("inputs(2).csv")


# seting up data in the format that will be used later on
d = df.set_index('Process_ID').T.to_dict('list')

# seting up variables for later calculations
percentListx = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
percentCheckpoints = []

numPGraph = []
clockGraph = []


for percent in percentListx:
    percentCheckpoints.append(int(percent*len(d)))






def age(taskQueue):
    for i in taskQueue:
        i[2]+=1
    
    return taskQueue


# This function simulates the Shortest-Remaining-First CPU scheduling algorithm,
# it takes one argument 'n' which is number of clock cycles after which execution will be halted.
def priority(n):
    
    # Opening a text file in which results will be recorded
    the_file = open('results5.txt', 'a')


    # seting up variables for later use
    waitTimes = []
    susPerProcesses = []
    numSusProcesses = 0

    timeQuantum = 20

    clock = 0
    taskQueue = []
    deadlinesMissed = 0
    percentCounter = 0
    completed = 0

    dataDict = {}

    
    index = 0

    # This is the main loop that represents clock cycles
    while clock <= n:

        # This boolean valiable will be true if context switching is to happen
        susFlag = False


        # This conditional is to push the next process in the task queue if it's arrival time has come
        if index <= len(df["Process_ID"])-1 and clock == df["Arrival_Time"][index]:

            if len(taskQueue) == 0:
                startTime = clock



            taskQueue.append([df["Process_ID"][index], df["Execution_Time"][index]])

            print("PUSHED: "+str(df["Process_ID"][index]) + " " + str(df["Arrival_Time"][index]) + " " + str(clock))
            index+=1

                

            



        # This conditional is to pop a process out of task queue if it is fully executed
        # And readjusts the list if time quantum is completed
        if len(taskQueue) > 0:
            currentTask = taskQueue[0]
            if currentTask[1]==0:
                t = taskQueue.pop(0)
                completed += 1
                susPerProcesses.append(numSusProcesses)
                numSusProcesses = 0

                # This condition checks if deadline is missed
                if clock>d[t[0]][3]:
                    deadlinesMissed += 1
                    print("Deadline Missed")
                
                if len(taskQueue)>0:
                    startTime = clock                


                

               

                # This condition records what % of processes are completed in how many clock cycles
                if completed == percentCheckpoints[percentCounter]:
                    the_file.write("\n\n\n{} PERCENT PROCESSES COMPLETED IN {} CLOCK CYCLES\n".format(int(percentListx[percentCounter]*100), clock))

                    percentCounter+=1                    
                
                # Records data to make required graph
                numPGraph.append(completed)
                clockGraph.append(clock)                
                waitTimes.append(clock-d[t[0]][0])
                print("POPED PROCESS: "+str(t[0]) + str(d[t[0]]) + " " + str(clock))

                

            # Reshuffles the taskQueue if time quantum in completed
            elif clock - startTime == timeQuantum:

                if len(taskQueue) == 1:
                    startTime = clock
                

                else:
                    currentTask[1]-=1        
                    prevTask = taskQueue.pop(0)
                    taskQueue.append(prevTask)
                    numSusProcesses+=1
                    susFlag = True



            if not susFlag:
                currentTask[1]-=1        

        if susFlag:
            print("Suspended {}".format(prevTask, taskQueue[0]))
            clock+=1
            continue

        

        clock+=1
    
    deadlinesMissed = deadlinesMissed + len(taskQueue)



    # Writes all the required information in the text file
    the_file.write("\n\n\nMAX WAITING TIME:    {}\n".format(max(waitTimes)))
    the_file.write("MIN WAITING TIME:    {}\n".format(min(waitTimes)))
    the_file.write("AVERAGE WAITING TIME:    {}\n".format(statistics.mean(waitTimes)))
    the_file.write("STANDARD DEVIATION OF WAITING TIME:    {}\n".format(statistics.stdev(waitTimes)))

    the_file.write("\n\n\nMAX NUMBER OF SUSPENSIONS PER PROCESS:    {}\n".format(max(susPerProcesses)))
    the_file.write("MIN NUMBER OF SUSPENSIONS PER PROCESS:    {}\n".format(min(susPerProcesses)))
    the_file.write("AVERAGE NUMBER OF SUSPENSIONS PER PROCESS:    {}\n".format(statistics.mean(susPerProcesses)))
    the_file.write("STANDARD DEVIATION OF NUMBER OF SUSPENSIONS PER PROCESS:    {}\n".format(statistics.stdev(susPerProcesses)))


    the_file.write("\n\n\nNUMBER OF DEADLINES MISSED:    {}\n".format(deadlinesMissed))
    the_file.write("\n\n\nNUMBER OF PROCESSES THAT TIMED OUT:    {}\n".format(len(taskQueue)))


    # Exporting graph data to a csv file
    dataDict["NumberOfProcess"] = numPGraph
    dataDict["Time"] = clockGraph

    df1 = pd.DataFrame(dataDict)

    df1.to_csv("graphData5.csv", index=False)


    # Halting all the processes
    sys.exit("All processes halted")




priority(30000)