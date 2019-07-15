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
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go;

logging.getLogger('werkzeug').setLevel(logging.ERROR);
#OVC Credential
ovcIP = "NA";
ovcUser = "NA";
ovcPass = "NA";
llCluster = {};
#Inventory
hostsList = {}
clustersList = {};
#Interval
intervalSec = 5;
reloginInterval = 1800;
widthPage = '94vw';
marginPage = '3vw';

def UpdateAllInventory():
    global ovcIP, hostsList, clustersList;
    if ovcIP =="NA":
          return;
    clustersList = llCluster.GetClustersAll();
    hostsList = llCluster.GetHostsAll();

def Login(ovcIP, ovcUser, ovcPass):
    global llCluster;

    llCluster = SimplivityCluster(ovcIP, ovcUser, ovcPass);
    result =  llCluster.Initialize();

    UpdateAllInventory();

    return result;

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
    global ovcIP, dayBackupList;
    resultList = {};

    if ovcIP == "NA":
        resultList["Please Login"] = 1;
        return resultList;

    targetDate = datetime.now() - timedelta(days=n);
    
    backupList = llCluster.GetBackUpsFrom(targetDate);
    if backupList == {}:
        resultList["None"] = 1;
        return;
    #Check every Backup state and add counts
    for backup in backupList:
        if (backup['state'] in resultList):
            resultList[backup['state']] += 1;
        else:
            resultList[backup['state']] = 0;

    return resultList;

def DrawCapacityReport():
    report = html.Div(id = "capacityReport", className = "container-fluid", children=[
        html.Div(className ='row',style = {'width':widthPage, 'margin-left':marginPage},children=[
            html.H2(children='Simplivity quick summary.'),
            dcc.Interval(
                id = 'summary-update',
                interval = intervalSec * 1000,
                n_intervals = 0
            )
        ]),
        html.Div(className='row',style={'width':widthPage, 'margin-left':marginPage,'height':'50vh'},children=[
            html.Div(className = 'col-4', children=[
                html.Div(style={'text-align':'center','margin-top':'12%'},children=[html.H4( children ="Federation Dashboard")]),
                html.Div(className='row',children=[
                    html.Div(className='col-6',style={'text-align':'right', 'vertical-align':'center'},children=[
                        html.H5(style={'display':'inline-block','margin-top':'5%'}, children ="OVC IP Address :"),
                    ]),
                    html.Div(className='col-6',style={'text-align':'left', 'vertical-align':'center'},children=[
                        html.H5(id='ipSum',style={'display':'inline-block','margin-top':'5%'}, children ="Please Login"),
                    ]),
                ]),
                html.Div(className='row',children=[
                    html.Div(className='col-6',style={'text-align':'right', 'vertical-align':'center'},children=[
                        html.H5(style={'display':'inline-block','margin-top':'5%'}, children ="Total Nodes :"),
                    ]),
                    html.Div(className='col-6',style={'text-align':'left', 'vertical-align':'center'},children=[
                        html.H5(id='nodeSum',style={'display':'inline-block','margin-top':'5%'}, children ="Please Login"),
                    ]),
                ]),
                html.Div(className='row',children=[
                    html.Div(className='col-6',style={'text-align':'right', 'vertical-align':'center'},children=[
                        html.H5(style={'display':'inline-block','margin-top':'5%'}, children ="Total Clusters :"),
                    ]),
                    html.Div(className='col-6',style={'text-align':'left', 'vertical-align':'center'},children=[
                        html.H5(id='clusterSum',style={'display':'inline-block','margin-top':'5%'}, children ="Please Login"),
                    ]),
                ]),
            ]),
            html.Div(className = 'col-4', children=[
                html.Div(className='row',style={'height':'10%'},children=[html.H5(children=["Cluster's Data Reduction Ratio."])]),   
                html.Div(className='row',style={'height':'90%'},children=[
                    dcc.Graph(
                        id='cluster-reduction-graph',
                        animate=True,
                        style = {'height':'100%','width':'100%'}           
                    ),
                ]),
                dcc.Interval(
                    id = 'cluster-reduction-update',
                    interval = intervalSec * 1000,
                    n_intervals = 0
                )
            ]),
            html.Div(className = 'col-4', children=[
                html.Div(className='row',style={'height':'10%'},children=[html.H5(children=["Cluster's Data Consumption."])]),   
                html.Div(className='row',style={'height':'90%'},children=[
                    dcc.Graph(
                        id='cluster-physical-graph',
                        animate=True,
                        style = {'height':'100%','width':'100%'}           
                    ),
                ]),
                dcc.Interval(
                    id = 'cluster-physical-update',
                    interval = intervalSec * 1000,
                    n_intervals = 0
                )
            ]),
        ]),
        html.Div(className='row',style={'width':widthPage,'padding-top':0, 'margin-left':marginPage,'height':(hostNum*25+300)},children=[
            html.Div(className = 'col-4', children=[
                html.Div(className='row',style={'height':'10%'},children=[html.H5(children=["Cluster's Logical Data."])]),   
                html.Div(className='row',style={'height':'90%'},children=[
                    dcc.Graph(
                        id='cluster-logical-graph',
                        animate=True,
                        style = {'height':'100%','width':'100%'}           
                    ),
                ]),
                dcc.Interval(
                    id = 'cluster-logical-update',
                    interval = intervalSec * 1000,
                    n_intervals = 0
                )
            ]),
            html.Div(className = 'col-4', children=[
                html.Div(className='row',style={'height':'10%'},children=[html.H5(children=["Node's Logical Data comsumption (TiB)"])]),   
                html.Div(className='row',style={'height':'90%'},children=[
                    dcc.Graph(
                        id='logical-graph',
                        animate=True,
                        style = {'height':'100%','width':'100%'}           
                    ),
                ]),
                dcc.Interval(
                    id = 'logical-update',
                    interval = intervalSec * 1000,
                    n_intervals = 0
                )
            ]),
            html.Div(className = 'col-4', children=[
                html.Div(className='row',style={'height':'10%'},children=[html.H5(children=["Node's Data comsumption (TiB)"])]),   
                html.Div(className='row',style={'height':'90%'},children=[
                    dcc.Graph(
                        id='physical-graph',
                        animate=True,
                        style = {'height':'100%','width':'100%'}           
                    ),
                ]),
                dcc.Interval(
                    id = 'physical-update',
                    interval = intervalSec * 1000,
                    n_intervals = 0
                )
            ]),
        ]),
    ]);
    return report;

def DrawBackupReport():
    report = html.Div(id = "backupReport", className = "container-fluid", children=[
        html.Div(className ='row',style={'width':widthPage, 'margin-left':marginPage,'padding-top':70},children=[
            html.H2(children='Simplivity backup report.'),
        ]),
        html.Div(className ='row',style={'width':widthPage, 'margin-left':marginPage},children=[
            html.Div(className ='col-4', children=[
                html.H5(children='''
                 Backup report since last 24 hours.
                '''),  
                dcc.Graph(
                    id='24h-backup',
                    animate=True       
                ),
                dcc.Interval(
                    id = '24h-update',
                    interval = intervalSec * 1000,
                    n_intervals = 0
                ),
            ]),
            html.Div(className ='col-4', children=[
                html.H5(children='''
                 Backup report since last 1 Month.
                '''),    
            
                dcc.Graph(
                    id='30d-backup',
                    animate=True       
                ),
                dcc.Interval(
                    id = '30d-update',
                    interval = intervalSec * 1000,
                    n_intervals = 0
                ),
            ]),
            html.Div(className ='col-4', children=[
                html.H5(children='''
                 Backup report overall.
                '''),    
            
                dcc.Graph(
                    id='all-backup',
                    animate=True       
                ),
                dcc.Interval(
                    id = 'all-update',
                    interval = intervalSec * 1000,
                    n_intervals = 0
                ),
            ]),
        ]),
    ]);
    return report;

def DrawLoginPage():
    global ovcIP, ovcPass, ovcUser;
    print(ovcIP);

    
    loginPage = html.Nav(id = "loginPage",className = "navbar navbar-expand-sm bg-dark navbar-dark", children=[
            html.Span(className = 'navbar-brand', children = 'OVC Mon'),
            html.Span(children='OVC IP: ', style={"margin-left":30},className = 'navbar-text'),
            html.Div(children=[   
                dcc.Input(id='ipInput', style={"width":'16vw',"margin-left":10}, className = 'form-control' , type='text', value='172.30.5.31'),
            ]),
            html.Span(children='OVC Username: ', style={"margin-left":30},className = 'navbar-text'),
            html.Div(children=[   
                dcc.Input(id='userInput', style={"width":'16vw',"margin-left":10}, className = 'form-control' , type='text', value='administrator@vsphere.local'),
            ]),
            html.Span(children='OVC Password: ', style={"margin-left":30},className = 'navbar-text'),
            html.Div(children=[   
                dcc.Input(id='passwordInput', style={"width":'16vw',"margin-left":10}, className = 'form-control', type='password', value='P@ssw0rd'),
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
        ]),
        html.Div(className ='row',children=[
            dcc.Interval(
            id = 'autoUpdate',
            interval = intervalSec * 1000,
            n_intervals = 0
            ),
            html.H6(children='Last sucessful update at :  '),
            html.H6(id = 'lastUpdate',children='Please Login'),
        ]),

    ]);
    return header;

#external_stylesheets = [dbc.themes.BOOTSTRAP];
hostNum = GetHostCount();


app = dash.Dash(__name__)
app.title = "OVC Mon";
isCapacity = True;
isBackup = True;

donutColors = ['rgb(0,177,136)','rgb(91,71,103)','rgb(255,141,109)','rgb(128,130,133)','rgb(100,100,100)'];

loginPage = DrawLoginPage();
header = DrawHeader();
capacityReport = DrawCapacityReport();
backupReport = DrawBackupReport();
dashboard = html.Div(style={'bgcolor':'rgb(30,30,30)'},children = [loginPage,header,capacityReport, backupReport]);
app.layout = dashboard;


@app.callback(Output('cluster-logical-graph', 'figure'), 
    [Input('cluster-logical-update', 'n_intervals')])
def UpdateClusterLogical(n):

    data = GetClustersCapacityData();
    nameCount = 0;
    maxCap = 0;
    for name in data['name']:
        totalCap = data['vmData'][nameCount]+data['localBackup'][nameCount]+data['remoteBackup'][nameCount];
        nameCount = nameCount + 1;
        if (totalCap > maxCap):
                maxCap = totalCap;
    vmTrace = go.Bar(
        y = data['name'],
        x = data['vmData'],
        name = 'VM Data (TiB)',
        orientation = 'h',
        marker = dict(
            color = 'rgb(91,71,103)'
            )
        );
    localBackupTrace = go.Bar(
        y = data['name'],
        x = data['localBackup'],
        name = 'Local Backup (TiB)',
        orientation = 'h',
        marker = dict(
            color = 'rgb(255,141,109)'
            )
        );
    remoteBackupTrace = go.Bar(
        y = data['name'],
        x = data['remoteBackup'],
        name = 'Remote Backup (TiB)',
        orientation = 'h',
        marker = dict(
            color = 'rgb(128,130,133)'
            )
        );
    dataOutput = [vmTrace,localBackupTrace,remoteBackupTrace];
    barLayout = go.Layout(xaxis = dict(range = [0,maxCap], title='Effective Capacity (TiB)'),yaxis = dict(range = [-1,nameCount]),barmode="stack");
    print("\nCluster's Logical Graph updated");
    return {'data' : dataOutput, 'layout' : barLayout}

@app.callback(Output('logical-graph', 'figure'), 
    [Input('logical-update', 'n_intervals')])
def UpdateLogical(n):

    data = GetHostsCapacityData();
    nameCount = 0;
    maxCap = 0;
    for name in data['name']:
        totalCap = data['vmData'][nameCount]+data['localBackup'][nameCount]+data['remoteBackup'][nameCount];
        nameCount = nameCount + 1;
        if (totalCap > maxCap):
                maxCap = totalCap;
    vmTrace = go.Bar(
        y = data['name'],
        x = data['vmData'],
        name = 'VM Data (TiB)',
        orientation = 'h',
        marker = dict(
            color = 'rgb(91,71,103)'
            )
        );
    localBackupTrace = go.Bar(
        y = data['name'],
        x = data['localBackup'],
        name = 'Local Backup (TiB)',
        orientation = 'h',
        marker = dict(
            color = 'rgb(255,141,109)'
            )
        );
    remoteBackupTrace = go.Bar(
        y = data['name'],
        x = data['remoteBackup'],
        name = 'Remote Backup (TiB)',
        orientation = 'h',
        marker = dict(
            color = 'rgb(128,130,133)'
            )
        );
    dataOutput = [vmTrace,localBackupTrace,remoteBackupTrace];
    barLayout = go.Layout(xaxis = dict(range = [0,maxCap], title='Effective Capacity (TiB)'),yaxis = dict(range = [-1,nameCount]),barmode="stack");
    print("\nLogical Graph updated");
    return {'data' : dataOutput, 'layout' : barLayout}

@app.callback(Output('physical-graph', 'figure'), 
    [Input('physical-update', 'n_intervals')])
def UpdatePhysical(n):
    
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
        y = physData['name'],
        x = physData['usedCap'],
        name = 'Used Capacity (TiB)',
        orientation = 'h',
        marker = dict(
            color = 'rgb(0,177,136)'
            )
        );
    leftTrace = go.Bar(
        y = physData['name'],
        x = physData['leftCap'],
        name = 'Free Capacity (TiB)',
        orientation = 'h',
        marker = dict(
            color = 'rgb(200,200,200)'
            )
        );

    dataOutput = [usedTrace,leftTrace];
    barLayout = go.Layout(xaxis = dict(range = [0,maxCap], title='Physical Capacity (TiB)'),yaxis = dict(range = [-1,nameCount]),barmode="stack");
    print("\nPhysical Graph updated");
    return {'data' : dataOutput, 'layout' : barLayout};


@app.callback(Output('cluster-reduction-graph', 'figure'), 
    [Input('cluster-reduction-update', 'n_intervals')])
def UpdateReduction(n):
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
    barLayout = go.Layout(xaxis = dict(range = [-1,nameCount]),yaxis = dict(range = [0,maxCap], title='Data Reduction Ratio (x)'), barmode='group');
    print("\nLogical Graph updated");
    return {'data' : dataOutput, 'layout' : barLayout}

@app.callback(Output('cluster-physical-graph', 'figure'), 
    [Input('cluster-physical-update', 'n_intervals')])
def UpdateClusterPhysical(n):
    
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
    barLayout = go.Layout(xaxis = dict(range = [-1,nameCount]),yaxis = dict(range = [0,maxCap], title='Physical Capacity (TiB)'),barmode="stack");
    print("\nCluster Physical Graph updated");
    return {'data' : dataOutput, 'layout' : barLayout};

@app.callback(Output('24h-backup', 'figure'), 
    [Input('24h-update', 'n_intervals')])
def dayUpdate(n):
    
    allBackup = GetBackupLastNDay(1);
    statusList = [];
    countList = [];
    donutLayout = {
        "title":"Statuses of Backups",
        "grid": {"rows": 1, "columns": 1},
        "annotations": [
            {
                "font": {"size": 20},
                "showarrow": False,
                "text": "24 Hrs",
                "x": 0.5,
                "y": 0.5
            }
        ]
    }
    holeSize = 0.8;

    for key in allBackup:
        if key =="Please Login":
            holeSize = 1;
        statusList.append(key);
        countList.append(allBackup[key]);
    data = {"values":countList,
        "labels":statusList,
        "domain": {"column": 0},
        "name": "Backup Status",
        "hoverinfo":"label+percent+name",
        "hole": holeSize,
        "type": "pie",
        "marker":{"colors":donutColors},
    }
    dataOutput = [data];
    print("\n24hrs backup updated");
    return {'data' : dataOutput, 'layout' : donutLayout};

@app.callback(Output('30d-backup', 'figure'), 
    [Input('30d-update', 'n_intervals')])
def monthUpdate(n):

    allBackup = GetBackupLastNDay(30);
    statusList = [];
    countList = [];
    donutLayout = {
        "title":"Statuses of Backups",
        "grid": {"rows": 1, "columns": 1},
        "annotations": [
            {
                "font": {"size": 20},
                "showarrow": False,
                "text": "1 Month",
                "x": 0.5,
                "y": 0.5
            }
        ]
    }

    holeSize = 0.8;

    for key in allBackup:
        if key =="Please Login":
               holeSize = 1;
        statusList.append(key);
        countList.append(allBackup[key]);
    data = {"values":countList,
        "labels":statusList,
        "domain": {"column": 0},
        "name": "Backup Status",
        "hoverinfo":"label+percent+name",
        "hole": holeSize,
        "type": "pie",
        "marker":{"colors":donutColors},
    }
    dataOutput = [data];
    print("\n30hrs backup updated");
    return {'data' : dataOutput, 'layout' : donutLayout};

@app.callback(Output('all-backup', 'figure'), 
    [Input('all-update', 'n_intervals')])
def allUpdate(n):

    completeCount = 0;
    backupCount = 0;
    allBackup = GetBackupLastNDay(9999);
    statusList = [];
    countList = [];
    donutLayout = {
        "title":"Statuses of Backups",
        "grid": {"rows": 1, "columns": 1},
        "annotations": [
            {
                "font": {"size": 20},
                "showarrow": False,
                "text": "All Backups",
                "x": 0.5,
                "y": 0.5
            }
        ]
    }
    holeSize = 0.8;

    for key in allBackup:
        if key =="Please Login":
               holeSize = 1;
        statusList.append(key);
        countList.append(allBackup[key]);
    data = {"values":countList,
        "labels":statusList,
        "domain": {"column": 0},
        "name": "Backup Status",
        "hoverinfo":"label+percent+name",
        "hole": holeSize,
        "type": "pie",
        "marker":{"colors":donutColors},
    }
    dataOutput = [data];
    print("\nAll backup updated");
    return {'data' : dataOutput, 'layout' : donutLayout};

@app.callback(Output('logInMessage', 'children'),
                [Input('loginButton', 'n_clicks')],
                [State('ipInput', 'value'),
                State('userInput', 'value'),
                State('passwordInput','value')])
def loginClick(n_clicks, input1, input2, input3):
    global ovcIP, ovcPass, ovcUser;
    if n_clicks == 0:
        return;
    result = Login(input1, input2, input3);
    if result == "error":
        return 'Cannot Log in to OVC';
    else :
        ovcIP = input1;
        ovcUser = input2;
        ovcPass = input3;
        intervalSec = 5;

        print 'OVCIP Udated';
        print ovcIP;
        return 'Login Successful';

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
    ],
    [Input('summary-update', 'n_intervals')])
def UpdateSummary(n):
    global ovcIP, nodesList, clustersList;
    if ovcIP == "NA":
        return ['Please Login','Please Login','Please Login'];
    nodes = hostsList;
    clusters = clustersList;

    return [ovcIP, len(nodes), len(clusters)];



@app.callback(Output('lastUpdate', 'children'), 
    [Input('autoUpdate', 'n_intervals')])
def AutoUpdate(n):
    global ovcIP, ovcPass, ovcUser;
    if ovcIP == "NA":
        return 'Please Login'
    
    UpdateAllInventory();

    return datetime.now();



if __name__ == '__main__':
    app.run_server(port=8080,host='0.0.0.0')
 



