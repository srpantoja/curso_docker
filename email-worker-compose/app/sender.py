import psycopg2
import redis
import json
import os
from bottle import Bottle, request

class Sender(Bottle):
    def __init__(self):
        super().__init__()
        self.route('/', method='POST', callback=self.send)
        redis_host = os.getenv('REDIS_HOST', 'queue')
        self.fila = redis.StrictRedis(host=redis_host, port=6379, db=0)
        
        db_name = os.getenv("DB_NAME", 'invalid')
        db_host = os.getenv("DB_HOST", 'db')
        db_user = os.getenv("DB_USER", 'postgres')
        db_password = os.getenv("DB_PASSWORD", 'invalid')

        dsn = f'dbname={db_name} user={db_user} host={db_host} password={db_password}'
        self.conn = psycopg2.connect(dsn)

    def register_message(self, email, assunto, mensagem):
        cur = self.conn.cursor()
        SQL = 'INSERT INTO emails(email, assunto, mensagem) VALUES (%s, %s, %s)'
        cur.execute(SQL, (email, assunto, mensagem))
        self.conn.commit()
        cur.close()

        print('Mensagem registrada !')

    def send(self):
        print(request.forms.get)
        email = request.forms.get('email')
        assunto = request.forms.get('assunto')
        mensagem = request.forms.get('mensagem')
        msg = {'email': email, 'assunto': assunto, 'mensagem': mensagem}
        self.fila.rpush('sender', json.dumps(msg))

        self.register_message(email, assunto, mensagem)
        return 'Mensagem enfileirada ! Email: {} Assunto: {} Mensagem: {}'.format(
            email, assunto, mensagem
        )




if __name__ =='__main__':
    sender = Sender()
    sender.run(host='0.0.0.0', port=9090, debug=True)