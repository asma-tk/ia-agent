from actions.create_file import create_file
from actions.delete_file import delete_file
from actions.writein_file import writein_file
from actions.deletein_file import deletein_file 
from actions.execute_regex import execute_regex
from agent import do

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
        {"action":"execute_regex",
        "params":["luna", "\d"]},

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
]

do(test_list)