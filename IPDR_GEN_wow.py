from operator import itemgetter
import time
import multiprocessing
from multiprocessing import Process,Queue,Pool,Lock,Manager
import sys,commands
import random
from optparse import OptionParser


'''
CMTS,3
CMTSupifName,9
CMTSdownifName,11
CMmacAddress,12
timeStamp,21
serviceDirection,28
serviceOctetsPassed,29
serviceSlaDropPkts,31
serviceSlaDelayPkts,32
'''

#ST_DT=raw_input("Enter the start Time(Year month day Hour Min Sec)")
#ED_DT=raw_input("Enter the end Time(Year month day Hour Min Sec)")
RefineryIndMap = {"Ref_Name": "SamisRollupA",\
                  "Job_Name": "Samis1HrRollup",\
                  "CmtsHostName":"CMTS_10.0.0.1",\
                  "CmtsIpv4Addr":"10.0.0.1",\
   		  "CmtsIpv6Addr":" ",\
		  "CmtsSysUpTime":"900",\
		  "CmtsMdIfName":"Cable5/0/3",\
                  "CmtsMdIfIndex":"103",\
		  "CmtsUpIfName":"Cable5/0/3-upstream",\
		  "CmtsUpIfType":"129",\
		  "CmtsDownIfName":"Cable5/0/3-downstream",\
		  "CmMacAddr":"01:FD:00:00:00:00",\
		  "CmIpV4Addr":"100.0.0.1",\
		  "CmIpV6Addr":" ",\
		  "CmIpv6LinkLocalAddr":" ",\
		  "CmServiceType":" ",\
		  "CmRegStatusValue":" ",\
		  "CmLastRegTime":" ",\
		  "CmDocsisMode":11,\
		  "CMcpeIpAddress":" ",\
		  "recJobExecTime":0,\
	          "recJobIntvalStartTime":0,\
		  "recJobIntvalStopTime":0,\
		  "ServiceFlowChSet":" ",\
  		  "ServiceIdentifier":"1",\
                  "ServiceClassName":"Gold",\
		  "ServiceFlowChSet":" ",\
   		  "ServiceDirection":"1",\
		  "ServiceOctetsPassed":1000,\
		  "ServicePktsPassed":500,\
   		  "ServiceSlaDropPkts":200,\
	          "ServiceSlaDelayPkts":50,\
		  "ServiceTimeActive":0,\
		  "ServiceDsMulticast":5,\
		  "SfDataRate":"1000 "\
		  }
Backup_refinery=RefineryIndMap
Service_direc=["1","2"]
Service_name={201:"Gold",301:"Platinum",401:"silver",501:"bronze"}
Docsis_mode=["10","11","20","30"]

CMTSFile=open('CMTS_CM_Combi','r')
CMTSCMCombi=CMTSFile.readlines()

CMTSFile.close()


#CMFile=open('CM_Names','r')
#CMName=CMFile.readlines()
#CMFile.close()

CMIPFile=open('CM_IPs','r')
CMIPs=CMIPFile.readlines()
CMIPFile.close()

CMTSMDFile=open('CMTS_MD_Names','r')
CMTSMDName=CMTSMDFile.readlines()
CMTSMDFile.close()

CMTSIPFile=open('CMTS_IPs','r')
CMTSIPs=CMTSIPFile.readlines()
CMTSIPFile.close()
#################   Binning and generation start here ######

#struct_time_st = time.strptime(ST_DT, "%Y-%m-%d:%H")
#struct_time_ed = time.strptime(ED_DT, "%Y-%m-%d:%H")
#startTime=int(time.mktime(struct_time_st))
#endTime=int(time.mktime(struct_time_ed))

def record_gen(dataInmap,startTime,endTime,binInterval,NumberOfRecords):
	startTime=int(time.mktime(time.strptime(startTime, "%Y-%m-%d:%H")))
	endTime=int(time.mktime(time.strptime(endTime, "%Y-%m-%d:%H")))
	binInterval=int(binInterval)	
	counter=(endTime-startTime)/binInterval
	tempTime=startTime
	print "Total Number of files wil be generated: " + str(counter)
	for i in range (0,counter):
                records=int(NumberOfRecords)
                filetime=time.strftime("%Y%m%d%H%M%S",time.localtime(startTime+binInterval-1+binInterval*i))
		
                fileName="Rollup_"+str(filetime)+".csv"
		print "Preparing file:\t" + fileName
                f=open(fileName, 'w')
		crTime=tempTime
                recStartTime=random.randrange(tempTime,tempTime+binInterval)
                recStopTime=random.randrange(recStartTime,recStartTime+1)
		while(records != 0):
			(CMTSName,CMName)=(random.choice(CMTSCMCombi)).split(',')
			recStartTime=random.randrange(tempTime,tempTime+binInterval)
			recStopTime=random.randrange(recStartTime,recStartTime+binInterval)
			oct_passed=random.randrange(10000,200000)
			pckts_passed=random.randrange(1000,oct_passed)
			drop_pckts=random.randrange(0,2)
			delay_pckts=random.randrange(0,2)
			key_val=random.choice(Service_name.keys())
			dataInmap["curTime"]=crTime*1000
			dataInmap["recStartTime"]=recStartTime*1000
			dataInmap["recEndTime"]=recStopTime*1000
			#dataInmap["CmtsHostName"]=CMTS_host[CMTS_rand_val]
			dataInmap["CmtsHostName"]=CMTSName.strip('\n')
			#dataInmap["CmtsIpv4Addr"]=CMTS_ips[CMTS_rand_val]
			dataInmap["CmtsIpv4Addr"]=random.choice(CMTSIPs).strip('\n')
			#dataInmap["CmtsMdIfName"]=CMTS_md_name[CMTS_rand_val]
			dataInmap["CmtsMdIfName"]=random.choice(CMTSMDName).strip('\n')
			#dataInmap["CmtsUpIfName"]=CMTS_md_name[CMTS_rand_val]+"-upstream"
			dataInmap["CmtsUpIfName"]=random.choice(CMTSMDName).strip('\n')+"-upstream"
			#dataInmap["CmtsDownIfName"]=CMTS_md_name[CMTS_rand_val]+"-downstream"
			dataInmap["CmtsDownIfName"]=random.choice(CMTSMDName).strip('\n')+"-downstream"
			#dataInmap["CmMacAddr"]=CM_mac[CM_rand_val]
			dataInmap["CmMacAddr"]=CMName.strip('\n')
	
			#dataInmap["CmIpV4Addr"]=CM_ips[CM_rand_val]
			dataInmap["CmIpV4Addr"]=random.choice(CMIPs).strip('\n')
			#dataInmap["CmServiceType"]=random.randrange(1,2)
			dataInmap["CmDocsisMode"]=Docsis_mode[random.randrange(0,3)]
			dataInmap["recJobExecTime"]=(endTime*10000)-1
       			dataInmap["recJobIntvalStartTime"]=recStartTime*1000
        		dataInmap["recJobIntvalStopTime"]=recStopTime*1000
			dataInmap["ServiceClassName"]=Service_name[key_val]
			dataInmap["ServiceDirection"]=random.choice(Service_direc)
			dataInmap["ServiceOctetsPassed"]=oct_passed
			dataInmap["ServicePktsPassed"]=pckts_passed
			dataInmap["ServiceSlaDropPkts"]=drop_pckts
			dataInmap["ServiceSlaDelayPkts"]=delay_pckts
			val_ipdr=dataInmap["Ref_Name"]+','+dataInmap["Job_Name"]+','+dataInmap["CmtsHostName"]+','+str(dataInmap["CmtsIpv4Addr"])+','+str(dataInmap["CmtsIpv6Addr"])+','+str(dataInmap["CmtsSysUpTime"])+','+dataInmap["CmtsMdIfName"]+','+dataInmap["CmtsMdIfIndex"]+','+dataInmap["CmtsUpIfName"]+','+dataInmap["CmtsUpIfType"]+','+dataInmap["CmtsDownIfName"]+','+str(dataInmap["CmMacAddr"])+','+str(dataInmap["CmIpV4Addr"])+','+str(dataInmap["CmIpV6Addr"])+','+str(dataInmap["CmIpv6LinkLocalAddr"])+','+dataInmap["CmServiceType"]+','+str(dataInmap["CmRegStatusValue"])+','+str(dataInmap["CmLastRegTime"])+','+dataInmap["CmDocsisMode"]+','+str(dataInmap["CMcpeIpAddress"])+','+str(dataInmap["recJobExecTime"])+','+str(dataInmap["recJobIntvalStartTime"])+','+str(dataInmap["recJobIntvalStopTime"])+','+dataInmap["ServiceFlowChSet"]+','+dataInmap["ServiceIdentifier"]+','+dataInmap["ServiceClassName"]+','+dataInmap["ServiceFlowChSet"]+','+str(dataInmap["ServiceDirection"])+','+str(dataInmap["ServiceOctetsPassed"])+','+str(dataInmap["ServicePktsPassed"])+','+str(dataInmap["ServiceSlaDropPkts"])+','+str(dataInmap["ServiceSlaDelayPkts"])+','+str(dataInmap["ServiceTimeActive"])+','+str(dataInmap["ServiceDsMulticast"])+','+str(dataInmap["SfDataRate"])
	
			
			f.write(str(val_ipdr)+'\n')
			records=records-1
		f.close()
		tempTime=startTime+binInterval*i
		
if __name__ == '__main__':

#	for i in range(20):
#		p = multiprocessing.Process(target=record_gen(Backup_refinery,startTime,endTime))
#		p.join
#		p.start()
	#record_gen(Backup_refinery,startTime,endTime)
	parser = OptionParser(usage="usage: %prog [options] ",version="%prog 1.0",conflict_handler="resolve")
        parser.add_option("-s", "--starttime",
                        action="store",
                        dest="startTime",
                        type="str",
                        help="YYYY-MM-DD:HH example:2013-01-22:00")
        parser.add_option("-e", "--endtime",
                        action="store",
                        dest="endTime",
                        type="str",
                        help="YYYY-MM-DD:HH example:2013-01-22:00")
        parser.add_option("-b", "--binInterval",
                        action="store",
                        dest="binInterval",
                        type="str",
                        help="Bin Interval (secs),  example:900")
        parser.add_option("-n", "--NumberOfRecords",
                        action="store",
                        dest="NumberOfRecords",
                        type="str",
                        help="Number of Records Required in every file")

        options, args = parser.parse_args()
        if(options.startTime != None and options.endTime != None and options.binInterval != None and options.NumberOfRecords != None):
                startTime = options.startTime
                endTime = options.endTime
                binInterval = options.binInterval
                NumberOfRecords = options.NumberOfRecords
        else:
                print "Insufficient Arguments entered...."
                (status,output) = commands.getstatusoutput("python %s --help" %(sys.argv[0]))
                print output
                sys.exit(0)
	record_gen(Backup_refinery,startTime,endTime,binInterval,NumberOfRecords)
