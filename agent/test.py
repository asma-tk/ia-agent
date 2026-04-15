from agent.actions.create_file import create_file
from agent.agent import do

# create_file("coucou.txt")

test_list = [

    {"action": "welcom", 
     "params": []},

     
    {
        
        "action": "hello",
        "params": []
    },
    {
        "action": "create_file",
        "params": ["fichier1"]
    },
{
        "action": "create_file",
        "params": ["fichier2"]
    },
{
        "action": "create_file",
        "params": ["fichier3"]
    },
    {
        "action": "delete_file",
        "params": ["fichier1"]
    },
    {
        "action": "delete_file",
        "params": ["fichier2"]
    },
    {
        "action": "delete_file",
        "params": ["fichier3"]
    },
    {"action":"writein_file",
     "params":["fichier1",""]},


       {"action":"writein_file",
     "params":["fichier2",""]},



       {"action":"writein_file",
     "params":["fichier3",""]},

        {"action":"deletein_file",
        "params":["fichier1",""]},

        {"action":"deletein_file",  
        "params":["fichier2",""]},


        {"action":"deletein_file",
        "params":["fichier3",""]},
]

do(test_list)