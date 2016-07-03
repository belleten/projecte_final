import zmq
from datetime import datetime, date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ORM.database import User, Base, Keg

# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
sock = context.socket(zmq.REP)
sock.bind("tcp://127.0.0.1:5678")

def update_database(amount_recv, nfc_user_recv, num_keg_recv):
    try:
        engine = create_engine('sqlite:///sqlalchemy_database.db')
        DBSession = sessionmaker(bind = engine)
        session = DBSession()
        ed_user = session.query(User).filter_by(userid = nfc_user_recv)
        try:
            ed_user = ed_user.one()
        except:
            create_user = User(username = 'No Name', userid = nfc_user_recv, realname = 'No Name', email = 'No Email', amount = amount_recv)
            session.add(create_user)
            session.commit()

        total_amount_user = float(ed_user.amount) + amount_recv
        ed_user.amount = total_amount_user
        session.commit()

        #The Keg id must be create before
        ed_keg = session.query(Keg).filter_by(kegid = num_keg_recv).one()
        total_amount_keg = float(ed_keg.amount) + amount_recv
        ed_keg.amount = total_amount_keg
        session.commit()
        return True

    except:
        return False


# Run a simple "Echo" server
while True:
    resultat = sock.recv()
    print resultat
    resultat1 = resultat.split(",")

    amount_recv = float(resultat1[0])
    nfc_user_recv = resultat1[1]
    num_keg_recv = resultat1[2]

    update_results = update_database(amount_recv, nfc_user_recv, num_keg_recv)

    sock.send("RECEIVED, KEEP DRINKING!!!")
