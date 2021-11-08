"""This will contain the different methods used to query the chart data for the dashboard"""
from SQLhelpers import return_query, check_permission

'''# of current user's tickets per status'''
def myTicketStatus(user):

    # pull the list of issues and the list of statuses
    statusOptions = return_query("SELECT Type FROM Status")
    if check_permission('CanViewUnassigned'):
        ticketList = return_query("SELECT issue_status FROM Issues WHERE user_assigned_to = Null OR user_assigned_to = ?", (user,))
        print('unassigned')
    else:
        print(user)
        ticketList = return_query('SELECT issue_status FROM Issues WHERE user_assigned_to = ?', (user,))
        print("assigned")

    numTicketsByStatus = tableCounter(statusOptions, ticketList)

    options = getDefaultOptions(f'Status of Issues that are assigned to {user}')
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

    return jsonData


'''# of open tickets per category'''
def openIssuesByCategory(user=''):
    print("open Issues by Category")
    # pull the list of issues and the list of categories
    categoryOptions = return_query("SELECT category FROM Categories")
    ticketList = return_query("SELECT issue_category FROM Issues WHERE NOT issue_status = 'Closed'")

    numTicketsByCategory = tableCounter(categoryOptions, ticketList)

    options = getDefaultOptions(f'Open Tickets by Category')
    backgroundColor, borderColor = getColors(len(numTicketsByCategory))

    jsonData = {
        'type': 'bar',
        'data': {
            'labels': list(numTicketsByCategory.keys()),
            'datasets': [{
                'label': 'Number of Tickets',
                'data': list(numTicketsByCategory.values()),
                'backgroundColor': backgroundColor,
                'borderColor': borderColor,
                'borderWidth': 1
            }]
        },
        'options': options
    }

    return jsonData



'''bucket display of closed tickets (completion date - creation date)'''
def ticketTurnaroundTime():
    return


'''Count of tickets submitted by the current user and their status'''
def mySubmittedTickets(user):

    # pull the list of issues and the list of statuses
    statusOptions = return_query("SELECT Type FROM Status")
    ticketList = return_query("SELECT issue_status FROM Issues WHERE user_submitted_by = ?", (user,))

    numTicketsByStatus = tableCounter(statusOptions, ticketList)

    options = getDefaultOptions(f'Status of tickets submitted by {user}')
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

    return jsonData

'''# of open tickets each employee currently has'''
def workloadBreakdown():
    # pull the list of issues and the list of categories
    userList = return_query("SELECT Username FROM Users")
    ticketList = return_query("SELECT user_assigned_to FROM Issues WHERE NOT issue_status = 'Closed' AND NOT issue_status = 'unassigned'")

    print(ticketList)

    numTicketsByUser = tableCounter(userList, ticketList)

    options = getDefaultOptions('Open Tickets by Users')
    backgroundColor, borderColor = getColors(len(numTicketsByUser))

    jsonData = {
        'type': 'bar',
        'data': {
            'labels': list(numTicketsByUser.keys()),
            'datasets': [{
                'label': 'Number of Tickets',
                'data': list(numTicketsByUser.values()),
                'backgroundColor': backgroundColor,
                'borderColor': borderColor,
                'borderWidth': 1
            }]
        },
        'options': options
    }

    return jsonData


'''given a 1 column key table and 1 column table of countables, return a dict of counted data'''
def tableCounter(keys, tableToCount):
    dictionary = {}
    keysKey = list(keys[0].keys())[0]

    for row in range(len(keys)):
        status = keys[row][keysKey]
        dictionary[status] = 0

    if tableToCount:
        tableToCountKey = list(tableToCount[0].keys())[0]
        for row in range(len(tableToCount)):
            status = tableToCount[row][tableToCountKey]
            dictionary[status] += 1

    return dictionary


def getDefaultOptions(title):
    defaultOptions = {
        'aspectRatio': 1,
        'responsive': 1,
        'maintainAspectRatio': 0,
        'plugins': {
            'title': {
                'display': 1,
                'text': title
            }
        }
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
