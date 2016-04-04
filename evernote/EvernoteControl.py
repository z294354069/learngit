#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import os, sys

from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Error

SERVICE_HOST = 'app.yinxiang.com'
Dev_Token = ''


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




if __name__ == '__main__':
    evernote = EvernoteControl()
    evernote.makeNotebook('张家语zrjy')
    # evernote.displayNoteBook()
    # evernote.deleteNotebook("python notebook")
    print("\r\n")
    evernote.displayNoteBook()
    evernote.makeNote('python note', 'this note is from python张忍', "python notebook")