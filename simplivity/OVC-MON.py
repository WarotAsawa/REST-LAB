# -*- coding: utf-8 -*-
#Import standard Python library
from SimplivityCluster import SimplivityCluster;
import sys;
import os.path;
import dash;
import logging;
from datetime import datetime, timedelta;
#Import external libraries
sys.path.insert(0, os.path.abspath(os.path.join(os.pardir,"lib")));
from dash.dependencies import Output, Input, State
from Time import Time;
import dateutil.parser as DateParser;
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go;

logging.getLogger('werkzeug').setLevel(logging.ERROR);
#OVC Credential
ovcIP = "NA";
ovcUser = "NA";
ovcPass = "NA";
defOVCIP = "";
defOVCUser = "";
defOVCPass = "";
llCluster = {};
#Inventory
hostsList = {}
clustersList = {};
backupList = {};
vmList = {}
#List of graph and text that need update
allGraph = {};
allText = {};
allOutput = [];
#Interval
backupSumDay = 1;
intervalSec = 10;
reloginInterval = 1800;
widthPage = '94vw';
marginPage = '3vw';

def UpdateAllInventory():
    global ovcIP, hostsList, clustersList, backupList,vmList;
    if ovcIP =="NA":
        return;

    clustersList = llCluster.GetClustersAll();
    hostsList = llCluster.GetHostsAll();
    vmList = llCluster.GetVMsAll();
    print("=====ALL INVENTORY UPDATED=====");

def UpdateAllBackup():
    global ovcIP, hostsList, clustersList, backupList,vmList;
    if ovcIP =="NA":
        return;

    backupList = llCluster.GetBackUpsAll();
    print("=====ALL BACKUP UPDATED=====");

def AddGraph(id):
    global allGraph, allOutput;
    allGraph[id] = html.Div(children = [dcc.Graph(id=id,animate=True,style = {'height':'100%','width':'100%'})]);
    allOutput.append(Output(id,'figure'));

def AddText(hType,id,string):
    global allText, allOutput;
    if hType == "H1":
        allText[id] = html.Div(id=id,className='h1 mb-0 font-weight-bold text-gray-800', children =string);
    if hType == "H2":
        allText[id] = html.Div(id=id,className='h2 mb-0 font-weight-bold text-gray-800', children =string);
    if hType == "H3":
        allText[id] = html.Div(id=id,className='h3 mb-0 font-weight-bold text-gray-800', children =string);
    if hType == "H4":
        allText[id] = html.Div(id=id,className='h4 mb-0 font-weight-bold text-gray-800', children =string);
    if hType == "H5":
        allText[id] = html.Div(id=id,className='h5 mb-0 font-weight-bold text-gray-800', children =string);
    if hType == "H6":
        allText[id] = html.Div(id=id,className='h6 mb-0 font-weight-bold text-gray-800', children =string);
    allOutput.append(Output(id,'children'));

def DrawText(id):
    global allText;
    return allText[id];

def DrawGraph(id):
    global allGraph;
    return allGraph[id];

def InitialOutputComponent():
    AddText("H5", 'ipSum', 'Please Login');
    AddText("H5", 'nodeSum', 'Please Login');
    AddText("H5", 'clusterSum', 'Please Login');
    AddText("H5", 'backupSum', 'Please Login');
    AddText("H6", 'lastUpdate', 'Please Login');
    AddGraph('cluster-reduction-graph');
    AddGraph('cluster-physical-graph');
    AddGraph('cluster-logical-graph');
    AddGraph('logical-graph');
    AddGraph('physical-graph');
    AddGraph('24h-backup');
    AddGraph('vm-policy-graph');
    AddGraph('all-backup');
    AddGraph('heatmap');

def Login(ovcIP, ovcUser, ovcPass):
    global llCluster;

    llCluster = SimplivityCluster(ovcIP, ovcUser, ovcPass);
    result =  llCluster.Initialize();

    UpdateAllInventory();

    return result;

#Get Simplivity's Data Methods

def GetClustersCapacityData():
    global ovcIP, clustersList;

    outputList = {};
    nodeList = [];
    nodeVMData = [];
    nodeLocalBackup = [];
    nodeRemoteBackup = [];
    nodeUsedSpace = [];
    nodeFreeSpace = [];
    nodeDedupe = [];
    nodeCompress = []
    nodeReduct = [];
    if ovcIP == "NA":
        nodeList.append("Please Login");
        nodeVMData.append(0);      
        nodeLocalBackup.append(0);
        nodeRemoteBackup.append(0);
        outputList['name'] = nodeList;
        outputList['vmData'] = nodeVMData;
        outputList['localBackup'] = nodeLocalBackup;
        outputList['remoteBackup'] = nodeRemoteBackup;
        outputList['used_capacity'] = [0];
        outputList['free_space'] = [0];
        outputList['deduplication_ratio'] = [0];
        outputList['compression_ratio'] = [0];
        outputList['efficiency_ratio'] = [0];
        return outputList;

    hostList = clustersList;

    for host in hostList:
        vmdata=float("{0:.2f}".format(host["stored_virtual_machine_data"]/pow(1024.0,4)));
        localbkk = float("{0:.2f}".format(host["local_backup_capacity"]/pow(1024.0,4)));
        remotebkk = float("{0:.2f}".format(host["remote_backup_capacity"]/pow(1024.0,4)));
        usedCapacity = float("{0:.2f}".format(host["used_capacity"]/pow(1024.0,4)));
        freeCapacity = float("{0:.2f}".format(host["free_space"]/pow(1024.0,4)));
        dedupe = host["deduplication_ratio"].split(":");
        dedupeRatio = float(dedupe[0]);
        compress = host["compression_ratio"].split(":");
        compressRatio = float(compress[0]);
        reduct = host["efficiency_ratio"].split(":");
        reductRatio = float(reduct[0]);
        nodeList.append(host['name']);
        nodeVMData.append(vmdata);      
        nodeLocalBackup.append(localbkk);
        nodeRemoteBackup.append(remotebkk);
        nodeUsedSpace.append(usedCapacity);
        nodeFreeSpace.append(freeCapacity);
        nodeDedupe.append(dedupeRatio);
        nodeCompress.append(compressRatio);
        nodeReduct.append(reductRatio);
    outputList['name'] = nodeList;
    outputList['vmData'] = nodeVMData;
    outputList['localBackup'] = nodeLocalBackup;
    outputList['remoteBackup'] = nodeRemoteBackup;
    outputList['used_capacity'] = nodeUsedSpace;
    outputList['free_space'] = nodeFreeSpace;
    outputList['deduplication_ratio'] = nodeDedupe;
    outputList['compression_ratio'] = nodeCompress;
    outputList['efficiency_ratio'] = nodeReduct;

    return outputList;

def GetHostsCapacityData():
    global ovcIP, hostsList;

    outputList = {};
    nodeList = [];
    nodeVMData = [];
    nodeLocalBackup = [];
    nodeRemoteBackup = [];
    if ovcIP == "NA":
        nodeList.append("Please Login");
        nodeVMData.append(0);      
        nodeLocalBackup.append(0);
        nodeRemoteBackup.append(0);
        outputList['name'] = nodeList;
        outputList['vmData'] = nodeVMData;
        outputList['localBackup'] = nodeLocalBackup;
        outputList['remoteBackup'] = nodeRemoteBackup;
        return outputList;

    hostList = hostsList

    for host in hostList:
        vmdata=float("{0:.2f}".format(host["stored_virtual_machine_data"]/pow(1024.0,4)));
        localbkk = float("{0:.2f}".format(host["local_backup_capacity"]/pow(1024.0,4)));
        remotebkk = float("{0:.2f}".format(host["remote_backup_capacity"]/pow(1024.0,4)));
        nodeList.append(host['name']);
        nodeVMData.append(vmdata);      
        nodeLocalBackup.append(localbkk);
        nodeRemoteBackup.append(remotebkk);
    outputList['name'] = nodeList;
    outputList['vmData'] = nodeVMData;
    outputList['localBackup'] = nodeLocalBackup;
    outputList['remoteBackup'] = nodeRemoteBackup;

    return outputList;

def GetPhysicalData():
    global ovcIP, hostsList;

    outputList = {};
    nodeList = [];
    usedCapList = [];
    leftCapList = [];
    if ovcIP == "NA":
        nodeList.append("Please Login");
        usedCapList.append(0);      
        leftCapList.append(0);
        outputList['name'] = nodeList;
        outputList['usedCap'] = usedCapList;
        outputList['leftCap'] = leftCapList;
    
        return outputList;

    hostList = hostsList;

    for host in hostList:
        allocCap=float("{0:.2f}".format(host["allocated_capacity"]/pow(1024.0,4)));
        usedCap = float("{0:.2f}".format(host["used_capacity"]/pow(1024.0,4)));
        nodeList.append(host['name']);
        usedCapList.append(usedCap);      
        leftCapList.append(allocCap-usedCap);
    outputList['name'] = nodeList;
    outputList['usedCap'] = usedCapList;
    outputList['leftCap'] = leftCapList;

    return outputList;

def GetHostCount():
    global ovcIP, hostsList;
    if ovcIP == "NA":
        return 3;
    hostList = hostsList;
    return len(hostList);

def GetBackupLastNDay(n):
    global ovcIP, backupList;
    resultList = {};

    if ovcIP == "NA":
        resultList["Please Login"] = 1;
        return resultList;

    targetDate = datetime.now() - timedelta(days=n);
    
    allBackup = backupList;
    if allBackup == {}:
        resultList["None"] = 1;
        return resultList;
    #Check every Backup state and add counts
    for backup in allBackup:
        backupTime = str(backup["created_at"]);
        backupDate = DateParser.parse(backupTime, ignoretz = True);
        
        if targetDate > backupDate:
            continue;
        if (backup['state'] in resultList):
            resultList[backup['state']] += 1;
            #print(targetDate);
            #print(backupDate)
        else:
            resultList[backup['state']] = 1;
    if len(resultList) == 0:
        resultList["No Backup"] = 1;
    return resultList;

def GetVMPolicyData():
    global ovcIP, vmList;
    resultList = {};

    if ovcIP == "NA":
        resultList["Please Login"] = 0;
        return resultList;

    if vmList == {}:
        resultList["None"] = 0;
        return resultList;
    #Check every Backup state and add counts
    for vm in vmList:
        vmPolicy = str(vm["policy_name"]);
        if (vmPolicy in resultList):
            resultList[vmPolicy] += 1;
        else:
            resultList[vmPolicy] = 1;
    if len(resultList) == 0:
        resultList["No Policy"] = 0;
    return resultList;

def GetBackupHistogramData():
    global ovcIP, backupList;
    resultList = {};

    if ovcIP == "NA":
        resultList["Please Login"] = 0;
        return resultList;

    if vmList == {}:
        resultList["None"] = 0;
        return resultList;
    #Check every Backup state and add counts
    for backup in backupList:
        startTime = str(backup['created_at']);
        endTime = str(backup['expiration_time']);
        #print(startTime + " " + endTime);
        if endTime == "NA":
            continue;
        startDate = DateParser.parse(startTime, ignoretz = True);
        endDate = DateParser.parse(endTime, ignoretz = True);

        retentionDays = (endDate - startDate).days;
        retention = str(retentionDays);
        if (retention in resultList):
            resultList[retention] += 1;
        else:
            resultList[retention] = 1;
    if len(resultList) == 0:
        resultList["No Backups"] = 0;
    return resultList;

def GetBackupHeatMapData():
    global ovcIP, backupList;

    today = datetime.now();
    today = today.replace(hour=0, minute=0, second=0, microsecond=0);
    targetDate = today - timedelta(days = 364);
    targetMonday = targetDate - timedelta(days = targetDate.weekday());

    totalDay = (today-targetMonday).days + 1;
    resultList = [0] * totalDay;
    #Check every Backup state and add counts
    for backup in backupList:
        endTime = backup['created_at'];
        endDate = DateParser.parse(endTime, ignoretz = True);
        endDate = endDate.replace(hour=0, minute=0, second=0, microsecond=0);
        dayDiff = (endDate - targetMonday).days;
        #print(dayDiff)
        if dayDiff <= totalDay-1 and dayDiff >=0:
            resultList[dayDiff] += 1;

    return resultList;

#Update Dashboard Graphs

def UpdateClusterLogical():  
    data = GetClustersCapacityData();
    nameCount = 0;
    maxCap = 0;
    for name in data['name']:
        totalCap = data['vmData'][nameCount]+data['localBackup'][nameCount]+data['remoteBackup'][nameCount];
        nameCount = nameCount + 1;
        if (totalCap > maxCap):
                maxCap = totalCap;
    vmTrace = go.Bar(
        x = data['name'],
        y = data['vmData'],
        name = 'VM Data (TiB)',
        #orientation = 'h',
        marker = dict(
            color = 'rgb(91,71,103)'
            )
        );
    localBackupTrace = go.Bar(
        x = data['name'],
        y = data['localBackup'],
        name = 'Local Backup (TiB)',
        #orientation = 'h',
        marker = dict(
            color = 'rgb(255,141,109)'
            )
        );
    remoteBackupTrace = go.Bar(
        x = data['name'],
        y = data['remoteBackup'],
        name = 'Remote Backup (TiB)',
        #orientation = 'h',
        marker = dict(
            color = 'rgb(128,130,133)'
            )
        );
    dataOutput = [vmTrace,localBackupTrace,remoteBackupTrace];
    barLayout = go.Layout(legend_orientation="h",yaxis = dict(range = [0,maxCap], title='Effective Capacity (TiB)'),xaxis = dict(range = [-1,nameCount]),barmode="stack");
    print("\nCluster's Logical Graph updated");
    return {'data' : dataOutput, 'layout' : barLayout}

def UpdateNodeLogical():

    data = GetHostsCapacityData();
    nameCount = 0;
    maxCap = 0;
    for name in data['name']:
        totalCap = data['vmData'][nameCount]+data['localBackup'][nameCount]+data['remoteBackup'][nameCount];
        nameCount = nameCount + 1;
        if (totalCap > maxCap):
                maxCap = totalCap;
    vmTrace = go.Bar(
        x = data['name'],
        y = data['vmData'],
        name = 'VM Data (TiB)',
        #orientation = 'h',
        marker = dict(
            color = 'rgb(91,71,103)'
            )
        );
    localBackupTrace = go.Bar(
        x = data['name'],
        y = data['localBackup'],
        name = 'Local Backup (TiB)',
        #orientation = 'h',
        marker = dict(
            color = 'rgb(255,141,109)'
            )
        );
    remoteBackupTrace = go.Bar(
        x = data['name'],
        y = data['remoteBackup'],
        name = 'Remote Backup (TiB)',
        #orientation = 'h',
        marker = dict(
            color = 'rgb(128,130,133)'
            )
        );
    dataOutput = [vmTrace,localBackupTrace,remoteBackupTrace];
    barLayout = go.Layout(legend_orientation="h",yaxis = dict(range = [0,maxCap], title='Effective Capacity (TiB)'),xaxis = dict(range = [-1,nameCount]),barmode="stack");
    print("\nLogical Graph updated");
    return {'data' : dataOutput, 'layout' : barLayout}

def UpdateNodePhysical():

    physData = GetPhysicalData();
    #set max x
    nameCount = 0;
    maxCap = 0;
    for name in physData['name']:
        totalCap = physData['usedCap'][nameCount]+physData['leftCap'][nameCount];
        nameCount = nameCount + 1;
        if (totalCap > maxCap):
                maxCap = totalCap;
    usedTrace = go.Bar(
        x = physData['name'],
        y = physData['usedCap'],
        name = 'Used Capacity (TiB)',
        #orientation = 'h',
        marker = dict(
            color = 'rgb(0,177,136)'
            )
        );
    leftTrace = go.Bar(
        x = physData['name'],
        y = physData['leftCap'],
        name = 'Free Capacity (TiB)',
        #orientation = 'h',
        marker = dict(
            color = 'rgb(200,200,200)'
            )
        );

    dataOutput = [usedTrace,leftTrace];
    barLayout = go.Layout(legend_orientation="h",yaxis = dict(range = [0,maxCap], title='Physical Capacity (TiB)'),xaxis = dict(range = [-1,nameCount]),barmode="stack");
    print("\nPhysical Graph updated");
    return {'data' : dataOutput, 'layout' : barLayout};

def UpdateClusterReduction():
    data = GetClustersCapacityData();
    nameCount = 0;
    maxCap = 0;
    for name in data['name']:
        totalCap = data['efficiency_ratio'][nameCount];
        nameCount = nameCount + 1;
        if (totalCap > maxCap):
                maxCap = totalCap;
    dedupTrace = go.Bar(
        y = data['deduplication_ratio'],
        x = data['name'],
        name = 'Deduplication Ratio',
        marker = dict(
            color = 'rgb(91,71,103)'
            )
        );
    compressTrace = go.Bar(
        y = data['compression_ratio'],
        x = data['name'],
        name = 'Compression Ratio',
        marker = dict(
            color = 'rgb(255,141,109)'
            )
        );
    reductTrace = go.Bar(
        y = data['efficiency_ratio'],
        x = data['name'],
        name = 'Efficiency Ratio',
        marker = dict(
            color = 'rgb(128,130,133)'
            )
        );
    dataOutput = [dedupTrace,compressTrace,reductTrace];
    barLayout = go.Layout(legend_orientation="h",xaxis = dict(range = [-1,nameCount]),yaxis = dict(range = [0,maxCap], title='Data Reduction Ratio (x)'), barmode='group');
    print("\nCluster reduction Graph updated");
    return {'data' : dataOutput, 'layout' : barLayout}

def UpdateClusterPhysical():
    physData = GetClustersCapacityData();
    #set max x
    nameCount = 0;
    maxCap = 0;
    for name in physData['name']:
        totalCap = physData['used_capacity'][nameCount]+physData['free_space'][nameCount];
        nameCount = nameCount + 1;
        if (totalCap > maxCap):
                maxCap = totalCap;
    usedTrace = go.Bar(
        y = physData['used_capacity'],
        x = physData['name'],
        name = 'Used Capacity (TiB)',
        marker = dict(
            color = 'rgb(0,177,136)'
            )
        );
    leftTrace = go.Bar(
        y = physData['free_space'],
        x = physData['name'],
        name = 'Free Capacity (TiB)',
        marker = dict(
            color = 'rgb(200,200,200)'
            )
        );

    dataOutput = [usedTrace,leftTrace];
    barLayout = go.Layout(legend_orientation="h",xaxis = dict(range = [-1,nameCount]),yaxis = dict(range = [0,maxCap], title='Cluster Physical Capacity (TiB)'),barmode="stack");
    print("\nCluster Physical Graph updated");
    return {'data' : dataOutput, 'layout' : barLayout};

def UpdateBackupDonuts(day):

    allBackup = GetBackupLastNDay(day);
    statusList = [];
    countList = [];
    title = "Status of backups since " + str(day) + " days";
    if day > 9000:
        title = "Status of all backups";
    holeSize = 0.8;
    protectedCount = 0;
    elseCount = 0;
    for key in allBackup:
        if key =="Please Login":
            holeSize = 1;
        if key =="PROTECTED":
            protectedCount = protectedCount+allBackup[key];
        elseCount = elseCount + allBackup[key];
        statusList.append(key);
        countList.append(allBackup[key]);
    protectedRate = protectedCount*100/elseCount;
    data = {"values":countList,
        "labels":statusList,
        "domain": {"column": 0},
        "name": "Backup Status",
        "hoverinfo":"label+value+name",
        "textinfo":"value",
        "hole": holeSize,
        "type": "pie",
        "marker":{"colors":donutColors},
    }
    donutLayout = {
        "title":title,
        "grid": {"rows": 1, "columns": 1},
        "annotations": [
            {
                "font": {"size": 15},
                "showarrow": False,
                "text": (str(protectedRate) + "% \nprotected"),
                "x": 0.5,
                "y": 0.5
            }
        ]
    }
    dataOutput = [data];
    print("\n" + str(day) + "days backup updated");
    return {'data' : dataOutput, 'layout' : donutLayout};

def UpdateVMPolicy():
    vmData = GetVMPolicyData();
    #set max x
    nameCount = 0;
    maxCap = 0;
    policyList = [];
    countList = [];
    for key in vmData.keys():
        policyList.append(key);
        countList.append(vmData[key]);
        totalCap = vmData[key];
        nameCount = nameCount + 1;
        if (totalCap > maxCap):
                maxCap = totalCap;
    policyTrace = go.Bar(
        y = policyList,
        x = countList,
        name = 'Number of VMs per Policy',
        orientation = 'h',
        marker = dict(
            color = 'rgb(255,141,109)'
            )
    );
    
    dataOutput = [policyTrace];
    barLayout = go.Layout(legend_orientation="h",xaxis = dict(range = [0,maxCap], title = "Number of VM"),yaxis = dict(range = [-1,nameCount]),barmode="stack");
    print("\n VM Policy Graph updated");
    return {'data' : dataOutput, 'layout' : barLayout};

def UpdateBackupHistogram():
    retentionData = GetBackupHistogramData();
    #set max x
    nameCount = 0;
    maxCap = 0;
    retentionList = [];
    countList = [];
    for key in retentionData.keys():
        retentionList.append(key);
        countList.append(retentionData[key]);
        totalCap = retentionData[key];
        nameCount = nameCount + 1;
        if (totalCap > maxCap):
                maxCap = totalCap;
    policyTrace = go.Bar(
        x = retentionList,
        y = countList,
        name = 'Backup Retention Histogram',
        marker = dict(
            color = 'rgb(91,71,103)'
            )
    );
    
    dataOutput = [policyTrace];
    barLayout = go.Layout(legend_orientation="h", yaxis = dict(range = [0,maxCap], title = "Number of Backups"),xaxis = dict(range = [-1,nameCount]),barmode="stack");
    print("\n Backup Histogram Graph updated");
    return {'data' : dataOutput, 'layout' : barLayout};

def UpdateBackupHeatMap():
    heat = GetBackupHeatMapData();
    totalDay = len(heat)-1;
    #print(heat)
    weekDay = ["Sun","M","T","W","Th","F","Sa"];
    xLabel = [];
    dayList = [];
    weekdays_in_year = [];
    weeknumber_of_dates = []
    month_year = [];
    hoverText = [];
    text = [];
    today = datetime.now()
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    firstDay = today - timedelta(days = totalDay);

    for i in range(0,totalDay+1):
        dayList.append(firstDay + timedelta(days = i));
    lastMonth = "";
    for i in range(0,totalDay+1):  
        d1 = dayList[i];
        d0 = dayList[0];
        my = "";
        if d1.day <= 7:
            my = str(d1.month) + "-" + str(d1.year);
        
        month_year.append(my);
        weekdays_in_year.append(d1.weekday())
        monday1 = (d1 - timedelta(days=d1.weekday()))
        monday0 = (d0 - timedelta(days=d0.weekday()))
        week1 = monday1.isocalendar()[1];
        week0 = monday0.isocalendar()[1];
        #print(str(monday1) + "  " + str(week1))
        #print((monday1-monday0).days/7);
        weekDiff = (monday1-monday0).days/7;
        thisMonth = monday1.strftime("%b %Y");
        if d1.weekday() == 0:
            if thisMonth ==  lastMonth:
                xLabel.append("");
            else:
                xLabel.append(thisMonth);
                lastMonth = thisMonth;
        weeknumber_of_dates.append(weekDiff);

        text.append(str(dayList[i].day) + "-" + str(dayList[i].month) + '-' + str(dayList[i].year) + " : " + str(heat[i]));
    #print(xLabel);
    colorscale=[[0,'rgb(220,220,220)'],[0.01,'rgb(220,220,220)'],
    [0.1,'rgb(165,209,199)'],[0.4,'rgb(165,209,199)'],
    [0.4,'rgb(110,198,178)'],[0.6,'rgb(110,198,178)'],
    [0.8,'rgb(55,188,157)'],[0.9,'rgb(55,188,157)'],[1,'rgb(0,177,136)']];
    data = [go.Heatmap(
        x = weeknumber_of_dates,
        y = weekdays_in_year,
        z = heat,
        text=text,
        hoverinfo="text",
        xgap=3, # this
        ygap=3, # and this is used to make the grid-like apperance
        showscale=False,
        colorscale=colorscale
        )
    ]
    layout = go.Layout(
        title="Backup Heatmap",
        height=280,
        yaxis=dict(
            showline = False, showgrid = False, zeroline = False,
            tickmode="array",
            ticktext=weekDay,
            tickvals=[0,1,2,3,4,5,6],
        ),
        xaxis=dict(
            showline = False, showgrid = False, zeroline = False,
            tickmode="array",
            ticktext=xLabel,
            tickvals=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52],
        ),
        font={'size':10, 'color':'#9e9e9e'},
        #plot_bgcolor=("#fff"),
        #margin = {'t':40)},
    )
    fig = go.Figure(data=data, layout=layout);

    return fig;

    
def UniversalUpdate():
    global ovcIP, nodeList, clustersList;
    outputList = [];
    ipSum = "";
    nodeSum = "";
    clusterSum = "";
    lastUpdate = "";

    if ovcIP == "NA":
        ipSum = "Please Login";
        nodeSum = "Please Login";
        clusterSum = "Please Login";
        lastUpdate = "Please Login";
    else:
        ipSum = ovcIP;
        nodeSum= len(hostsList);
        clusterSum = len(clustersList);
        lastUpdate = datetime.now();

    outputList.append(ipSum);
    outputList.append(nodeSum);
    outputList.append(clusterSum);
    outputList.append(lastUpdate);
    
    outputList.append(UpdateClusterReduction());
    outputList.append(UpdateClusterPhysical());
    outputList.append(UpdateClusterLogical());
    outputList.append(UpdateNodeLogical());
    outputList.append(UpdateNodePhysical());
    outputList.append(UpdateBackupDonuts(1));
    outputList.append(UpdateBackupDonuts(30));
    outputList.append(UpdateBackupDonuts(9999));

    return outputList;

#Draw Graphs DIV

def DrawCapacityReport():
    report = html.Div(id = "capacityReport", className = "container-fluid", children=[
        html.Div(className ='row mb-4 mt-4 pl-4',children=[
            html.H3(children='Simplivity quick summary.'),
            dcc.Interval(
                id = 'summary-update',
                interval = intervalSec * 1000,
                n_intervals = 0
            )
        ]),
        #Four Boxes Divs
        html.Div(className='row',children = [
            html.Div(className = 'col-xl-3 col-md-6 mb-4', children=[
                html.Div(className = 'card shadow h-100 py-2', children=[
                    html.Div(className = 'card-body',children=[
                        html.Div(className = 'row no-gutters align-items-center',children=[
                            html.Div(className = 'col',children=[
                                html.Div(className = 'text-xs font-weight-bold text-uppercase mb-1',style={'color':'#00b088'},children="OVC IP Address"),
                                DrawText('ipSum')
                            ]),
                        ]),
                    ]),
                ]),
            ]),
            html.Div(className = 'col-xl-3 col-md-6 mb-4', children=[
                html.Div(className = 'card shadow h-100 py-2', children=[
                    html.Div(className = 'card-body',children=[
                        html.Div(className = 'row no-gutters align-items-center',children=[
                            html.Div(className = 'col',children=[
                                html.Div(className = 'text-xs font-weight-bold text-uppercase mb-1',style={'color':'#00b088'},children="Total Clusters"),
                                DrawText('clusterSum')
                            ]),
                        ]),
                    ]),
                ]),
            ]),
            html.Div(className = 'col-xl-3 col-md-6 mb-4', children=[
                html.Div(className = 'card shadow h-100 py-2', children=[
                    html.Div(className = 'card-body',children=[
                        html.Div(className = 'row no-gutters align-items-center',children=[
                            html.Div(className = 'col',children=[
                                html.Div(className = 'text-xs font-weight-bold text-uppercase mb-1',style={'color':'#00b088'},children="Total Nodes"),
                                DrawText('nodeSum')
                            ]),
                        ]),
                    ]),
                ]),
            ]),
            html.Div(className = 'col-xl-3 col-md-6 mb-4', children=[
                html.Div(className = 'card shadow h-100 py-2', children=[
                    html.Div(className = 'card-body',children=[
                        html.Div(className = 'row no-gutters align-items-center',children=[
                            html.Div(className = 'col',children=[
                                html.Div(className = 'text-xs font-weight-bold text-uppercase mb-1',style={'color':'#00b088'},children="Total Backups"),
                                DrawText('backupSum')
                            ]),
                        ]),
                    ]),
                ]),
            ]),
        ]),
        #Cluster Summary
        html.Div(className ='row mt-4 mb-4 pl-4',children=[
            html.H3(children='Simplivity Capacity Reports.'),
        ]),
        html.Div(className='row',children=[   
            html.Div(className = 'col-xl-4 col-sm-12', children=[
                html.Div(className = 'card shadow mb-4', children = [
                    html.Div(className = 'card-header py-3 d-flex flex-row align-items-center justify-content-between',children=[
                        html.Div(className = 'h6 m-0 font-weight-bold', children = 'Logical Data per Cluster')
                    ]),
                    html.Div(className = 'card-body', children = [DrawGraph('cluster-logical-graph')]),
                ]),
            ]),
            html.Div(className = 'col-xl-4 col-sm-12', children=[
                html.Div(className = 'card shadow mb-4', children = [
                    html.Div(className = 'card-header py-3 d-flex flex-row align-items-center justify-content-between',children=[
                        html.Div(className = 'h6 m-0 font-weight-bold', children = 'Physical Data usage per Clusters')
                    ]),
                    html.Div(className = 'card-body', children = [DrawGraph('cluster-physical-graph')]),
                ]),
            ]),
            html.Div(className = 'col-xl-4 col-sm-12', children=[
                html.Div(className = 'card shadow mb-4', children = [
                    html.Div(className = 'card-header py-3 d-flex flex-row align-items-center justify-content-between',children=[
                        html.Div(className = 'h6 m-0 font-weight-bold', children = 'Data efficiency per Clusters')
                    ]),
                    html.Div(className = 'card-body', children = [DrawGraph('cluster-reduction-graph')]),
                ]),
            ]),
        ]),
        #Node Summary
        html.Div(className='row',children=[   
            html.Div(className = 'col-xl-6 col-sm-12', children=[
                html.Div(className = 'card shadow mb-4', children = [
                    html.Div(className = 'card-header py-3 d-flex flex-row align-items-center justify-content-between',children=[
                        html.Div(className = 'h6 m-0 font-weight-bold', children = 'Logical Data per Nodes')
                    ]),
                    html.Div(className = 'card-body', children = [DrawGraph('logical-graph')]),
                ]),
            ]),
            html.Div(className = 'col-xl-6 col-sm-12', children=[
                html.Div(className = 'card shadow mb-4', children = [
                    html.Div(className = 'card-header py-3 d-flex flex-row align-items-center justify-content-between',children=[
                        html.Div(className = 'h6 m-0 font-weight-bold', children = 'Physical Data usage per Nodes')
                    ]),
                    html.Div(className = 'card-body', children = [DrawGraph('physical-graph')]),
                ]),
            ]),
        ]),
        dcc.Interval(
            id = 'capacityUpdate',
            interval = intervalSec * 1000,
            n_intervals = 0
        ),
    ]);
    return report;

def DrawBackupReport():
    report = html.Div(id = "backupReport", className = "container-fluid", children=[
        html.Div(className ='row mt-4 mb-4 pl-4',children=[
            html.H3(children='Simplivity Backup Reports.'),
        ]),
        html.Div(className='row',children=[   
            html.Div(className = 'col-xl-4 col-sm-12', children=[
                html.Div(className = 'card shadow mb-4', children = [
                    html.Div(className = 'card-header py-3 d-flex flex-row align-items-center justify-content-between',children=[
                        html.Div(id ='backupSumText',className = 'h6 col-9 m-0 font-weight-bold', children =  'Backup summary since 1 Day'),
                        html.Div(className = 'col-3',children=[
                            dcc.Dropdown(id = 'backupDropDown',options=[
                                {'label': '1 Day', 'value': 1},
                                {'label': '1 Week', 'value': 7},
                                {'label': '1 Month', 'value': 30},
                                {'label': 'All time', 'value': 9999}
                            ],
                            searchable = False   
                            ) 
                        ])
                    ]),
                    html.Div(className = 'card-body', children = [DrawGraph('24h-backup')]),
                ]),
            ]),
            html.Div(className = 'col-xl-4 col-sm-12', children=[
                html.Div(className = 'card shadow mb-4', children = [
                    html.Div(className = 'card-header py-3 d-flex flex-row align-items-center justify-content-between',children=[
                        html.Div(className = 'h6 m-0 font-weight-bold', children =  'No of VM s per backup policy'),
                    ]),
                    html.Div(className = 'card-body', children = [DrawGraph('vm-policy-graph')]),
                ]),
            ]),
            html.Div(className = 'col-xl-4 col-sm-12', children=[
                html.Div(className = 'card shadow mb-4', children = [
                    html.Div(className = 'card-header py-3 d-flex flex-row align-items-center justify-content-between',children=[
                        html.Div(className = 'h6 m-0 font-weight-bold', children =  'Backup retention histogram'),
                    ]),
                    html.Div(className = 'card-body', children = [DrawGraph('all-backup')]),
                ]),
            ]),
        ]),
        html.Div(className ='row',children=[
            html.Div(className = 'col-xl-12 col-sm-12', children=[
                html.Div(className = 'card shadow mb-4', children = [
                    html.Div(className = 'card-header py-3 d-flex flex-row align-items-center justify-content-between',children=[
                        html.Div(className = 'h6 m-0 font-weight-bold', children =  'Backup Creation Heatmap'),
                    ]),
                    html.Div(className = 'card-body', children = [DrawGraph('heatmap')]),
                ]),
            ]),
            dcc.Interval(
                id = 'backupUpdate',
                interval = 10 * 1000,
                n_intervals = 0
            )

        ]),
    ]);
    return report;

def DrawLoginPage():
    global ovcIP, ovcPass, ovcUser;
    print(ovcIP);

    
    loginPage = html.Nav(id = "loginPage",className = "navbar navbar-expand-sm bg-dark navbar-dark shadow", children=[
            html.Span(className = 'navbar-brand', children = 'OVC Mon'),
            html.Span(children='OVC IP: ', style={"margin-left":30},className = 'navbar-text'),
            html.Div(children=[   
                dcc.Input(id='ipInput', style={"width":'16vw',"margin-left":10}, className = 'form-control' , type='text', value=defOVCIP),
            ]),
            html.Span(children='OVC Username: ', style={"margin-left":30},className = 'navbar-text'),
            html.Div(children=[   
                dcc.Input(id='userInput', style={"width":'16vw',"margin-left":10}, className = 'form-control' , type='text', value=defOVCUser)
            ]),
            html.Span(children='OVC Password: ', style={"margin-left":30},className = 'navbar-text'),
            html.Div(children=[   
                dcc.Input(id='passwordInput', style={"width":'16vw',"margin-left":10}, className = 'form-control', type='password', value=defOVCPass),
            ]),    
            html.Button(id='loginButton', className = 'btn btn-primary',n_clicks=0, children='Log In'),
            html.Span(id = 'logInMessage', style={"margin-left":30},  className = 'navbar-text'),
    ]);
    return loginPage;

def DrawHeader():
    header = html.Div(className="container-fluid",style = {'width':widthPage,'margin-left':marginPage,'padding-top':20},children=[
        
        html.Div(className ='row',children=[
            dcc.Interval(
            id = 'relogin',
            interval = reloginInterval * 1000,
            n_intervals = 0
            ),
            html.H1(children='Simplivity At A Glance Report'),
            #html.Button(id='refreshButton',style = {'margin-left':10}, className = 'btn btn-primary',n_clicks=0, children='Refresh')
        ]),
        html.Div(className ='row',children=[
            dcc.Interval(
            id = 'autoUpdate',
            interval = intervalSec * 1000,
            n_intervals = 0
            ),
            dcc.Interval(
            id = 'autoBackupUpdate',
            interval = intervalSec * 1000,
            n_intervals = 0
            ),
            html.H6(children='Last sucessful update at :  '),
            DrawText('lastUpdate'),
            html.H6(children = '', id = 'lastBackupUpdate')
        ]),

    ]);
    return header;

hostNum = GetHostCount();

app = dash.Dash(__name__)
app.title = "OVC Mon";
isCapacity = True;
isBackup = True;

InitialOutputComponent();
donutColors = ['rgb(0,177,136)','rgb(91,71,103)','rgb(255,141,109)','rgb(128,130,133)','rgb(100,100,100)'];

loginPage = DrawLoginPage();
header = DrawHeader();
capacityReport = DrawCapacityReport();
backupReport = DrawBackupReport();
dashboard = html.Div(style={'bgcolor':'rgb(30,30,30)'},children = [loginPage,header,capacityReport, backupReport]);
app.layout = dashboard;


@app.callback([Output('logical-graph', 'figure'),
            Output('physical-graph', 'figure'),
            Output('cluster-reduction-graph', 'figure'),
            Output('cluster-logical-graph', 'figure'),
            Output('cluster-physical-graph', 'figure'),
    ], 
    [Input('capacityUpdate', 'n_intervals')])
def OnCapacityUpdate(n):
    return [UpdateNodeLogical(),
            UpdateNodePhysical(),
            UpdateClusterReduction(),
            UpdateClusterLogical(),
            UpdateClusterPhysical()];

@app.callback([Output('24h-backup', 'figure'),
                Output('vm-policy-graph', 'figure'),
                Output('all-backup', 'figure'),
                Output('heatmap', 'figure')], 
    [Input('backupUpdate', 'n_intervals')])
def OnBackupUpdate(n):
    global backupSumDay;
    print(backupSumDay)
    return [UpdateBackupDonuts(backupSumDay),
            UpdateVMPolicy(),
            UpdateBackupHistogram(),
            UpdateBackupHeatMap()
    ];

@app.callback([Output('logInMessage', 'children'),
                Output('ipInput', 'value'),
                Output('userInput', 'value'),
                Output('passwordInput', 'value'),
                Output('autoUpdate', 'interval'),
                Output('autoBackupUpdate', 'interval')],
                [Input('loginButton', 'n_clicks')],
                [State('ipInput', 'value'),
                State('userInput', 'value'),
                State('passwordInput','value')])
def OnLoginClick(n_clicks, ipInput, userInput, passInput):
    global ovcIP, ovcPass, ovcUser, defOVCIP, defOVCPass, defOVCUser;
    if n_clicks == 0:
        return;
    result = Login(ipInput, userInput, passInput);
    if result == "error":
        return ['Cannot Log in to OVC',ipInput, userInput, passInput,5000,5000];
    else :
        ovcIP = ipInput;
        ovcUser = userInput;
        ovcPass = passInput;

        print 'OVCIP Updated';
        print ovcIP;
        UpdateAllInventory();
        UpdateAllBackup();
        return ['Log in successful',defOVCIP, defOVCUser, defOVCPass,60000,3600000];

@app.callback(Output('backupSumText', 'children'),[
                Input('backupDropDown', 'value')])
def OnBackupDayUpdate(value):
    global backupSumDay;

    label = "";
    if value == 1:
            label = "1 Day";
    elif value == 7:
        label = "1 Week";
    elif value == 30:
            label = "1 Month";
    else:
        label = "All time";
        value = 9999;
    backupSumDay = value;
    return 'Backup Summary since ' + label;

@app.callback(Output('relogin', 'interval'), 
    [Input('relogin', 'n_intervals')])
def reLogin(n):
    global ovcIP, ovcPass, ovcUser;
    if ovcIP == "NA":
        return 30*1000;
    result = Login(ovcIP,ovcUser, ovcPass);
    if result == "error":
        ovcIP = "NA";
        return 30*1000;
    else:
        return 30*1000;


@app.callback([Output('ipSum', 'children'), 
        Output('nodeSum', 'children'),
        Output('clusterSum', 'children'),
        Output('backupSum', 'children'),
    ],
    [Input('summary-update', 'n_intervals')])
def OnUpdateSummary(n):
    global ovcIP, nodesList, clustersList, backupList;
    if ovcIP == "NA":
        return ['Please Login','Please Login','Please Login','Please Login'];
    nodes = hostsList;
    clusters = clustersList;

    return [ovcIP, len(nodes), len(clusters), len(backupList)];

@app.callback(Output('lastUpdate', 'children'), 
    [Input('autoUpdate', 'n_intervals')])
def AutoUpdate(n):
    global ovcIP, ovcPass, ovcUser;
    if ovcIP == "NA":
        return 'Please Login'
    
    UpdateAllInventory();
    hostNum = GetHostCount();
    return datetime.now();


@app.callback(Output('lastBackupUpdate', 'children'), 
    [Input('autoBackupUpdate', 'n_intervals')])
def AutoBackupUpdate(n):
    global ovcIP, ovcPass, ovcUser, llCluster, backupList;
    if ovcIP == "NA":
        return ''
    UpdateAllBackup();
    hostNum = GetHostCount();
    return '';


if __name__ == '__main__':
    app.run_server(port=80,host='0.0.0.0')
 



