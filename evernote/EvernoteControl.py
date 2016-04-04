#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

from evernote.api.client import EvernoteClient
import evernote.edam.notestore.NoteStore as NoteStore
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Error

SERVICE_HOST = 'app.yinxiang.com'
Dev_Token = 'S=s16:U=33fa90:E=15b37ecfe6b:C=153e03bd190:P=1cd:A=en-devtoken:V=2:H=9cecf8305cc371bb7a2c1ce1ec6292cb'


class EvernoteControl:
    def __init__(self):
        self.client = EvernoteClient(token=Dev_Token, service_host=SERVICE_HOST)
        self.userStore = self.client.get_user_store()
        self.noteStore = self.client.get_note_store()
        print 'Login Succeed as ' + self.userStore.getUser().username


    def makeNotebook(self, notebookName):
        notebook = Types.Notebook()
        notebook.name = notebookName
        try:
            notebook = self.noteStore.createNotebook(notebook)
            print('create "%s" successful'%notebookName)
            return notebook
        except Error.EDAMUserException:
            print('create "%s" failed. Maybe you should rename the notebook name'%notebookName)

    def __listNotebook(self):
        try:
            notebooks = self.noteStore.listNotebooks()
            return notebooks
        except Error.EDAMUserException, Error.EDAMUserException:
            print('get notebook error')
            return None

    def __findNoteBookGUID(self, notebookName):
        guid = ""
        notebooks = self.__listNotebook()
        if notebooks is not None:
            for n in notebooks:
                if notebookName == n.name:
                    guid = n.guid
                    break
        return guid


    def displayNoteBook(self):
        notebooks = self.__listNotebook()
        if notebooks is not None:
            for n in notebooks:
                print(n.name + "  " + n.guid)
        else:
            print('No notebooks. Please create one')


    def deleteNotebook(self, notebook):
        #guid = ""
        notebooks = self.__listNotebook()
        guid = self.__findNoteBookGUID(notebook)
        if guid is not "":
            self.noteStore.expungeNotebook(guid)
        else:
            print("%s is not exited"%notebook)


    def makeNote(self, noteTitle, noteBody, parentNotebook = None):
        nBody = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>'
        nBody += '<!DOCTYPE en-note SYSTEM \"http://xml.evernote.com/pub/enml2.dtd\">'
        nBody += "<en-note>%s</en-note>" % noteBody

        ourNote = Types.Note()
        ourNote.title = noteTitle
        ourNote.content = nBody

        # if parentNotebook and hasattr(parentNotebook, 'guid'):
        #     ourNote.notebookGuid = parentNotebook.guid

        if parentNotebook :
            guid = self.__findNoteBookGUID(parentNotebook)
            ourNote.notebookGuid = guid

        try:
            note = self.noteStore.createNote(ourNote)
        except Error.EDAMUserException, edue:
            print("EDAMUserException:", edue)
            return None

        except Error.EDAMNotFoundException, ednfe:
            print("EDAMNotFoundException: Invalid parent notebook GUID")
            return None

        return note

    def showNote(self):
        filter = NoteStore.NoteFilter()
        filter.ascending = False
        spec = NoteStore.NotesMetadataResultSpec()
        spec.includeTitle = True
        ourNoteList = self.noteStore.findNotesMetadata(Dev_Token, filter, 0, 100, spec)

        wholeNotes = []
        for note in ourNoteList.notes:
            # wholeNote = self.noteStore.getNote(Dev_Token, note.guid, True, False, False, False)
            # print("Content length: %d" % wholeNote.contentLength)
            # wholeNotes.append(wholeNote)
            # for note in wholeNotes:
            #     print(note.content)
            print(self.noteStore.getNoteContent(Dev_Token, note.guid))



if __name__ == '__main__':
    evernote = EvernoteControl()
    # evernote.makeNotebook('张家语zrjy')
    # # evernote.displayNoteBook()
    # evernote.deleteNotebook("python notebook")
    # print("\r\n")
    # evernote.displayNoteBook()
    # evernote.makeNote('python note', 'this note is from python张忍', "python notebook")
    # evernote.showNote()



    path = "C:\Users\Administrator\Desktop\dev_token.txt"
    with open(path, "r") as f:
        content = f.read()
    fileName = path.split("\\")
    fileName = fileName.pop()
    title = fileName.split(".")[0]
    evernote.makeNote(title, content, "python notebook")

    evernote.showNote()

