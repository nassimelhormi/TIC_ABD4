import pymysql.cursors
import random
import logging
import pprint

connection = pymysql.connect(host='mysqlmaster',
                             user='vdm',
                             password='vdm',
                             db='vdm_db',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)

select_mysql_slave = random.choice(['mysqlslave', 'mysqlslave2'])


def connect_to_slave():
    return pymysql.connect(host=select_mysql_slave,
                           user='vdm',
                           password='vdm',
                           db='vdm_db',
                           autocommit=True,
                           cursorclass=pymysql.cursors.DictCursor)


def select_booking_stats(tarif):
    connection_ro = connect_to_slave()
    sql = "SELECT count(*) AS `stats`" \
          "FROM Reservations " \
          "LEFT JOIN Spectateurs ON Reservations.id_reservation = Spectateurs.id_reservation " \
          "LEFT JOIN Clients ON Spectateurs.id_client = Clients.id_client " \
          "WHERE Clients.tarif = %s"
    logging.warning(sql)
    try:
        with connection_ro.cursor() as cursor:
            cursor.execute(sql, tarif)
            result = cursor.fetchone()
            logging.info(result)
            return result
    except Exception as e:
        print(str(e))
        return None
    finally:
        connection_ro.close()


def select_bookings_by_date(date_start, date_end):
    connection_ro = connect_to_slave()
    sql = "SELECT * " \
          "FROM Reservations " \
          "LEFT JOIN Spectateurs ON Reservations.id_reservation = Spectateurs.id_reservation " \
          "LEFT JOIN Clients ON Spectateurs.id_client = Clients.id_client " \
          "WHERE Reservations.day BETWEEN %s AND %s"
    logging.warning(sql)
    try:
        with connection_ro.cursor() as cursor:
            cursor.execute(sql, date_start, date_end)
            result = cursor.fetchall()
            logging.info(result)
            return result
    except Exception as e:
        print(str(e))
        return None
    finally:
        connection_ro.close()


def select_bookings_by_name(name):
    connection_ro = connect_to_slave()
    sql = "SELECT * " \
          "FROM Reservations " \
          "LEFT JOIN Spectateurs ON Reservations.id_reservation = Spectateurs.id_reservation " \
          "LEFT JOIN Clients ON Spectateurs.id_client = Clients.id_client " \
          "WHERE Reservations.g_name = %s"
    logging.warning(sql)
    try:
        with connection_ro.cursor() as cursor:
            cursor.execute(sql, name)
            result = cursor.fetchall()
            logging.info(result)
            return result
    except Exception as e:
        print(str(e))
        return None
    finally:
        connection_ro.close()


def select_all_bookings():
    connection_ro = connect_to_slave()
    try:
        with connection_ro.cursor() as cursor:
            sql = "SELECT * " \
                  "FROM Reservations " \
                  "LEFT JOIN Spectateurs ON Reservations.id_reservation = Spectateurs.id_reservation " \
                  "LEFT JOIN Clients ON Spectateurs.id_client = Clients.id_client"
            logging.warning(sql)
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except (pymysql.err.OperationalError, pymysql.ProgrammingError, pymysql.InternalError,
            pymysql.IntegrityError, TypeError) as error:
        logging.warning("insert Exception -> {}, SQL={}".format(str(error), sql))
    finally:
        connection_ro.close()


def count_all_bookings():
    connection_ro = connect_to_slave()
    try:
        with connection_ro.cursor() as cursor:
            sql = "SELECT COUNT(*) AS `nb_bookings` FROM Reservations WHERE 1 = 1"  # replace connection master par connection slev
            logging.warning(sql)
            cursor.execute(sql)
            result = cursor.fetchone()
            return result
    except (pymysql.err.OperationalError, pymysql.ProgrammingError, pymysql.InternalError,
            pymysql.IntegrityError, TypeError) as error:
        logging.warning("insert Exception -> {}, SQL={}".format(str(error), sql))
        return False
    finally:
        connection_ro.close()


def insert(sql, values):
    try:
        with connection.cursor() as cursor:
            logging.info("insert({}, {})".format(sql, values))
            cursor.execute(sql, values)
        # on commit les changements
        # connection.commit()

        with connection.cursor() as cursor:
            # On recupere le last_id inserted
            cursor.execute("SELECT  LAST_INSERT_ID();")
            result = cursor.fetchone()
            return result['LAST_INSERT_ID()']
    except (pymysql.err.OperationalError, pymysql.ProgrammingError, pymysql.InternalError,
            pymysql.IntegrityError, TypeError) as error:
        logging.warning("insert Exception -> {}, SQL={}, V={}".format(str(error), sql, values))
        return False


def fetchall(sql, values, is_master=False):
    try:
        with connection.cursor() as cursor:
            # On recupere le last_id inserted
            cursor.execute(sql % values)
            result = cursor.fetchall()
            logging.info(result)
            return result
    except Exception as e:
        print(str(e))
        logging.warning("fetchall -> " + str(e) + " sql -> " + sql % values)
        return []


def fetchone(sql, values, is_master=False):
    try:
        with connection.cursor() as cursor:
            # On recupere le last_id inserted
            cursor.execute(sql % values)
            result = cursor.fetchone()
            return result
    except Exception as e:
        print(str(e))
        return None


def create_reservation(day, hour, is_vr, g_name):
    sql = "INSERT INTO Reservations(day, hour, is_vr,g_name)  VALUES (%s, %s, %s, %s)"
    values = (day, hour, is_vr, g_name,)
    id_reservation = insert(sql, values)
    return (id_reservation)


def get_clients(json_data):
    client_list = []
    acheteur = json_data['Acheteur']
    k = {
        'gender': acheteur['Civilite'],
        'age': acheteur['Age'],
        'email': acheteur['Email'],
        'first_name': acheteur['Nom'],
        'last_name': acheteur['Prenom'],
        'is_acheteur': True
    }
    for reservation in json_data['Reservation']:
        d = {
            'gender': reservation['Spectateur']['Civilite'],
            'age': reservation['Spectateur']['Age'],
            'email': '',
            'first_name': reservation['Spectateur']['Nom'],
            'last_name': reservation['Spectateur']['Prenom'],
            'tarif': reservation['Tarif'],
            'is_acheteur': False
        }
        if (d['first_name'] != k['first_name'] and d['last_name'] != k['last_name']):
            client_list.append(d)
        else:
            k['tarif'] = reservation['Tarif']
    client_list.append(k)
    return client_list


def find_client(gender, first_name, last_name):
    sql = "SELECT id_client FROM Clients WHERE gender = '%s' AND first_name = '%s' AND last_name = '%s'"
    values = (gender, first_name, last_name,)
    rows = fetchall(sql, values, True)

    if len(rows) == 1:
        return rows[0]['id_client']
    return None


def insert_clients(list_clients):
    list_ids = []
    for client in list_clients:
        founded_client = find_client(client['gender'], client['first_name'], client['last_name'])
        logging.info("founded_client = {}".format(founded_client))
        if founded_client == None:
            try:
                is_acheteur = 0 if client['is_acheteur'] == True else 1
                values = (client['gender'], client['age'], client['email'], client['first_name'], client['last_name'],
                          client['tarif'], is_acheteur,)
                sql = "INSERT INTO Clients(gender,age,email,first_name,last_name,tarif,is_acheteur) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                pprint.pprint(sql)
                inserted_client = insert(sql, values)
                logging.info("inserted_client = {}".format(inserted_client))
                list_ids.append(inserted_client)
            except Exception as e:
                raise e
                logging.warning("insert_clients Exception ----> {}".format(str(e)))
        else:
            list_ids.append(founded_client)
    return list_ids


def insert_spectateurs(list_ids, id_reservation):
    logging.info(list_ids)
    for id_clients in list_ids:
        values = (id_clients, id_reservation,)
        sql = "INSERT INTO Spectateurs(id_client,id_reservation) VALUES(%s, %s)"
        insert(sql, values)


def process(json_data):
    try:
        logging.info("Process new reservation...")
        day = json_data['Game']['Jour']
        hour = json_data['Game']['Horaire']
        is_vr = 1 if json_data['Game']['VR'] == "Non" else 0
        g_name = json_data['Game']['Nom']

        logging.info("Inter booking.process")
        logging.info(json_data)
        logging.info("Create reservation")
        id_reservation = create_reservation(day, hour, is_vr, g_name)
        logging.info("New reservation created with ID = {}".format(id_reservation))
        client_list = get_clients(json_data)
        insered_clients = insert_clients(client_list)
        insert_spectateurs(insered_clients, id_reservation)
        return {'id': id_reservation, 'day': day, 'hour': hour, 'is_vr': is_vr, 'g_name': g_name}
    except Exception as e:
        logging.warning("Process error -> {}".format(str(e)))
        return {'error': 'Internal error'}
    finally:
        connection.close()