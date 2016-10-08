import tkinter
import time
import threading
import sys
import queue

import GUI
import NetClient

class GuiPart:
    def __init__(self, master, myQueue, endCommand):
        self.myQueue = myQueue
        # Set up the GUI
    def processIncoming(self):
        """Handle all messages currently in the myQueue, if any."""
        while self.myQueue.qsize():
            try:
                msg = self.myQueue.get(0)

                gui.addMessage(msg)
                print (msg)
            except queue.Empty:
                # just on general principles, although we don't
                # expect this branch to be taken in this case
                pass

class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O).
        """
        self.master = master

        # Create the queue
        self.myQueue = queue.Queue()

        # Set up the GUI part
        self.guiThread = GuiPart(master, self.myQueue, self.endApplication)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start()

        # Start the periodic call in the GUI to check if the myQueue contains
        # anything
        self.periodicCall()

    def periodicCall(self):
        """
        Check every 200 ms if there is something new in the myQueue.
        """
        self.guiThread.processIncoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            sys.exit(1)
        self.master.after(200, self.periodicCall)

    def workerThread1(self):
        self.netClient = NetClient

        while self.running:
            # To simulate asynchronous I/O, we create a random number at
            # random intervals. Replace the following two lines with the real
            # thing.
            for i in range(5):
                time.sleep(1)
                for i in gui.poll():
                    self.netClient.recieve(i)
            msg = self.netClient.recieve(username)
            for i in msg:
                self.myQueue.put(i)

    def endApplication(self):
        self.running = 0

root = tkinter.Tk()

gui = GUI.GUI(root)
username = gui.getUsername()

client = ThreadedClient(root)
while(True):
    gui.update()