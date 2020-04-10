import threading


myPort =None
adminPort=None
myUrl=None
myIP=None
adminIP=None

publicKey=None
privateKey=None
id=None

blockchain=None
current_transactions={}#dictionary για να τα βρισκουμε με βαση το id
transaction_pool=[]

allUrls=[]
allPublicKeys=[]

utxos=[]
#utxos_copy=[]
hasReceivedGenesisBlock=False
connectedParticipants=0

#αλλάζουμε αυτες τις τιμές για να παραμετροποι΄ήσουμε το συστημά μας
numOfParticipants=5
capacity=10
difficulty=4

lock = threading.RLock()# ώστε καθε νημα που έχει προσβαση στις ανώτερες τιμές να εχει ατομική προσβαση

#
miningLock=threading.RLock()# ώστε τα νήματα που κανουν mine να κάνουν Mine στην σειρά
someoneIsMining=False

#μετρηκες
benchmarkLock=threading.RLock()
transactionTimes=[]
miningTimes=[]
transactionsServiced=0

#για οταν μας ζηταν το chain, θελουμε ανεξαρτητες δομες
chainLock=threading.RLock()
blockchainForCons=None
current_transactionsForCons={}
utxosForCons=[]
transactionPoolForCons=[]
