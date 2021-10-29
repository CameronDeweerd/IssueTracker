"""This will contain the different methods used to query the chart data for the dashboard"""
from SQLhelpers import return_query, check_permission
from flask import escape

'''# of current user's tickets per status'''
def myTicketStatus(user):

    # pull the list of issues and the list of statuses
    statusOptions = return_query("SELECT Type FROM Status")
    if check_permission('CanViewUnassigned'):
        ticketList = return_query("SELECT issue_status FROM Issues WHERE user_assigned_to IS Null")
    else:
        ticketList = return_query("SELECT issue_status FROM Issues WHERE user_assigned_to IS ?", user)

    numTicketsByStatus = tableCounter(statusOptions, ticketList)
    print(list(numTicketsByStatus.keys()))
    print(list(numTicketsByStatus.values()))

    options = getDefaultOptions()
    backgroundColor, borderColor = getColors(len(numTicketsByStatus))

    jsonData = {
        'type': 'doughnut',
        'data': {
            'labels': list(numTicketsByStatus.keys()),
            'datasets': [{
                'label': list(numTicketsByStatus.keys()),
                'data': list(numTicketsByStatus.values()),
                'backgroundColor': backgroundColor,
                'borderColor': borderColor,
                'borderWidth': 1
            }]
        },
        'options': options
    }
    # jsonData = "'" + str(jsonData).replace("'", "`") + "'"
    print(jsonData)

    return jsonData


'''# of open tickets per category'''
def openIssuesByCategory():
    return


'''bucket display of closed tickets (completion date - creation date)'''
def ticketTurnaroundTime():
    return


'''# of open tickets each employee currently has'''
def workloadBreakdown():


    return


'''given a 1 column key table and 1 column table of countables, return a dict of counted data'''
def tableCounter(keys, tableToCount):
    if keys and tableToCount:
        dictionary = {}
        keysKey = list(keys[0].keys())[0]
        tableToCountKey = list(tableToCount[0].keys())[0]

        for row in range(len(keys)):
            status = keys[row][keysKey]
            dictionary[status] = 0

        for row in range(len(keys)):
            status = tableToCount[row][tableToCountKey]
            dictionary[status] += 1
        return dictionary
    else:
        return


def getDefaultOptions():
    defaultOptions = {
        'aspectRatio': 1,
        'responsive': 1,
        'maintainAspectRatio': 0,
    }
    return defaultOptions


def getColors(number):

    backgroundColor = [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)'
    ]

    borderColor = [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)'
    ]

    return backgroundColor[0:number], borderColor[0:number]
