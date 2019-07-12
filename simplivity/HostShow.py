# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
from SimplivityCluster import SimplivityCluster;
import sys;
import os.path;
import plotly.graph_objs as go;

def GetHostsCapacityData():

    llCluster = SimplivityCluster("172.30.5.31", "administrator@vsphere.local", "P@ssw0rd");
    llCluster.Initialize();
    hostList = llCluster.GetHostsAll();
    outputList = {};
    nodeList = [];
    nodeVMData = [];
    nodeLocalBackup = [];
    nodeRemoteBackup = [];

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

    llCluster = SimplivityCluster("172.30.5.31", "administrator@vsphere.local", "P@ssw0rd");
    llCluster.Initialize();
    hostList = llCluster.GetHostsAll();
    outputList = {};
    nodeList = [];
    usedCapList = [];
    leftCapList = [];

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

external_stylesheets = ['./myStyle.css']
    #{'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},

data = GetHostsCapacityData();
physData = GetPhysicalData();

vmTrace = go.Bar(
    y = data['name'],
    x = data['vmData'],
    name = 'VM Data (TiB)',
    orientation = 'h'
    );
localBackupTrace = go.Bar(
    y = data['name'],
    x = data['localBackup'],
    name = 'Local Backup (TiB)',
    orientation = 'h'
    );
remoteBackupTrace = go.Bar(
    y = data['name'],
    x = data['remoteBackup'],
    name = 'Remote Backup (TiB)',
    orientation = 'h'
    );

usedTrace = go.Bar(
    y = physData['name'],
    x = physData['usedCap'],
    name = 'Used Capacity (TiB)',
    orientation = 'h'
    );
leftTrace = go.Bar(
    y = physData['name'],
    x = physData['leftCap'],
    name = 'Free Capacity (TiB)',
    orientation = 'h'
    );

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Simplivity Capacity Usage'),

    html.Div(children='''
        Logical Usage: Sperated by data type (TiB).
    '''),    
    dcc.Graph(
        id='Host logical capacity (TiB)',
        figure= go.Figure(data=[vmTrace,localBackupTrace,remoteBackupTrace],
            layout = go.Layout(barmode="stack")
        )
    ),

    html.Div(children='''
        Physical Usage: Sperated by node physical usage (TiB).
    '''),    
    dcc.Graph(
        id='Host physical capacity (TiB)',
        figure= go.Figure(data=[usedTrace,leftTrace],
            layout = go.Layout(barmode="stack")
        )
    )
]);




if __name__ == '__main__':
    app.run_server(port=8080,host='0.0.0.0')