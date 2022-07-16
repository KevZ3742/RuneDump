from functools import partial
from operator import index
import requests
import base64
import json
from tkinter import *
import sys

root = Tk()
root.title("Rune Dump")
rows = []

# Get Lockfile
try:
    with open("/Applications/League of Legends.app/Contents/LoL/lockfile") as r:
        lockfile = r.read().split(':')
except:
    sys.exit(0)

root.lift()
with open('SavedRunes.json') as json_file:
    body = json.load(json_file)

headers = {"Authorization" : "Basic " + str(base64.b64encode(bytes('riot:' + lockfile[3], 'utf-8')))[2:-1]}

def request(method, endpoint, data=None):
    if method == "get":
        return requests.get("https://127.0.0.1:" + lockfile[2] + endpoint, verify = False, headers=headers, json=data)
    elif method == "post":
        return requests.post("https://127.0.0.1:" + lockfile[2] + endpoint, verify = False, headers=headers, json=data)
    elif method == "delete":
        return requests.delete("https://127.0.0.1:" + lockfile[2] + endpoint, verify = False, headers=headers, json=data)
    return "-1"

def loadJson(body):
    with open('SavedRunes.json') as json_file:
        body = json.load(json_file)

def saveJson():
    with open('SavedRunes.json', 'w') as new:
        json.dump(body, new)

class EditableLabel(Label):
    id = None

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.entry = Entry(self)
        self.entry.insert(0, self.cget("text"))
        self.bind("<Double-1>", self.edit_start)
        self.entry.bind("<Return>", self.edit_stop)
        self.entry.bind("<FocusOut>", self.edit_stop)
        self.entry.bind("<Escape>", self.edit_cancel)

    def setId(self, index):
        self.id = index

    def edit_start(self, event=None):
        self.entry.place(relx=.5, rely=.5, relwidth=1.0, relheight=1.0, anchor="center")
        self.entry.focus_set()

    def edit_stop(self, event=None):
        oldName = self.cget("text")
        loadJson(body)
        if self.entry.get() == '':
            self.configure(text=oldName)
        else:
            self.configure(text=self.entry.get())
        body[self.id]['name'] = self.cget("text")
        saveJson()
        self.entry.place_forget()

    def edit_cancel(self, event=None):
        self.entry.delete(0, "end")
        self.entry.place_forget()

def exportClicked():
    runePages = request("get", "/lol-perks/v1/pages")
    runeJson = (runePages.json())

    loadJson(body)

    for a in runeJson:
        if a['current']:
            currentRunes = {}

            currentRunes["name"] = a["name"]
            currentRunes["primaryStyleId"] = a["primaryStyleId"]
            currentRunes["subStyleId"] = a["subStyleId"]
            currentRunes["selectedPerkIds"] = a["selectedPerkIds"]
            currentRunes["current"] = "true"

            body.append(currentRunes)

    saveJson()
    createImports()

    print('Export Successful')

def idSearchClicked():
    text = entry.get()
    loadJson(body)

    id = request('get', '/lol-perks/v1/currentpage')
    runeID = (id.json())

    request("delete", "/lol-perks/v1/pages/" + str(runeID["id"]))
    request("post", "/lol-perks/v1/pages", body[int(text)])

    print('Import Successful')
    
def specificImportClicked(i):
    loadJson(body)

    id = request('get', '/lol-perks/v1/currentpage')
    runeID = (id.json())

    request("delete", "/lol-perks/v1/pages/" + str(runeID["id"]))
    request("post", "/lol-perks/v1/pages", body[i])

    print('Import Successful')

def deleteImportClicked(i):
    loadJson(body)

    body.pop(i)
    for x in range(len(rows)):
        rows[x]['id'].destroy()
        rows[x]['name'].destroy()
        rows[x]['import'].destroy()
        rows[x]['delete'].destroy()

    saveJson()
    createImports()

    print('Delete Successful')

def createImports():
    loadJson(body)

    i = 0
    for a in body:
        temp = {}

        temp['id'] = Label(root, text='[' + str(i) + ']', width=15)
        temp['name'] = EditableLabel(root, text=a['name'], width=15)
        temp['name'].setId(i)
        temp['import'] = Button(root, text='▶', width=1, command=partial(specificImportClicked, i))
        temp['delete'] = Button(root, text='🗑️', width=1, command=partial(deleteImportClicked, i))
        temp['id'].grid(row=i+2,column=0)
        temp['name'].grid(row=i+2,column=1, columnspan=12)
        temp['import'].grid(row=i+2,column=13)
        temp['delete'].grid(row=i+2,column=14)

        rows.append(temp)
        i += 1

Button(root, text='⬆️', width=1, command=exportClicked).grid(row=1, column=14)
Label(root, text='Rune Index:', width=15).grid(row=1, column=0)
entry = Entry(root, width=15)
entry.grid(row=1, column=1, columnspan=12)
Button(root, text='🔍', width=1, command=idSearchClicked).grid(row=1,column=13)
createImports()

mainloop()