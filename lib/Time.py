import datetime;

#Custom Time class for manage UTC and printout formats
class Time:
    # Here will be the instance stored.
    __instance = None;

    #Get Singleton's only instance
    @staticmethod
    def GetInstance():
        """ Static access method. """
        if Time.__instance == None:
            Time();
        return Time.__instance ;

    #Init Singleton Object
    def __init__(self):
        """ Virtually private constructor. """
        if Time.__instance != None:
            raise Exception("This class is a singleton!");
        else:
            Time.__instance = self;

    #Get time now in TUC format
    def GetTimeNow(self):
        now = datetime.datetime.utcnow();
        return now;

    #Get time of previous N days in UTC format
    def GetPreviousNDay(self, n):
        now = datetime.datetime.utcnow();
        offset = datetime.timedelta(days=n);
        return now - offset;

    #Get time of previous N months in UTC format
    def GetPreviousNMonth(self, n):
        now = datetime.datetime.utcnow();
        offset = datetime.timedelta(days=n*30);
        return now - offset;

    #Get time of previous N years in UTC format
    def GetPreviousNYear(self, n):
        now = datetime.datetime.utcnow();
        offset = datetime.timedelta(days=n*365);
        return now - offset;


