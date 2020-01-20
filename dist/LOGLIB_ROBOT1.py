#the library that is used to write detailed logs of the vehicles actions
#author: katznboyz/harrison

#import statements
import os, datetime

#main class for the logger
class RobotActionLogger:

    #set the path to /dev/null and let the user change it when they initialize the class
    LOG_PATH = '/dev/null'

    #variables for the time formats (all in UTC for organizational purposes)
    LINE_TIME_STRING_FORMAT = '%m-%d-%y-%H-%M-%S-UTC' #month-day-year-hour-minute-second-UTC
    FILE_TIME_STRING_FORMAT = '%m-%d-%y-UTC' #month-day-year-UTC

    #create an error class for when the path they want to write to is nonexistent
    class WritePathNonexistentError(Exception):
        pass

    #function to initialize the class
    def __init__(self, logFolderPath) -> None:

        #check that the log folder path is existent
        if (not os.path.exists(str(logFolderPath))):

            #since the path does not exist raise an error
            raise RobotActionLogger.WritePathNonexistentError('The path "{}" does not exist. Please initialize the logger into a folder that already exists.'.format(logFolderPath))

        #set the log path to logFolderPath
        self.LOG_PATH = str(logFolderPath)
    
    #function to create a line that can be written to the log or printed to the console
    def createLogLine(self, text) -> str:

        #final output string
        outputString = '{}\u2588{}\u2588{}'.format(
            str(datetime.datetime.utcnow().strftime(str(self.LINE_TIME_STRING_FORMAT))), #time string
            str(os.getpid()), #process ID string
            str(str(text).replace('\u2588', '|')) #message text string
        )

        #return the final output string
        return str(outputString)
    
    #function to write a line to the log file
    def writeLogLine(self, text) -> None:

        #generate the line that will be logged
        logLineText = str(self.createLogLine(text))

        #generate the title of the log file
        logFileName = str(datetime.datetime.utcnow().strftime(str(self.FILE_TIME_STRING_FORMAT))) + '.txt'

        #create the log file path
        logFilePath = str(self.LOG_PATH) + str('/' if (str(self.LOG_PATH[-1]) != '/') else '') + str(logFileName)
        
        #check if the file exists
        if (not os.path.exists(str(logFilePath))):

            #create the file since it doesnt exist
            logFile = open(logFilePath, 'w')
            logFile.write('')
            logFile.close()

            #delete the logFile variable so it doesnt overlap later
            del logFile
        
        #open the file and get the previous contents
        logFile = open(logFilePath, 'r')
        previousLogFileContents = str(logFile.read())
        logFile.close()

        #delete the logFile variable so it doesnt overlap to the write only file below this
        del logFile

        #write the previous contents plus the new contents to the log file
        logFile = open(logFilePath, 'w')
        logFile.write(str(str(previousLogFileContents) + '\n' + str(logLineText)))
        logFile.close()