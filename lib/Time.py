#---------------------------------------------------------------------
import datetime;
#---------------------------------------------------------------------

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

    def GetTimeNow(self):
        ''' Get time now in UTC format '''
        now = datetime.datetime.utcnow();
        return now;

    def GetPreviousNDay(self, n=1):
        ''' Get time of previous N days in UTC format '''
        now = datetime.datetime.utcnow();
        offset = datetime.timedelta(days=n);
        return now - offset;

    def GetPreviousNMonth(self, n=1):
        ''' Get time of previous N months in UTC format '''
        now = datetime.datetime.utcnow();
        offset = datetime.timedelta(days=n*30);
        return now - offset;
 
    def GetPreviousNYear(self, n=1):
        ''' Get time of previous N years in UTC format '''
        now = datetime.datetime.utcnow();
        offset = datetime.timedelta(days=n*365);
        return now - offset;

    def UTCToISO(self,dt):
        ''' Convert date time to ISO format '''
        return dt.replace(microsecond = 0).isoformat() + 'Z';

