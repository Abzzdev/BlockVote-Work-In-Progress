import csv
import socket
import hashlib
import platform
import re, uuid

if platform == "linux" or platform == "linux2":
    # linux
    print()
    
elif platform == "darwin":
    # MAC OS X
    print()
    
elif platform == "win64" or platform == "win32":
    # Windows 64-bit and 32-bit
    import wmi
    c = wmi.WMI()

TCP_IP = 'blockvote2.ddns.net'
TCP_PORT = 5006
BUFFER_SIZE = 1024

# Encodes a string with SHA256 Encoding
def SHA256ENC(string):
    hash_func = hashlib.sha256()
    encoded_string=string.encode()
    hash_func.update(encoded_string)
    message = hash_func.hexdigest()
    return message

# Generates NodeID from the Hash of the MAC Address + the Hard Drive serial number.
def createNodeID():
    if platform == "win64" or platform == "win32":
        MACAddress = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    else:
        MACAddress = ':Null'
        
    HardDriveSerialNumber = c.Win32_PhysicalMedia()[0].wmi_property('SerialNumber').value.strip()
    NodeID = SHA256ENC(MACAddress + HardDriveSerialNumber)
    return NodeID


# Takes the .csv named knownNodes.csv and turns it into an array
def createNodeIDList():
    nodeListFilename = 'knownNodes.csv'
        
    Nodes = []
        
    with open(nodeListFilename, 'r', newline='') as fd:
        reader = csv.reader(fd)
        for row in reader:
            Nodes.append(row)
            #print(row)
            #print(Nodes)
            
    return Nodes
    
    
# Searches through the array of nodes and checks if your NodeID is in that List
def searchNodeIDList(NodeID, NodeIDList):
    print(NodeIDList)
    NodeID = NodeID.split(",")
    print(NodeID)
    if NodeID in NodeIDList:
        return True
    else:
        return False
        

def updateNodeIDList(Nodes):
    nodeListFilename = 'knownNodes.csv'
        
    with open(nodeListFilename, 'w') as fd:
        writer = csv.writer(fd)
        for node in Nodes:
            writer.writerow([node])
    
def main():
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((TCP_IP, TCP_PORT))
    
    pendingTransmissionFile = 'pendingTransmission.txt'
    pendingTransmission = open(pendingTransmissionFile,'rb')
    while True:
        l = pendingTransmission.read(BUFFER_SIZE)
        while (l):
            clientSocket.send(l)
            l = pendingTransmission.read(BUFFER_SIZE)
        if not l:
            pendingTransmission.close()
            clientSocket.close()
            break
    
    clientSocket.close()
    print('connection closed')

if __name__ == "__main__":
    NodeID = createNodeID()
    NodeList = createNodeIDList()
    nodeIDinList = searchNodeIDList(NodeID, NodeList)
    print(nodeIDinList)
    
    # If the ID isn't in the list append the ID to the list
    if nodeIDinList == False:
        NodeList.append(NodeID)
        
    # Overwrite contents of .csv file with updated data
    updateNodeIDList(NodeList)
    while True:
        main()
